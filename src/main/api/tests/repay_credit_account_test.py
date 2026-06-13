from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRoleCreditRequest
from src.main.api.models.credit_response import CreditResponse


class TestRepayCreditAccount:
    def test_repay_credit_valid(self, db_session: Session,
                                api_manager: ApiManager,
                                create_user_role_credit_request: CreateUserRoleCreditRequest,
                                create_account_request_for_credit: CreateAccountResponse,
                                create_credit_response: CreditResponse
                                ):
        repay_response = api_manager.user_steps.repay_credit(create_credit_response, create_user_role_credit_request)
        assert repay_response.amountDeposited == create_credit_response.amount
        db_data = TransactionCrudDb.get_last_transaction_by_credit_id(db_session, repay_response.creditId)
        assert db_data.amount == repay_response.amountDeposited, 'amount should be equals'

    def test_repay_credit_invalid(self, db_session: Session,
                                api_manager: ApiManager,
                                create_user_role_credit_request: CreateUserRoleCreditRequest,
                                create_account_request_for_credit: CreateAccountResponse,
                                create_credit_response: CreditResponse
                                ):
        repay_response = api_manager.user_steps.repay_credit_invalid(create_credit_response, create_user_role_credit_request)
        assert "The amount is not enough" in repay_response.error

        db_data = CreditCrudDb.get_credit(db_session, create_credit_response.creditId)
        assert db_data.amount == create_credit_response.amount
