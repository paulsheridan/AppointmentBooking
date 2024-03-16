import json

from appointment import list_appointments


def lambda_handler(message, context):

    if "httpMethod" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    month = message["pathParameters"]["month"]

    appointments = list_appointments(user_id, f"{month}-00", f"{month}-31")
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps([appointment.model_dump(exclude={"user_id"}) for appointment in appointments]),
    }
