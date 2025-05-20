import json
from typing import Optional, Dict

def create_response(message: str, status_code: int, error: Optional[str]=None) -> Dict[str, str]:
    """
    Creates a formatted response with a message, status code, and optionally an error.
    
    :param message (str): The response message.
    :param status_code (int): The HTTP status code.
    :param error (Optional[str]): Optional error message.
    
    
    :return Dict[str, str]: The formatted response dictionary.
    """
    response_body = {"message": message}
    if error:
        response_body["error"] = error
    return {"statusCode": status_code, "body": json.dumps(response_body)}