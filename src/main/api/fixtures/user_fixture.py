import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserDefaultRequest, CreateUserRoleCreditRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_response import DepositResponse


@pytest.fixture
def create_user_default_request(api_manager: ApiManager) -> CreateUserDefaultRequest:
    body = RandomModelGenerator.generate(CreateUserDefaultRequest)
    api_manager.admin_steps.create_user_default(body)
    return body


@pytest.fixture
def create_user_role_credit_request(api_manager: ApiManager) -> CreateUserRoleCreditRequest:
    body = RandomModelGenerator.generate(CreateUserRoleCreditRequest)
    api_manager.admin_steps.create_credit_user(body)
    return body


@pytest.fixture()
def create_account_request_for_credit(api_manager: ApiManager,
                                      create_user_role_credit_request: CreateUserRoleCreditRequest) -> CreateAccountResponse:
    account_response = api_manager.user_steps.create_account_request(create_user_role_credit_request)
    return account_response


@pytest.fixture()
def create_credit_response(api_manager: ApiManager,
                           create_user_role_credit_request: CreateUserRoleCreditRequest,
                           create_account_request_for_credit: CreateAccountResponse
                           ) -> CreditResponse:
    credit_request = CreditRequest(accountId=create_account_request_for_credit.id)
    credit_request.accountId = create_account_request_for_credit.id
    return api_manager.user_steps.receive_credit(create_account_request_for_credit.id, create_user_role_credit_request)


@pytest.fixture()
def create_deposit_response(api_manager: ApiManager,
                            create_account_request_for_credit: CreateAccountResponse,
                            create_user_role_credit_request: CreateUserRoleCreditRequest
                            ) -> DepositResponse:
    return api_manager.user_steps.deposit(create_account_request_for_credit.id, create_user_role_credit_request)
