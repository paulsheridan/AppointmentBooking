import boto3
import os
import json
from boto3.dynamodb.conditions import Key

from appointment import Appointment, get_appointment


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    email = message["pathParameters"]["email"]
    start_datetime = message["pathParameters"]["start_datetime"]

    appointment = get_appointment(email, start_datetime)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(appointment)}