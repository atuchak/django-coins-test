from decimal import Decimal

import pytest


@pytest.mark.django_db(transaction=True)
def test_accounts_list(client):
    url = '/v1/accounts'
    resp = client.get(url)
    assert resp
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.django_db(transaction=True)
def test_accounts_create(client, admin_user):
    url = '/v1/accounts'
    data = {}
    resp = client.post(url, data=data)
    assert resp
    assert resp.status_code == 400

    data = {
        'id': 'user_acc_1',
        'owner': admin_user.id,
        'balance': '111.00',
    }
    resp = client.post(url, data=data)
    json_resp = resp.json()
    assert resp
    assert resp.status_code == 201
    assert isinstance(json_resp, dict)
    assert json_resp == data


@pytest.mark.django_db(transaction=True)
def test_payments_list(client):
    url = '/v1/payments'
    resp = client.get(url)
    assert resp
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.django_db(transaction=True)
def test_payments_create(client, admin_user, first_account, second_account):
    url = '/v1/payments'

    data = {
        'amount': '100',
        'account': second_account.id,
        'from_account': first_account.id,
    }
    resp = client.post(url, data=data)
    json_resp = resp.json()
    assert json_resp
    assert resp.status_code == 201
    assert isinstance(json_resp, dict)
    assert Decimal(json_resp['amount']) == - Decimal(data['amount'])
    assert json_resp['account'] == second_account.id
    assert json_resp['from_account'] == first_account.id
    assert json_resp['direction'] == 'outgoing'


@pytest.mark.django_db(transaction=True)
def test_payments_create_error_400(client, admin_user, first_account, second_account):
    url = '/v1/payments'
    data = {}
    resp = client.post(url, data=data)
    assert resp
    assert resp.status_code == 400

    data = {
        'amount': '-100',
        'account': second_account.id,
        'from_account': first_account.id,
    }
    resp = client.post(url, data=data)
    json_resp = resp.json()
    assert json_resp
    assert resp.status_code == 400
