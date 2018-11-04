"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
from decimal import Decimal

import pytest

import billing.models as billing_models


@pytest.fixture(autouse=True, scope='function')
def media_root(settings, tmpdir_factory):
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True, scope='function')
def password_hashers(settings):
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(scope='function')
def first_account(admin_user):
    account_id = 'bob123'
    return billing_models.Account.objects.create(id=account_id, user=admin_user, balance=Decimal('999.0'))


@pytest.fixture(scope='function')
def second_account(admin_user):
    account_id = 'alice456'

    return billing_models.Account.objects.create(id=account_id, user=admin_user, balance=0)
