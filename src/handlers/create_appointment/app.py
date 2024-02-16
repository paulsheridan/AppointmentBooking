import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")

    if aws_environment == "AWS_SAM_LOCAL":
        appointments_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        appointments_table = boto3.resource("dynamodb", region_name=region)

    table = appointments_table.Table("Appointments")
    appointment = json.loads(message["body"])

    params = {
        "pk": appointment["email"],
        "sk": appointment["startDateTime"],
        "createdAt": str(datetime.timestamp(datetime.now())),
        "description": appointment["description"],
    }

    response = table.put_item(TableName="Appointments", Item=params)
    print(response)

    return {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps({"msg": "Appointment created"}),
    }
