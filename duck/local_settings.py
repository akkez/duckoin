# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'duck',
		'USER': '',
		'PASSWORD': '',
		'HOST': 'localhost',
		'PORT': '3306',
	}
}

SOCIAL_AUTH_VK_OAUTH2_KEY = '6146235'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '***'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_TWITTER_KEY = 'qaB193YE8jK70F8P0ihIqP6n4'
SOCIAL_AUTH_TWITTER_SECRET = '***'
