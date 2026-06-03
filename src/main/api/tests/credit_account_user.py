from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditAccountUser:
    def test_credit_account_user_valid(self):
        create_user_request = CreateUserRequest(username="Max00360", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00360", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        body_for_credit = CreditRequest(accountId=account_response.id, amount=5000, termMonths=12)
        credit_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00360", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(body_for_credit)

        assert credit_response.amount == 5000
        assert credit_response.termMonths == 12
        assert credit_response.balance == 5000

    def test_credit_account_user_invalid(self):
        create_user_request = CreateUserRequest(username="Max00362", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00362", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        body_for_credit = CreditRequest(accountId=account_response.id, amount=5000, termMonths=12)
        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00362", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(body_for_credit)

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max00362", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(body_for_credit)
