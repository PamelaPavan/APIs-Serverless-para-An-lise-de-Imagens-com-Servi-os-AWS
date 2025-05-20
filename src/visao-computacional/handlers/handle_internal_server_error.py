from typing import Optional, Dict
from .create_response import create_response

def handle_internal_server_error(message: str, error_details: Optional[str] = None) -> Dict[str, str]:
    """
    Creates a response for an internal server error with status code 500 and an error message.
    
    :param message (str): The response message.
    :param error_details (Optional[str]): Optional error details.
    
    :return Dict[str, str]: The formatted internal server error response.
    """
    return create_response("An unexpected error occurred", 500, error_details)