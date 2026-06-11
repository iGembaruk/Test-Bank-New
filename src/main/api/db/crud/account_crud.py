import allure
from sqlalchemy.orm import Session

from src.main.api.db.models.account_table import Account


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        answer = db.query(Account).filter_by(id=account_id).first()
        with allure.step(f"SELECT * FROM account WHERE id = {account_id} LIMIT 1"):
            allure.attach(
                body=str(answer),
                name="answer to db:",
                attachment_type=allure.attachment_type.TEXT
            )
        return answer

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commit()
