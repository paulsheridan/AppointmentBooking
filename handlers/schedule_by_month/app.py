import json

from appointment import list_schedule


def lambda_handler(message, context):

    if "httpMethod" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    month = message["pathParameters"]["month"]

    start = f"{month}-00"
    end = f"{month}-31"

    appointments = list_schedule(user_id, start, end)

    print("appointments")
    print(appointments)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps([appointment.__dict__ for appointment in appointments]),
    }
