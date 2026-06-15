from src.main.api.models.base_model import BaseModel
import random

class TransferAccountRequest(BaseModel):
    fromAccountId:int
    toAccountId:int
    amount: float = round(random.uniform(500, 10000), 2)