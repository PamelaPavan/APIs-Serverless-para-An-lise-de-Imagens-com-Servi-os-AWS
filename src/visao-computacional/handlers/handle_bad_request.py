from typing import Optional, Dict
from .create_response import create_response

def handle_bad_request(message: str, error_details: Optional[str]=None) -> Dict[str, str]:
    """
    Creates a response for a bad request with status code 500 (400).
    
    :param message (str): The response message.
    :param error_details (Optional[str]): Optional error details.
    
    :return Dict[str, str]: The formatted bad request response.
    """
    return create_response(message, 500, error_details)