import random

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.credit_request import CreditRequest


class TestCreditAccountUser:
    def test_credit_account_user_valid(self, db_session: Session, api_manager: ApiManager,
                                       create_credit_user_request: CreateCreditUserRequest):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)
        credit_body = CreditRequest(accountId=account.id, amount=random.uniform(5000.0, 15000),
                                    termMonths=random.randint(1, 12))
        credit_response = api_manager.user_steps.receive_credit(credit_body, create_credit_user_request.username,
                                                                create_credit_user_request.password)

        assert credit_response.termMonths == credit_body.termMonths
        assert credit_response.amount == credit_body.amount
        assert credit_response.balance == credit_body.amount
        credit_from_db = CreditCrudDb.get_credit(db_session, credit_response.creditId)
        assert credit_from_db.account_id == credit_response.id, 'error: credit in db not found with id'

    def test_credit_account_user_invalid(self, db_session: Session, api_manager: ApiManager,
                                         create_credit_user_request: CreateCreditUserRequest):
        account = api_manager.user_steps.create_account_for_credit(create_credit_user_request)
        credit_body = CreditRequest(accountId=account.id, amount=random.uniform(5000.0, 15000),
                                    termMonths=random.randint(1, 12))
        response_valid = api_manager.user_steps.receive_credit(credit_body, create_credit_user_request.username,
                                              create_credit_user_request.password)
        api_manager.user_steps.recieve_error_credit(credit_body, create_credit_user_request.username,
                                                            create_credit_user_request.password)
        db_empty =  CreditCrudDb.get_credit(db_session, response_valid.creditId)
        assert int(db_empty.amount) == int(credit_body.amount)
