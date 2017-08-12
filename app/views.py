from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth


class IndexView(TemplateView):
	template_name = 'templates/index.html'
	pass


class LoginView(TemplateView):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('index')
		if kwargs.get('act') == 'start':
			messages.info(request, 'Для получения уточек нужно авторизироваться на сайте')
		return super().dispatch(request, *args, **kwargs)

	template_name = 'templates/login.html'


class AboutView(TemplateView):
	template_name = 'templates/about.html'


class SettingsView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		user = request.user

		try:
			vk_login = user.social_auth.get(provider='vk-oauth2')
		except UserSocialAuth.DoesNotExist:
			vk_login = None

		try:
			twitter_login = user.social_auth.get(provider='twitter')
		except UserSocialAuth.DoesNotExist:
			twitter_login = None

		can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

		return render(request, 'templates/settings.html', {
			'vk_login': vk_login,
			'twitter_login': twitter_login,
			'can_disconnect': can_disconnect
		})


class PasswordView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		if request.user.has_usable_password():
			PasswordForm = PasswordChangeForm
		else:
			PasswordForm = AdminPasswordChangeForm

		form = PasswordForm(request.user)
		return render(request, 'templates/password.html', {'form': form})

	def post(self, request, *args, **kwargs):
		if request.user.has_usable_password():
			PasswordForm = PasswordChangeForm
		else:
			PasswordForm = AdminPasswordChangeForm

		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Ваш пароль был обновлен')
			return redirect('password')
		else:
			messages.error(request, 'Пожалуйста, исправьте допущенные ошибки')
		return render(request, 'templates/password.html', {'form': form})
