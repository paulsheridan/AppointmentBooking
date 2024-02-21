import boto3
import os
import json
from boto3.dynamodb.conditions import Key

from client import Client, get_client


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    email = message["pathParameters"]["email"]

    client = get_client(email)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(client)}
