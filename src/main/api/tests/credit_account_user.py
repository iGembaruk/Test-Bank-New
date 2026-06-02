import requests


class TestCreditAccountUser:
    def test_credit_account_user_valid(self):
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
                "username": "Egor14",
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
                "username": "Egor14",
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

        credit_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": id_account,
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
        assert credit_response.json().get("amount") == 5000
        assert credit_response.json().get("termMonths") == 12
        assert credit_response.json().get("balance") == 5000

    def test_credit_account_user_invalid(self):
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
                "username": "Egor16",
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
                "username": "Egor16",
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

        credit_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": id_account,
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

        credit_two_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": id_account,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_two_response.status_code == 404
        assert credit_two_response.json().get("error") == "Only one active credit allowed per user"
