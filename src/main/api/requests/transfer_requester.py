import requests
from requests import Response

from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_account_request: TransferAccountRequest) -> TransferAccountResponse | Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == 200:
            return TransferAccountResponse(**response.json())
        return response
