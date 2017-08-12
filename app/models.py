from django.db import models


# Create your models here.
class Wallet(models.Model):
	display_name = models.CharField(max_length=100),
	title = models.CharField(max_length=100),
	local_id = models.IntegerField(),
	user = models.ForeignKey('User'),

