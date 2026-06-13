import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserDefaultRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session,
                            api_manager: ApiManager,
                            create_user_default_request: CreateUserDefaultRequest):
        response = api_manager.user_steps.create_account_request(create_user_default_request)
        assert response.balance == 0
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Account not found db'
        assert account_from_db.balance is not None, 'account_from_db.balance should be'