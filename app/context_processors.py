from django.conf import settings


def some_settings(request):
	return {
		'REWARD_COOLDOWN': settings.REWARD_COOLDOWN,
		'REWARD_AMOUNT': settings.REWARD_AMOUNT
	}
