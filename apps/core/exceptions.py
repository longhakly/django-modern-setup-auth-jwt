from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        self.detail = {
            "error": message,
            "error_code": self.status_code,
        }


class BaseCustomException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred."

    def __init__(self, message=None, status=None):
        self.detail = {
            "error": message or self.default_detail,
            "error_code": status or self.status_code,
        }
        self.status_code = status or self.status_code
