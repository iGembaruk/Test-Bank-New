import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserDefaultRequest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_admin = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_admin)

        assert response.user.username == login_admin.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager: ApiManager, create_user_default_request: CreateUserDefaultRequest):
        response = api_manager.admin_steps.login_user(create_user_default_request)
        assert response.user.username == create_user_default_request.username
        assert response.user.role == create_user_default_request.role
