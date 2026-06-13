from src.main.api.models.base_model import BaseModel


class ErrorMessageResponse(BaseModel):
    error: str