from django.db import transaction, IntegrityError

from app.models import Wallet, Transfer
import random


def get_or_create_wallet(user):
	try:
		wallet = Wallet.objects.get(user=user)
	except Wallet.DoesNotExist:
		# creating new wallet
		wallet = Wallet()
		wallet.user = user
		wallet.local_id = random.randint(1000000, 9999999)
		wallet.title = 'DUCK.{}'.format(wallet.local_id)
		wallet.display_name = None
		wallet.balance = 0
		wallet.save()
	# print("New wallet id =", wallet.pk)

	return wallet


class BillingException(Exception):
	pass


def transfer_funds(from_wallet, to_wallet, amount, comment):
	if from_wallet is not None:
		if from_wallet.balance < amount:
			raise BillingException('Not enough funds')

	if to_wallet is None:
		raise BillingException('Receiver cannot be null')

	if comment is None or comment == '':
		raise BillingException('Missing comment')

	try:
		amount = int(amount)
	except:
		raise BillingException('Incorrect transfer amount')

	if amount < 0:
		raise BillingException('Cannot transfer negative funds')

	try:
		with transaction.atomic():
			transfer = Transfer()
			transfer.amount = amount
			transfer.comment = comment
			transfer.sender = from_wallet
			transfer.receiver = to_wallet
			transfer.save()

			if from_wallet is not None:
				from_wallet.balance -= amount
				from_wallet.save()

			to_wallet.balance += amount
			to_wallet.save()
	except IntegrityError as e:
		raise BillingException('Transaction integrity error: {}'.format(e))

	return True
