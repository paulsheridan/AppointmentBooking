import json

from service import get_service


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    service_id = message["pathParameters"]["service_id"]

    service = get_service(user_id, service_id)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(service.model_dump(exclude={"user_id"})),
    }
