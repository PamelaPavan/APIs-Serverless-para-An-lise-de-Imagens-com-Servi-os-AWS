import json
from typing import Any
from errors import JSONDecodeError

def parse_body(body: str) -> Any:
    """
    Attempts to decode a JSON string and raises an error if the JSON is invalid.

    :param body: JSON string to decode.
    :return: Decoded JSON object.
    :raises JSONDecodeError: If the JSON string is invalid.
    """
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise JSONDecodeError("Invalid JSON")