import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

class Wallet(models.Model):
	display_name = models.CharField(max_length=100, null=True)
	title = models.CharField(max_length=100)
	local_id = models.IntegerField()
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	balance = models.IntegerField()
	last_reward = models.DateTimeField(null=True)
	public = models.BooleanField(default=False)
	anonymous = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now_add=True)

	def get_name(self):
		if self.display_name is None:
			return self.title

		return self.display_name

	def can_take_reward(self):
		if self.last_reward is None:
			return True

		now = timezone.now()
		return self.last_reward + datetime.timedelta(days=settings.REWARD_COOLDOWN) < now


class Transfer(models.Model):
	sender = models.ForeignKey('Wallet', related_name='sender', null=True)
	receiver = models.ForeignKey('Wallet', related_name='receiver')
	amount = models.IntegerField()
	comment = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True)


class PendingTransfer(models.Model):
	TYPE_CHOICE = (
		('twitter', 'Twitter'),
		('vk', 'VK'),
		('email', 'Email'),
	)
	sender = models.ForeignKey('Wallet')
	amount = models.IntegerField()
	cancelled = models.BooleanField()
	comment = models.CharField(max_length=500)
	receiver_type = models.CharField(max_length=10, choices=TYPE_CHOICE, blank=False)
	receiver = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now=True)
