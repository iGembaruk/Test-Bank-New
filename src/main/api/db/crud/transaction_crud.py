from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction



class TransactionCrudDb:
    @staticmethod
    def get_transaction(db: Session, id_account: int) -> Transaction | None:
        return db.query(Transaction).filter_by(id=id_account).first()