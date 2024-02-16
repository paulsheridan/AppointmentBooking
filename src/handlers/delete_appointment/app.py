import boto3
import os
import json


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "DELETE":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table_name = os.environ.get("TABLE", "Appointments")
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")

    if aws_environment == "AWS_SAM_LOCAL":
        activities_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        activities_table = boto3.resource("dynamodb", region_name=region)

    table = activities_table.Table(table_name)
    appointment_id = message["pathParameters"]["id"]
    appointment_date = message["pathParameters"]["date"]

    params = {"id": appointment_id, "date": appointment_date}

    response = table.delete_item(Key=params)
    print(response)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"msg": "Appointment deleted"}),
    }
