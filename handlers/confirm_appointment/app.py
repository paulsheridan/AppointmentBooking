import json

from appointment import patch_appointment_status


def lambda_handler(message, context):
    if "body" not in message or message["httpMethod"] != "PATCH":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    start = message["pathParameters"]["id"]

    response = patch_appointment_status(user_id, start, True, False)

    return {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps(response["Attributes"]),
    }
