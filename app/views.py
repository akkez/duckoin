import datetime

from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

from app.utils import get_or_create_wallet, transfer_funds, BillingException
from app.models import Transfer, Wallet


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


class WalletView(LoginRequiredMixin, TemplateView):
	template_name = 'templates/wallet.html'

	def get_context_data(self, **kwargs):
		wallet = get_or_create_wallet(self.request.user)
		wallet_url = self.request.build_absolute_uri(wallet.get_link())

		can_take_reward = wallet.can_take_reward()
		next_reward = timezone.now() if can_take_reward else wallet.last_reward + settings.REWARD_DELTA
		history = Transfer.objects.filter(Q(receiver=wallet) | Q(sender=wallet)).order_by('-created')
		return super().get_context_data(
			wallet=wallet, wallet_url=wallet_url, can_take_reward=can_take_reward, next_reward=next_reward, history=history, **kwargs)


class RewardView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		wallet = get_or_create_wallet(self.request.user)

		if not wallet.can_take_reward():
			messages.error(request, "В данный момент вы не можете получить уточки :(")
			return redirect('wallet')

		success = False
		try:
			success = transfer_funds(None, wallet, settings.REWARD_AMOUNT, "Держи уточки!")
		except BillingException as e:
			messages.error(request, "Ошибка: {}".format(e))

		if success:
			messages.success(request, "Уточки уже у тебя на счёте!")
			wallet.last_reward = timezone.now()
			wallet.save()

		return redirect('wallet')


class PublicWalletView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse('dummy')

	# template_name = 'templates/public_wallet.html'


class TransferView(LoginRequiredMixin, TemplateView):
	def get_context_data(self, **kwargs):
		wallet = get_or_create_wallet(self.request.user)
		history = Transfer.objects.filter(sender=wallet).order_by('-created')
		return super().get_context_data(history=history, wallet=wallet, **kwargs)

	template_name = 'templates/transfer.html'
