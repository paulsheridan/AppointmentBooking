import json

from appointment import patch_appointment_status


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    start = message["pathParameters"]["id"]

    response = patch_appointment_status(user_id, start, True, False)
    return {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps(response["Attributes"]),
    }
