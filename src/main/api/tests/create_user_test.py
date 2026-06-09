import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateSimpleUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_simple_user_request",
        [RandomModelGenerator.generate(CreateSimpleUserRequest)]
    )
    def test_create_user_valid(self, api_manager, create_simple_user_request):
        response = api_manager.admin_steps.create_simple_user(create_simple_user_request)

        assert create_simple_user_request.username == response.username
        assert create_simple_user_request.role == response.role

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Maxx1", "Pas!sw0rд"),
            ("Maxx2", "Pas!sw0"),
            ("Maxx3", "pas!sw0rd"),
            ("Maxx4", "PAS!SWORD"),
            ("Maxx5", "PASSSWORD"),
            ("Maxx5", "PAS!SWRRD"),
        ]
    )
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateSimpleUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)
