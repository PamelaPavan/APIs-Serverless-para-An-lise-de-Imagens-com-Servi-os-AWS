import json, boto3

from errors import BadRequestError, InternalServerError
from handlers import handle_bad_request, handle_internal_server_error
from rekognition import RekognitionImage
from utils import parse_body, v1_response

def v1_vision(event, context):
    try:    
        body = parse_body(event['body'])
        image = body.get('imageName')
        bucket = body.get('bucket')
        if not image or not bucket:
            raise BadRequestError("Missing 'imageName' or 'bucket' in request body")
        url_to_image = 'https://' + bucket + '/' + image

        object_att = boto3.client('s3').head_object(Bucket=bucket, Key=image)
        last_modified = object_att['LastModified']

        rekognition_client = boto3.client("rekognition")
        # Cria a instancia do Rekognition
        bucket_object = boto3.resource("s3").Object(bucket, image)
        bucket_image = RekognitionImage.from_bucket(bucket_object, rekognition_client)
        # Detecta faces na imagem
        faces = bucket_image.detect_faces()
        # Converte os dados das faces para um dict
        result = [face.to_dict() for face in faces]
        new_response = v1_response(result, url_to_image, last_modified)
        body = new_response
        response = {"statusCode": 200, "body": json.dumps(body)}
   
    except BadRequestError as e:
        response = handle_bad_request(e.message, e.error_details)

    except InternalServerError as e:
        response = handle_internal_server_error(e.message, e.error_details)

    except Exception as e:
        response = handle_internal_server_error(str(e), repr(e))

    return response