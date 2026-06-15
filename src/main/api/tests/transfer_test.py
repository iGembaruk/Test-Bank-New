import random

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserDefaultRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest


class TestTransfer:
    def test_transfer_valid(self, db_session: Session,
                            api_manager: ApiManager,
                            create_user_role_credit_request: CreateUserDefaultRequest,
                            create_account_request_for_credit: CreateAccountResponse,
                            create_deposit_response: DepositRequest
                            ):
        create_account_two_response = api_manager.user_steps.create_account_request(create_user_role_credit_request)
        transfer_response = api_manager.user_steps.transfer(
            deposit_response=create_deposit_response,
            to_account_id=create_account_two_response.id,
            user=create_user_role_credit_request
        )
        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, transfer_response.toAccountId)
        assert db_data.transaction_type == "transfer"

    def test_transfer_invalid(self, db_session: Session,
                              api_manager: ApiManager,
                              create_user_role_credit_request: CreateUserDefaultRequest,
                              create_account_request_for_credit: CreateAccountResponse,
                              create_deposit_response: DepositResponse
                              ):
        create_account_two_response = api_manager.user_steps.create_account_request(create_user_role_credit_request)
        transfer_response = api_manager.user_steps.transfer_invalid(
            deposit_response=create_deposit_response,
            to_account_id=create_account_two_response.id,
            user=create_user_role_credit_request
        )
        assert transfer_response.error == f"Insufficient funds. Current balance: {create_deposit_response.balance}, required: {create_deposit_response.balance + 100}"

        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, create_account_two_response.id)
        assert db_data is None, "transaction not should be!"
