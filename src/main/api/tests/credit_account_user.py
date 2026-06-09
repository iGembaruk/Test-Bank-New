import random

from src.main.api.models.credit_request import CreditRequest


class TestCreditAccountUser:
    def test_credit_account_user_valid(self, api_manager, create_credit_user_request):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)
        credit_body = CreditRequest(accountId=account.id, amount=random.uniform(5000.0, 15000),
                                    termMonths=random.randint(1, 12))
        credit_response = api_manager.user_steps.receive_credit(credit_body, create_credit_user_request.username,
                                                                create_credit_user_request.password)

        assert credit_response.termMonths == credit_body.termMonths
        assert credit_response.amount == credit_body.amount
        assert credit_response.balance == credit_body.amount

    def test_credit_account_user_invalid(self, api_manager, create_credit_user_request):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)
        credit_body = CreditRequest(accountId=account.id, amount=random.uniform(5000.0, 15000),
                                    termMonths=random.randint(1, 12))
        api_manager.user_steps.receive_credit(credit_body, create_credit_user_request.username,
                                              create_credit_user_request.password)
        api_manager.user_steps.recieve_error_credit(credit_body, create_credit_user_request.username,
                                                    create_credit_user_request.password)
