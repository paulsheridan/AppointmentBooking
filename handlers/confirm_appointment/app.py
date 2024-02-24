import json

from appointment import Appointment, update_appointment


def lambda_handler(message, context):
    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    email = message["pathParameters"]["email"]
    # TODO: Get the user_id from the request auth for use below
    user_id = context["identity"]["cognitoIdentityId"]

    appointment = Appointment(**request_data)

    return {"statusCode": 201, "headers": {}, "body": json.dumps(client.__dict__)}
