from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateSimpleUserRequest, CreateCreditUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateSimpleUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.USER_CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_create()
        ).post()
        return response

    def create_account_for_credit(self, create_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            endpoint=Endpoint.USER_CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_create()
        ).post()
        return response

    def receive_credit(self, credit_request: CreditRequest, username: str, password: str):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.CREDIT_FOR_ACCOUNT,
            response_spec=ResponseSpecs.request_create()
        ).post(credit_request)
        return response

    def recieve_error_credit(self, credit_request: CreditRequest, username: str, password: str):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.CREDIT_FOR_ACCOUNT,
            response_spec=ResponseSpecs.request_bad()
        ).post(credit_request)
        return response

    def deposit(self, deposit_request: DepositRequest, username: str, password: str):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_invalid(self, deposit_request: DepositRequest, username: str, password: str):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.DEPOSIT,
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_request)

    def repay_credit(self, repay_request: RepayCreditRequest, username: str, password: str):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_request)
        return response

    def repay_credit_invalid(self, repay_request: RepayCreditRequest, username: str, password: str):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_bad()
        ).post(repay_request)

    def transfer(self, transfer_request: TransferAccountRequest, username: str, password: str):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.TRANSFER,
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, transfer_request: TransferAccountRequest, username: str, password: str):
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password=password),
            endpoint=Endpoint.TRANSFER,
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)
