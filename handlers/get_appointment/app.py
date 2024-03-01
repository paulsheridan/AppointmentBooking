import json

from appointment import get_appointment


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    start = message["pathParameters"]["id"]

    appointments = get_appointment(user_id, start)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps([appointment.__dict__ for appointment in appointments]),
    }
