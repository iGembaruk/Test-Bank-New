from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from typing import Optional, Type

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
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
