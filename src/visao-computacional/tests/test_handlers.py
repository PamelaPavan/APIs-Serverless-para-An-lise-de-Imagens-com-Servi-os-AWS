from handlers import create_response, handle_bad_request, handle_internal_server_error

def test_create_response():
    response = create_response("Success", 200)
    assert response["statusCode"] == 200
    assert response["body"] == '{"message": "Success"}'

    response = create_response("Error", 500, "Invalid input")
    assert response["statusCode"] == 500
    assert response["body"] == '{"message": "Error", "error": "Invalid input"}'

def test_handle_bad_request():
    response = handle_bad_request("Bad request")
    assert response["statusCode"] == 500
    assert response["body"] == '{"message": "Bad request"}'

    response = handle_bad_request("Bad request", "Missing field")
    assert response["statusCode"] == 500
    assert response["body"] == '{"message": "Bad request", "error": "Missing field"}'

def test_handle_internal_server_error():
    response = handle_internal_server_error("An unexpected error occurred")
    assert response["statusCode"] == 500
    assert response["body"] == '{"message": "An unexpected error occurred"}'

    response = handle_internal_server_error("An unexpected error occurred", "Database down")
    assert response["statusCode"] == 500
    assert response["body"] == '{"message": "An unexpected error occurred", "error": "Database down"}'