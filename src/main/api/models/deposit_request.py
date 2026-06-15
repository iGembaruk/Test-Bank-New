import random

from src.main.api.models.base_model import BaseModel


class DepositRequest(BaseModel):
    accountId: int
    amount: float = round(random.uniform(1000.0, 9000.0), 2)
