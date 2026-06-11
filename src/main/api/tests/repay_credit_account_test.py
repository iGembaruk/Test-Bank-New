import random

from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest


class TestRepayCreditAccount:
    def test_repay_credit_valid(self, api_manager, create_credit_user_request):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)

        body_for_credit = CreditRequest(accountId=account.id, amount=round(random.uniform(5000, 10000), 2),
                                        termMonths=random.randint(1, 12))
        credit_response = api_manager.user_steps.receive_credit(
            credit_request=body_for_credit,
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )

        repay_request = RepayCreditRequest(creditId=credit_response.creditId, accountId=credit_response.id,
                                           amount=body_for_credit.amount)
        repay_response = api_manager.user_steps.repay_credit(
            repay_request=repay_request,
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )
        assert repay_response.amountDeposited == body_for_credit.amount

    def test_repay_credit_invalid(self, api_manager, create_credit_user_request):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)

        body_for_credit = CreditRequest(accountId=account.id, amount=random.uniform(5000, 10000),
                                        termMonths=random.randint(1, 12))
        credit_response = api_manager.user_steps.receive_credit(
            credit_request=body_for_credit,
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )

        repay_request = RepayCreditRequest(creditId=credit_response.creditId, accountId=credit_response.id,
                                           amount=body_for_credit.amount)
        api_manager.user_steps.repay_credit_invalid(
            repay_request=repay_request,
            username=create_credit_user_request.username,
            password=create_credit_user_request.password
        )
