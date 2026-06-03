import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self):
        create_user_request = CreateUserRequest(username="Max00366", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00366", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        replenishment_deposit_request = DepositAccountRequest(accountId=create_account_response.id, amount=1000.5)
        replenishment_deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00366", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(replenishment_deposit_request)

        assert replenishment_deposit_response.balance == 1000.5

    def test_deposit_account_invalid(self):
        create_user_request = CreateUserRequest(username="Max00367", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00367", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        replenishment_deposit_request = DepositAccountRequest(accountId=create_account_response.id)
        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00367", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(replenishment_deposit_request)

