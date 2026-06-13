import random

from src.main.api.models.base_model import BaseModel


class CreditRequest(BaseModel):
    accountId: int
    amount: float = round(random.uniform(5000, 15000), 2)
    termMonths: int = random.randint(1, 12)