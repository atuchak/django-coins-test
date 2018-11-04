from django.db import models, transaction
from django.core.exceptions import ValidationError

from billing.mixins import CreateUpdateMixin

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Account(CreateUpdateMixin, models.Model):
    id = models.TextField(primary_key=True, editable=False)  # NoQA
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    @transaction.atomic
    def change_balance(self, amount):
        """
        Lock Account row and change the balance

        :param amount: Amount of balance change
        :type amount: decimal.Decimal
        :return: None
        """
        account = Account.objects.select_for_update().get(pk=self.pk)
        account.balance += amount
        account.save()
        self.refresh_from_db()

    def clean(self):
        """
        Validate balance value before save.

        :return: None
        """
        if self.balance < 0:
            msg = _('Account balance can not be negative')
            raise ValidationError(msg)

    def save(self, **kwargs):
        """
        Override default save() and add model validation before save.
        """
        self.full_clean()
        return super().save(**kwargs)


class Payment(CreateUpdateMixin, models.Model):
    DIRECTION_CHOICES = [('imcoming', 'incoming'), ('outgoing', 'outgoing')]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_to_account')
    direction = models.TextField(choices=DIRECTION_CHOICES)

    class Meta:
        ordering = ['-id']

    @classmethod
    @transaction.atomic
    def create_payment(cls, amount, from_account_id, to_account_id):
        try:
            from_account = Account.objects.select_for_update().get(pk=from_account_id)
            to_account = Account.objects.select_for_update().get(pk=to_account_id)
        except Account.DoesNotExist as e:
            raise e

        from_account.change_balance(amount=-amount)
        to_account.change_balance(amount=+amount)

        outgoing_payment = Payment.objects.create(
            amount=-amount, from_account=from_account, to_account=to_account, direction='outgoing',
        )
        incoming_payment = Payment.objects.create(
            amount=+amount, from_account=to_account, to_account=to_account, direction='incoming',
        )

        return outgoing_payment, incoming_payment
