from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserDefaultRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserDefaultRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        url="/auth/token/login",
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    USER_CREATE_ACCOUNT = EndpointConfiguration(
        url="/account/create",
        request_model=None,
        response_model=CreateAccountResponse
    )

    CREDIT_FOR_ACCOUNT = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditRequest,
        response_model=CreditResponse
    )

    DEPOSIT = EndpointConfiguration(
        url="/account/deposit",
        request_model=DepositRequest,
        response_model=DepositResponse,
    )

    REPAY_CREDIT = EndpointConfiguration(
        url="/credit/repay",
        request_model=RepayCreditRequest,
        response_model=RepayCreditResponse,
    )

    TRANSFER = EndpointConfiguration(
        url="/account/transfer",
        request_model=TransferAccountRequest,
        response_model=TransferAccountResponse,
    )
