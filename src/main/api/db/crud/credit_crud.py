import allure
from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit(db: Session, id: int) -> Credit | None:
        answer = db.query(Credit).filter_by(id=id).first()
        with allure.step(f"DB: SELECT * FROM credit WHERE id={id}"):
            allure.attach(
                body=str(answer),
                name="DB result",
                attachment_type=allure.attachment_type.TEXT
            )
        return answer
