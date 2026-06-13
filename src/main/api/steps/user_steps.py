from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRoleCreditRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.error_message_response import ErrorMessageResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account_request(self, user):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(user.username,
                                                   user.password),
            endpoint=Endpoint.USER_CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_create()
        ).post()
        return response

    def receive_credit(self, account_id: int, user: CreateUserRoleCreditRequest):
        credit_request = CreditRequest(accountId=account_id)
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username,
                                                   password=user.password),
            endpoint=Endpoint.CREDIT_FOR_ACCOUNT,
            response_spec=ResponseSpecs.request_create()
        ).post(credit_request)
        return response

    def recieve_error_credit(self, account_id: int, user):
        credit_request = CreditRequest(accountId=account_id)
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username,
                                                   password=user.password),
            endpoint=Endpoint.CREDIT_FOR_ACCOUNT,
            response_spec=ResponseSpecs.request_bad()
        ).post(credit_request)
        return ErrorMessageResponse(**response.json())

    def deposit(self, account_id: int, user):
        deposit_request = DepositRequest(accountId=account_id)
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_invalid(self, account_id: int, user):
        deposit_request = DepositRequest(accountId=account_id)
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.DEPOSIT,
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_request)
        return ErrorMessageResponse(**response.json())

    def repay_credit(self, credit_response: CreditResponse, user: CreateUserRoleCreditRequest):
        repay_request = RepayCreditRequest(
            accountId=credit_response.id,
            amount=credit_response.amount,
            creditId=credit_response.creditId
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_request)
        return response

    def repay_credit_invalid(self, credit_response: CreditResponse, user: CreateUserRoleCreditRequest):
        repay_request = RepayCreditRequest(
            accountId=credit_response.id,
            amount=credit_response.amount - 100,
            creditId=credit_response.creditId
        )
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.REPAY_CREDIT,
            response_spec=ResponseSpecs.request_bad()
        ).post(repay_request)
        return ErrorMessageResponse(**response.json())

    def transfer(self, deposit_response: DepositResponse, to_account_id: int, user):
        transfer_request = TransferAccountRequest(
            fromAccountId=deposit_response.id,
            toAccountId=to_account_id,
            amount=deposit_response.balance
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.TRANSFER,
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, deposit_response: DepositResponse, to_account_id: int, user):
        transfer_request = TransferAccountRequest(
            fromAccountId=deposit_response.id,
            toAccountId=to_account_id,
            amount=deposit_response.balance + 100
        )
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=user.username, password=user.password),
            endpoint=Endpoint.TRANSFER,
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)
        return ErrorMessageResponse(**response.json())
