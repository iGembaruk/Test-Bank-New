import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateSimpleUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_simple_user_request: CreateSimpleUserRequest):
        response = api_manager.user_steps.create_account(create_simple_user_request)
        assert response.balance == 0
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Account not found db'
        assert account_from_db.balance is not None, 'Field balance for created account not found in db'