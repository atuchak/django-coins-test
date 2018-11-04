from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from billing.models import Payment


@pytest.mark.parametrize('payment_amount, balance', [
    [Decimal('10'), 10],
    [-0, 0],
])
def test_account_balance_change(second_account, payment_amount, balance):
    assert second_account.balance == Decimal('0.0')
    assert second_account.balance == 0

    second_account.change_balance(amount=payment_amount)
    assert second_account.balance == balance


def test_account_balance_change_raises_exc(second_account):
    with pytest.raises(ValidationError):
        second_account.change_balance(amount=-10)


def test_payment_create_payment(first_account, second_account):
    amount = Decimal('19.39')
    first_account_balance = first_account.balance
    second_account_balance = second_account.balance
    num_of_payments = Payment.objects.count()
    Payment.create_payment(amount=amount, from_account_id=first_account.id, to_account_id=second_account.id)
    new_num_of_payments = Payment.objects.count()
    assert num_of_payments + 2 == new_num_of_payments

    first_account.refresh_from_db()
    new_first_account_balance = first_account.balance
    second_account.refresh_from_db()
    new_second_account_balance = second_account.balance
    assert first_account_balance - amount == new_first_account_balance
    assert second_account_balance + amount == new_second_account_balance
