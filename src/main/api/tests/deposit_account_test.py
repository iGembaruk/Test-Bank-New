import random

import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self,db_session: Session, api_manager, create_simple_user_request):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)
        replenishment_deposit_request = DepositRequest(accountId=create_account_response.id,
                                                       amount=random.uniform(1000, 2000))
        replenishment_deposit_response = api_manager.user_steps.deposit(
            deposit_request=replenishment_deposit_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
        assert replenishment_deposit_response.balance == replenishment_deposit_request.amount

    def test_deposit_account_invalid(self, api_manager, create_simple_user_request):
        create_account_response = api_manager.user_steps.create_account(create_simple_user_request)
        replenishment_deposit_request = DepositRequest(accountId=create_account_response.id)

        api_manager.user_steps.deposit_invalid(
            deposit_request=replenishment_deposit_request,
            username=create_simple_user_request.username,
            password=create_simple_user_request.password
        )
