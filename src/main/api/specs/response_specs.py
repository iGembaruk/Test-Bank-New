from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text

        return confirm

    @staticmethod
    def request_create():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text

        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND, HTTPStatus.UNPROCESSABLE_CONTENT], response.text

        return confirm
