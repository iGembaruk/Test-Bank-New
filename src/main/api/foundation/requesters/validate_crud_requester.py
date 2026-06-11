from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
import allure
import json


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model = model, log=False)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            if model:
                allure.attach(
                    body=json.dumps(model.model_dump(), indent=2, ensure_ascii=False),
                    name=f"Request model: {model.__class__.__name__}",
                    attachment_type=allure.attachment_type.JSON
                )
            else:
                allure.attach(
                    body="",
                    name="Request: empty",
                    attachment_type=allure.attachment_type.TEXT
                )
            allure.attach(
                body=json.dumps(response.json(), indent=2, ensure_ascii=False),
                name=(
                    f"Response model: {self.endpoint.value.response_model.__name__}, status_code={response.status_code}"),
                attachment_type=allure.attachment_type.JSON
            )
            self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        with allure.step(f"DELETE {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"):
            allure.attach(
                body=response.json(),
                name=f"Response",
                attachment_type=allure.attachment_type.JSON
            )
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
