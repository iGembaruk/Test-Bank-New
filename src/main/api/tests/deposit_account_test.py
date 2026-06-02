import pytest
import requests


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Egor02",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Egor02",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_account_for_user.status_code == 201
        assert create_account_for_user.json().get("balance") == 0
        id_account = create_account_for_user.json().get("id")

        replenishment_deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": int(id_account),
                "amount": 1000.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert replenishment_deposit_response.status_code == 200
        assert replenishment_deposit_response.json().get("balance") == 1000.5

    def test_deposit_account_invalid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Egor04",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Egor04",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_account_for_user.status_code == 201
        assert create_account_for_user.json().get("balance") == 0
        id_account = create_account_for_user.json().get("id")

        replenishment_deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": id_account,
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert replenishment_deposit_response.status_code == 400
        assert replenishment_deposit_response.json().get("error") == "Amount is required"
