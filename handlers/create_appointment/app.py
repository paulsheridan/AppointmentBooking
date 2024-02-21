import json

from appointment import Appointment, create_appointment


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    request_data = json.loads(message["body"])
    appointment = Appointment(**request_data)

    create_appointment(appointment)

    return {"statusCode": 201, "headers": {}, "body": json.dumps(appointment.__dict__)}
