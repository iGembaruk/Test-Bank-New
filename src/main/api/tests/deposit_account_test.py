import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.db.crud.user_crud import UserCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRoleCreditRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session,
                                   api_manager: ApiManager,
                                   create_user_role_credit_request: CreateUserRoleCreditRequest,
                                   create_account_request_for_credit: CreateAccountResponse
                                   ):
        deposit_response = api_manager.user_steps.deposit(create_account_request_for_credit.id,
                                                          create_user_role_credit_request)
        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, deposit_response.id)
        assert db_data.to_account_id == create_account_request_for_credit.id, 'id account no math with id response'

    def test_deposit_account_invalid(self, db_session: Session,
                                     api_manager: ApiManager,
                                     create_user_role_credit_request: CreateUserRoleCreditRequest,
                                     create_account_request_for_credit: CreateAccountResponse
                                     ):
        response = api_manager.user_steps.deposit_invalid(1, create_user_role_credit_request)
        db_user = UserCrudDb.get_user_by_username(db_session, create_user_role_credit_request.username)
        assert f"not found or does not belong to userId {db_user.id}" in response.error
