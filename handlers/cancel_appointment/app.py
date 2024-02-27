import json

from appointment import cancel_appointment


def lambda_handler(message, context):
    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    start_datetime = message["pathParameters"]["start_datetime"]

    response = cancel_appointment(user_id, start_datetime)

    return {"statusCode": 201, "headers": {}, "body": json.dumps(response)}
