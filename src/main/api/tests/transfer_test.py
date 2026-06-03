from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransfer:
    def test_transfer_valid(self):
        create_user_request = CreateUserRequest(username="Max00370", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00370", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        replenishment_deposit_request = DepositAccountRequest(accountId=create_account_response.id, amount=1000.5)
        replenishment_deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00370", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(replenishment_deposit_request)

        create_account_two_for_user = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00370", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        transfer_request = TransferAccountRequest(fromAccountId=replenishment_deposit_response.id, toAccountId=create_account_two_for_user.id, amount=500.75)
        transfer_response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00370", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)
        assert transfer_response.fromAccountIdBalance == 1000.50 - 500.75

    def test_transfer_invalid(self):
        create_user_request = CreateUserRequest(username="Max00371", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00371", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        replenishment_deposit_request = DepositAccountRequest(accountId=create_account_response.id, amount=1000.5)
        replenishment_deposit_response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00371", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(replenishment_deposit_request)

        create_account_two_for_user = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00371", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        transfer_request = TransferAccountRequest(fromAccountId=replenishment_deposit_response.id,
                                                  toAccountId=create_account_two_for_user.id, amount=5000.75)
        TransferRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00371", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)