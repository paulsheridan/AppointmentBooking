import json

from appointment import Appointment, confirm_appointment


def lambda_handler(message, context):
    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    # TODO: Get the user_id from the request auth for use below
    user_id = context["identity"]["cognitoIdentityId"]
    start_datetime = message["pathParameters"]["start_datetime"]

    response = confirm_appointment(user_id, start_datetime)

    return {"statusCode": 201, "headers": {}, "body": json.dumps(response)}
