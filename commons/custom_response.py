from enum import Enum


class CustomResponse:
    def __init__(self, status_code: int | None, msg: str, service: Enum, request_id: int | None = None):
        self.status_code = status_code
        self.msg = msg
        self.service = service
        self.request_id = request_id

    def get_response(self):
        return f"{self.service}: {self.msg} Status code: {self.status_code}"


