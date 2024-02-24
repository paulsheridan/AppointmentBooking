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
    # TODO: Get the user_id from the request auth for use below
    user_id = context["identity"]["cognitoIdentityId"]

    client = get_client(user_id, email)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(client)}
