import json
from errors import BadRequestError, InternalServerError
from handlers import handle_bad_request, handle_internal_server_error

def v1_description(event, context):
    try:
        body = {
            "message": "VISION api version 1."
        }

        response = {"statusCode": 200, "body": json.dumps(body)}

    except BadRequestError as e:
        response = handle_bad_request(e.message, e.error_details)

    except InternalServerError as e:
        response = handle_internal_server_error(e.message, e.error_details)

    except Exception as e:
        response = handle_internal_server_error(str(e), repr(e))

    return response