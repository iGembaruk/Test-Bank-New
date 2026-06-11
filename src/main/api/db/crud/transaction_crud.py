import allure
from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_last_transaction_by_account_id(db: Session, id_account: int) -> Transaction | None:
        answer = db.query(Transaction).filter_by(to_account_id=id_account).order_by(Transaction.created_at).first()
        with allure.step(f"SELECT * FROM transaction WHERE to_account_id={id_account} ORDER BY created_at LIMIT 1"):
            allure.attach(
                body=str(answer),
                name="answer database:",
                attachment_type=allure.attachment_type.TEXT
            )
            return answer
    @staticmethod
    def get_last_transaction_by_credit_id(db: Session, credit_id:int) -> Transaction | None:
        answer = db.query(Transaction).filter_by(credit_id=credit_id).order_by(Transaction.created_at).first()
        with allure.step(f"SELECT * FROM transaction WHERE credit_id={credit_id} ORDER BY created_at LIMIT 1"):
            allure.attach(
                body=str(answer),
                name="answer database:",
                attachment_type=allure.attachment_type.TEXT
            )
            return answer
