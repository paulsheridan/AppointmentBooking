import boto3
import os
import json


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "PUT":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    table_name = os.environ.get("TABLE", "Appointments")
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        appointments_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        appointments_table = boto3.resource("dynamodb", region_name=region)

    table = appointments_table.Table(table_name)
    appointment = json.loads(message["body"])

    params = {"id": appointment["id"], "date": appointment["date"]}

    response = table.update_item(
        Key=params,
        UpdateExpression="set stage = :s, description = :d",
        ExpressionAttributeValues={
            ":s": appointment["stage"],
            ":d": appointment["description"],
        },
        ReturnValues="UPDATED_NEW",
    )
    print(response)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"msg": "Appointment updated"}),
    }
