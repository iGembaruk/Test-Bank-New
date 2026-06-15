import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRoleCreditRequest


@pytest.mark.api
class TestCreditAccountUser:
    def test_credit_account_user_valid(self,
                                       db_session: Session,
                                       api_manager: ApiManager,
                                       create_user_role_credit_request: CreateUserRoleCreditRequest,
                                       create_account_request_for_credit: CreateAccountResponse,
                                       ):
        credit_response = api_manager.user_steps.receive_credit(create_account_request_for_credit.id,
                                                                create_user_role_credit_request)

        db_result = CreditCrudDb.get_credit(db_session, credit_response.creditId)
        assert credit_response.id == db_result.account_id, 'in db and api no equals id operation'

    def test_credit_account_user_invalid(self,
                                         db_session: Session,
                                         api_manager: ApiManager,
                                         create_user_role_credit_request: CreateUserRoleCreditRequest,
                                         create_account_request_for_credit: CreateAccountResponse,
                                         ):
        credit_response_success = api_manager.user_steps.receive_credit(create_account_request_for_credit.id,
                                                                        create_user_role_credit_request)

        db_success = TransactionCrudDb.get_last_transaction_by_account_id(db_session, credit_response_success.id)

        credit_response_error = api_manager.user_steps.recieve_error_credit(create_account_request_for_credit.id,
                                                                            create_user_role_credit_request)

        assert credit_response_error.error == "Only one active credit allowed per user"

        db_repeat = TransactionCrudDb.get_last_transaction_by_account_id(db_session, credit_response_success.id)
        assert db_success.id == db_repeat.id, 'last transaction should be in success request'
