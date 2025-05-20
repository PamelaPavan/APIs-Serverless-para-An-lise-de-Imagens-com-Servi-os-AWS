from typing import Optional
from .base_error import BadRequestError

class JSONDecodeError(BadRequestError):
    """
    Represents a JSON decoding error.
    """
    def __init__(self, error_details: Optional[str]=None):
        super().__init__("Invalid JSON format", error_details)

class InvalidRequestBodyError(BadRequestError):
    """
    Represents a bad request error.
    """
    def __init__(self, error_details: Optional[str]=None):
        super().__init__("Invalid request body", error_details)