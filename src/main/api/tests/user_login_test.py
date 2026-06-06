import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_admin = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_admin)

        assert response.user.username == login_admin.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)
        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role
