import json

from client import get_client


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    email = message["pathParameters"]["email"]

    client = get_client(user_id, email)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(client)}
