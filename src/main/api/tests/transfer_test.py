import random

from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest


class TestTransfer:
    def test_transfer_valid(self, create_simple_user_request, api_manager):
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

    def test_transfer_invalid(self, create_simple_user_request, api_manager):
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
