import requests


class TestTransfer:
    def test_transfer_valid(self):
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
        token_admin = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Egor07",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_admin}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Egor07",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token_user = login_user_response.json().get("token")

        create_account_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_for_user.status_code == 201
        assert create_account_for_user.json().get("balance") == 0
        account_id = create_account_for_user.json().get("id")

        replenishment_deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": int(account_id),
                "amount": 1000.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}",
                "Content-Type": "application/json"
            }
        )
        assert replenishment_deposit_response.status_code == 200
        assert replenishment_deposit_response.json().get("balance") == 1000.5

        create_account_two_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_two_for_user.status_code == 201
        assert create_account_two_for_user.json().get("balance") == 0
        account_id_two = create_account_two_for_user.json().get("id")

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id,
                "toAccountId": account_id_two,
                "amount": 500.75
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}",
                "Content-Type": "application/json"
            }
        )

        assert transfer_response.status_code == 200
        assert transfer_response.json().get("fromAccountId") == int(account_id)
        assert transfer_response.json().get("toAccountId") == int(account_id_two)
        assert transfer_response.json().get("fromAccountIdBalance") == 1000.50 - 500.75

    def test_transfer_invalid(self):
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
        token_admin = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Egor10",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_admin}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Egor10",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token_user = login_user_response.json().get("token")

        create_account_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_for_user.status_code == 201
        assert create_account_for_user.json().get("balance") == 0
        account_id = create_account_for_user.json().get("id")

        replenishment_deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": int(account_id),
                "amount": 1000.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}",
                "Content-Type": "application/json"
            }
        )
        assert replenishment_deposit_response.status_code == 200
        assert replenishment_deposit_response.json().get("balance") == 1000.5

        create_account_two_for_user = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_two_for_user.status_code == 201
        assert create_account_two_for_user.json().get("balance") == 0
        account_id_two = create_account_two_for_user.json().get("id")

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id,
                "toAccountId": account_id_two,
                "amount": 5000.75
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}",
                "Content-Type": "application/json"
            }
        )

        assert transfer_response.status_code == 422
        assert transfer_response.json().get("error") == "Insufficient funds. Current balance: 1000.50, required: 5000.75"
