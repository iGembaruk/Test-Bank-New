from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.requests.repay_credit_requester import RepayCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestRepayCreditAccount:
    def test_repay_credit_valid(self):
        create_user_request = CreateUserRequest(username="Max00363", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00363", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        body_for_credit = CreditRequest(accountId=account_response.id, amount=5000, termMonths=12)
        credit_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00363", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(body_for_credit)

        repay_request = RepayCreditRequest(creditId=credit_response.creditId, accountId=credit_response.id,
                                           amount=5000.0)
        repay_response = RepayCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00363", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_request)
        assert repay_response.amountDeposited == 5000.0

    def test_repay_credit_invalid(self):
        create_user_request = CreateUserRequest(username="Max00364", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00364", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        body_for_credit = CreditRequest(accountId=account_response.id, amount=5000, termMonths=12)
        credit_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00364", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(body_for_credit)

        repay_request = RepayCreditRequest(creditId=credit_response.creditId, accountId=credit_response.id,
                                           amount=5000.1)
        RepayCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00364", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(repay_request)