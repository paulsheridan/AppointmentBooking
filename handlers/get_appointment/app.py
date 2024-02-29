import json

from appointment import get_appointment


def lambda_handler(message, context):
    email = message["pathParameters"]["email"]
    start_datetime = message["pathParameters"]["start_datetime"]

    appointment = get_appointment(email, start_datetime)
    return {"statusCode": 200, "headers": {}, "body": json.dumps(appointment)}
