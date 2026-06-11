import random

import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager, create_simple_user_request):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)
        replenishment_deposit_request = DepositRequest(accountId=create_account_response.id,
                                                       amount=random.uniform(1000, 2000))
        replenishment_deposit_response = api_manager.user_steps.deposit(
            deposit_request=replenishment_deposit_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        assert replenishment_deposit_response.balance == replenishment_deposit_request.amount
        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, replenishment_deposit_response.id)
        assert int(db_data.amount) == int(replenishment_deposit_request.amount)

    def test_deposit_account_invalid(self, db_session, api_manager, create_simple_user_request):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)
        replenishment_deposit_request = DepositRequest(accountId=create_account_response.id)

        api_manager.user_steps.deposit_invalid(
            deposit_request=replenishment_deposit_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        db_data = TransactionCrudDb.get_last_transaction_by_account_id(db_session, replenishment_deposit_request.accountId)
        assert db_data is None
