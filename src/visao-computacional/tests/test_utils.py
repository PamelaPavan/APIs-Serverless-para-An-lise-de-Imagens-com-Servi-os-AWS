import pytest
from datetime import datetime
from utils import categorize_labels, parse_body, v1_response
from errors import JSONDecodeError

def test_categorize_labels():
    labels = [
        {"name": "Face", "confidence": 95, "parents": []},
        {"name": "Animal", "confidence": 85, "parents": [{"Name": "Pet"}]},
        {"name": "Dog", "confidence": 65, "parents": [{"Name": "Pet"}]},
        {"name": "Cat", "confidence": 55, "parents": [{"Name": "Pet"}]},
    ]
    
    pet_labels, prompt, face_detected = categorize_labels(labels)
    
    assert face_detected is True
    assert len(pet_labels) == 2
    assert pet_labels[0]["Name"] == "Animal"
    assert pet_labels[1]["Name"] == "Dog"
    assert prompt == "Animal Dog "

def test_parse_body_valid_json():
    body = '{"key": "value"}'
    result = parse_body(body)
    assert result == {"key": "value"}

def test_parse_body_invalid_json():
    body = '{"key": "value"'
    with pytest.raises(JSONDecodeError, match="Invalid JSON"):
        parse_body(body)

def test_v1_response_with_datetime():
    original_response = []
    url_to_image = "http://example.com/image.jpg"
    created_image = datetime(2023, 8, 1, 12, 0, 0)
    
    result = v1_response(original_response, url_to_image, created_image)
    
    assert result["url_to_image"] == url_to_image
    assert result["created_image"] == "01-08-2023 12:00:00"
    assert len(result["faces"]) == 1
    assert result["faces"][0]["position"]["Height"] is None

def test_v1_response_with_invalid_date_format():
    original_response = []
    url_to_image = "http://example.com/image.jpg"
    created_image = "invalid-date-format"
    
    result = v1_response(original_response, url_to_image, created_image)
    
    assert result["created_image"] == "Invalid date format"

def test_v1_response_with_faces():
    original_response = [
        {
            "bounding_box": {
                "Height": 0.1,
                "Left": 0.1,
                "Top": 0.1,
                "Width": 0.1
            },
            "emotion": {
                "type": "HAPPY",
                "confidence": 99.0
            }
        }
    ]
    url_to_image = "http://example.com/image.jpg"
    created_image = datetime(2023, 8, 1, 12, 0, 0)
    
    result = v1_response(original_response, url_to_image, created_image)
    
    assert result["faces"][0]["position"]["Height"] == 0.1
    assert result["faces"][0]["classified_emotion"] == "HAPPY"