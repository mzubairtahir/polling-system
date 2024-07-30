"""This module contains some common classes that can be used across our project"""


class ResponseData:
    """Class for standard response format"""

    def __init__(self, success=True, message=None, data=None, errors=None) -> None:
        """
        Args:
            success (bool, optional): Success of request. Defaults to True.
            message (_type_, optional): Any message you want to pass to client. Defaults to None.
            data (_type_, optional): Any data you want to pass to client. Defaults to None.
            errors (_type_, optional): Any form errors you want to pass to client. Defaults to None.
        """
        self.success = success
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self):
        data = {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors
        }
        return data


class ServiceError(Exception):
    """Custom exception that can be raised in Serivce classes"""

    def __init__(self, data: ResponseData, status_code=200) -> None:
        """
        Args:
            data (ResponseData): data that you want to return to client
            status_code (_type_, optional): status code of response. Defaults to None.
        """
        self.message = "This error is generated in a service"
        self.data = data
        self.status_code = status_code
