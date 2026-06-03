import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_admin_request)

        assert login_admin_response.user.username == login_admin_request.username
        assert login_admin_response.user.role == "ROLE_ADMIN"

    def test_login_user(self):
        create_user_request = CreateUserRequest(username="Max00351", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username="Max00351", password="Pas!sw0rd")
        login_user_response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_response.user.username == login_user_request.username
        assert login_user_response.user.role == create_user_request.role
