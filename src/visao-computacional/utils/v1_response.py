from datetime import datetime
from typing import List, Dict, Any, Union

def format_date(date: Union[str, datetime]) -> str:
    """
    Formats a given date string or datetime object into a standard string format.

    :param date: A date string or datetime object.
    :return: Formatted date string.
    """
    if isinstance(date, datetime):
        return date.strftime("%d-%m-%Y %H:%M:%S")
    try:
        dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        return "Invalid date format"

def default_face() -> Dict[str, Any]:
    """
    Creates a default face dictionary with None values for positions and emotions.

    :return: Default face dictionary.
    """
    return {
        "position": {
            "Height": None,
            "Left": None,
            "Top": None,
            "Width": None
        },
        "classified_emotion": None,
        "classified_emotion_confidence": None
    }


def transform_faces(faces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms a list of face dictionaries to the desired format.

    :param faces: List of face dictionaries.
    :return: Transformed list of face dictionaries.
    """
    return [
        {
            "position": {
                "Height": face["bounding_box"]["Height"],
                "Left": face["bounding_box"]["Left"],
                "Top": face["bounding_box"]["Top"],
                "Width": face["bounding_box"]["Width"]
            },
            "classified_emotion": face["emotion"]["type"],
            "classified_emotion_confidence": face["emotion"]["confidence"],
        }
        for face in faces
    ]

def v1_response(original_response: List[Dict[str, Any]], url_to_image: str, created_image: Union[str, datetime]) -> Dict[str, Any]:
    """
    Transforms the original response into the desired format.

    :param original_response: The original response from Rekognition.
    :param url_to_image: URL to the original image.
    :param created_image: URL or datetime of the created/modified image.
    :return: A dictionary in the desired format.
    """
    last_modified_str = format_date(created_image)

    if not original_response:
        return {
            "url_to_image": url_to_image,
            "created_image": last_modified_str,
            "faces": [default_face()]
        }

    return {
        "url_to_image": url_to_image,
        "created_image": last_modified_str,
        "faces": transform_faces(original_response)
    }