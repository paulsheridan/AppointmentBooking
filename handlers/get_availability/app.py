import json

from availability import get_availability


def lambda_handler(message, context):
    user_id = message["pathParameters"]["artist"]
    service_id = message["queryStringParameters"]["service"]
    month = message["queryStringParameters"]["month"]

    available = get_availability(user_id, service_id, month)
    print(available)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(available),
    }
