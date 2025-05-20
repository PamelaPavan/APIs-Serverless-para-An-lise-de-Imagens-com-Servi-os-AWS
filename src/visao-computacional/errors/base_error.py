from typing import Optional

class CustomError(Exception):
    """
    Base error class for custom status code and message.
    
    :param message (str): The error message.
    :param status_code (int): The HTTP status code.
    :param error_details (Optional[str]): Additional details about the error.
    """
    def __init__(self, message: str, status_code: int, error_details: Optional[str]=None):
        self.message = message
        self.status_code = status_code
        self.error_details = error_details
    
    def __str__(self) -> str:
        return f"{self.status_code}: {self.message} - {self.error_details if self.error_details else ''}"


class BadRequestError(CustomError):
    """
    Represents a bad request error with status code 500 (400).
    """
    def __init__(self, message: str, error_details: Optional[str]=None):
        super().__init__(message, 500, error_details)