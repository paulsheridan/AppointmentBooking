import boto3
import os
import json
from boto3.dynamodb.conditions import Key

from user import User, get_user


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["pathParameters"]["user_id"]
    user = get_user(user_id)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(user)}
