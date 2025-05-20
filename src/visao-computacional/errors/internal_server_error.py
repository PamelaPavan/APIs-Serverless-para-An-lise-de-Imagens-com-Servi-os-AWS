from typing import Optional
from .base_error import CustomError

class InternalServerError(CustomError):
    """
    Represents an internal server error with status code 500.
    """
    def __init__(self, error_details: Optional[str]=None):
        super().__init__("Internal server error", 500, error_details)
