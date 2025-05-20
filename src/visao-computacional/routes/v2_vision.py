import boto3, json
from botocore.exceptions import ClientError
from errors import BadRequestError, InternalServerError
from handlers import handle_bad_request, handle_internal_server_error
from rekognition import RekognitionImage
from utils import categorize_labels, format_date, parse_body, prepare_bedrock

def get_faces_from_image(faces):
    faces_info = [face.to_dict() for face in faces]
    transformed_faces = [
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
        for face in faces_info
    ]
    return transformed_faces

def invoke_bedrock_model(prompt):
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt, model_id, request = prepare_bedrock(prompt)
    try:
        response = bedrock_client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        raise InternalServerError(f"Model invocation failed: {e}")

    model_response = json.loads(response["body"].read())
    return model_response["results"][0]["outputText"]

def create_response_body(url_to_image, last_modified_str, pet_labels, response_text, faces=None):
    if faces:
        return {
            "url_to_image": url_to_image,
            "created_image": last_modified_str,
            "faces": faces,
            "pets": [{"labels": pet_labels, "Dicas": response_text}]
        }
    else:
        return {
            "url_to_image": url_to_image,
            "created_image": last_modified_str,
            "pets": [{"labels": pet_labels, "Dicas": response_text}]
        }

def v2_vision(event, context):
    try: 
        body = parse_body(event['body'])
        image = body.get('imageName')
        bucket = body.get('bucket')
        if not image or not bucket:
            raise BadRequestError("Missing 'imageName' or 'bucket' in request body")
        url_to_image = 'https://' + bucket + '/' + image

        object_att = boto3.client('s3').head_object(Bucket=bucket, Key=image)
        last_modified = object_att['LastModified']
        last_modified_str = format_date(last_modified)

        rekognition_client = boto3.client("rekognition")
        
        # Cria a instancia do Rekognition
        bucket_object = boto3.resource("s3").Object(bucket, image)
        bucket_image = RekognitionImage.from_bucket(bucket_object, rekognition_client)

        # Detecta labels na image
        labels = bucket_image.detect_labels(50)
        # Converte RekognitionLabel instances para dicionário
        label_dicts = [label.to_dict() for label in labels]
        pet_labels, prompt, there_is_face = categorize_labels(label_dicts)
        
        if not pet_labels:
            print(f"len check: {len(labels)}")
            response_body = {
                "url_to_image": url_to_image,
                "created_image": last_modified_str,
                "pets": [{"labels": None, "Dicas": None}]
            }
        else:
            faces = get_faces_from_image(bucket_image.detect_faces()) if there_is_face else None
            response_text = invoke_bedrock_model(prompt)
            response_body = create_response_body(url_to_image, last_modified_str, pet_labels, response_text, faces)

        response = {"statusCode": 200, "body": json.dumps(response_body)}
      
    except BadRequestError as e:
        response = handle_bad_request(e.message, e.error_details)

    except InternalServerError as e:
        response = handle_internal_server_error(e.message, e.error_details)

    except Exception as e:
        response = handle_internal_server_error(str(e), repr(e))

    return response