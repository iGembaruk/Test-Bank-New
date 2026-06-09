import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateSimpleUserRequest, CreateCreditUserRequest


@pytest.fixture
def create_simple_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateSimpleUserRequest)
    api_manager.admin_steps.create_simple_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_credit_user(user_request)
    return user_request

