import json
from typing import Optional
from xml.etree.ElementTree import indent

import allure
import requests
from pydantic import BaseModel
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel], log: bool = True) -> Response:
        body = model.model_dump() if model else None
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )
        if log:
            with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
                body = json.dumps(model.model_dump(), indent=2, ensure_ascii=False) if model else {}
                allure.attach(body, "Request", allure.attachment_type.JSON)
                allure.attach(json.dumps(response.json(), indent=2, ensure_ascii=False), "Response Error",
                              allure.attachment_type.JSON)

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec,
        )
        allure.step(f"DELETE user{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}")
        self.response_spec(response)
        return response
