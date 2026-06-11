import random

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateSimpleUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest


class TestTransfer:
    def test_transfer_valid(self, db_session: Session, create_simple_user_request: CreateSimpleUserRequest,
                            api_manager: ApiManager):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)

        deposit_body = DepositRequest(accountId=create_account_response.id,
                                      amount=round(random.uniform(1000.0, 2000.0), 2))
        replenishment_deposit_response = api_manager.user_steps.deposit(
            deposit_request=deposit_body,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        create_account_two_response = api_manager.user_steps.create_account(create_simple_user_request)

        transfer_request = TransferAccountRequest(fromAccountId=replenishment_deposit_response.id,
                                                  toAccountId=create_account_two_response.id,
                                                  amount=round(random.uniform(500, 1000), 2))
        transfer_response = api_manager.user_steps.transfer(
            transfer_request=transfer_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        assert transfer_response.fromAccountIdBalance == deposit_body.amount - transfer_request.amount
        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, transfer_response.toAccountId)
        assert db_data is not None

    def test_transfer_invalid(self, db_session: Session, create_simple_user_request: CreateSimpleUserRequest,
                              api_manager: ApiManager):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)

        deposit_body = DepositRequest(accountId=create_account_response.id,
                                      amount=round(random.uniform(1000.0, 2000.0), 2))
        replenishment_deposit_response = api_manager.user_steps.deposit(
            deposit_request=deposit_body,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        create_account_two_response = api_manager.user_steps.create_account(create_simple_user_request)

        transfer_request = TransferAccountRequest(fromAccountId=replenishment_deposit_response.id,
                                                  toAccountId=create_account_two_response.id,
                                                  amount=round(random.uniform(2001, 3000), 2))
        api_manager.user_steps.transfer_invalid(
            transfer_request=transfer_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )

        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, transfer_request.toAccountId)
        assert db_data is None
