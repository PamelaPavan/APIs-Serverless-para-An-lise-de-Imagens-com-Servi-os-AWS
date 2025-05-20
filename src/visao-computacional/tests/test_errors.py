from errors import CustomError, BadRequestError, JSONDecodeError, InvalidRequestBodyError,  InternalServerError

def test_custom_error():
    error = CustomError("Error message", 418)
    assert error.message == "Error message"
    assert error.status_code != 500
    assert error.error_details is None
    assert str(error) == "418: Error message - "

def test_bad_request_error():
    error = BadRequestError("Bad request")
    assert error.message == "Bad request"
    assert error.status_code == 500
    assert error.error_details is None
    assert str(error) == "500: Bad request - "

def test_json_decode_error():
    error = JSONDecodeError()
    assert error.message == "Invalid JSON format"
    assert error.status_code == 500
    assert error.error_details is None
    assert str(error) == "500: Invalid JSON format - "

def test_invalid_request_body_error():
    error = InvalidRequestBodyError()
    assert error.message == "Invalid request body"
    assert error.status_code == 500
    assert error.error_details is None
    assert str(error) == "500: Invalid request body - "

def test_internal_server_error():
    error = InternalServerError()
    assert error.message == "Internal server error"
    assert error.status_code == 500
    assert error.error_details is None
    assert str(error) == "500: Internal server error - "