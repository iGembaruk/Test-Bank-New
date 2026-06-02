import requests


class TestRepayCreditAccount:
    def test_repay_credit_valid(self):
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
                "username": "Egor25",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
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
                "username": "Egor24",
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
        account_id = create_account_for_user.json().get("id")

        credit_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_response.status_code == 201
        credit_id = credit_response.json().get("creditId")

        repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 5000.0
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert repay_response.status_code == 200
        assert repay_response.json().get("creditId") == credit_id
        assert repay_response.json().get("amountDeposited") == 5000.0

    def test_repay_credit_invalid(self):
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
                "username": "Egor26",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
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
                "username": "Egor26",
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
        account_id = create_account_for_user.json().get("id")

        credit_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_response.status_code == 201
        credit_id = credit_response.json().get("creditId")

        repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 5000.1
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert repay_response.status_code == 422
        assert repay_response.json().get("error") == "Insufficient funds. Current balance: 5000.00, required: 5000.10"
