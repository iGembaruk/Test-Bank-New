import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_simple_user_request):
        response = api_manager.user_steps.create_account(create_simple_user_request)
        assert response.balance == 0