"""duck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from app.views import IndexView, LoginView, SettingsView, PasswordView, AboutView, WalletView, PublicWalletView, RewardView
from social_django.urls import urlpatterns as social_urls
from django.contrib.auth.views import logout as logout_view

static_urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_urlpatterns = [
	url(r'^admin/', admin.site.urls),

	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^about/$', AboutView.as_view(), name='about'),
	url(r'^wallet/$', WalletView.as_view(), name='wallet'),
	url(r'^reward/$', RewardView.as_view(), name='reward'),
	url(r'^wallet/(?P<id>\d+)/$', PublicWalletView.as_view(), name='public_wallet'),

	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^start/$', LoginView.as_view(), name='start', kwargs=dict(act='start')),
	url(
		r'^logout/$',
		logout_view,
		{'template_name': 'templates/logout.html'},
		name='logout'
	),
	url(r'^settings/$', SettingsView.as_view(), name='settings'),
	url(r'^password/$', PasswordView.as_view(), name='password'),

	url('', include(social_urls, namespace='social')),

]

urlpatterns = app_urlpatterns + static_urlpatterns
