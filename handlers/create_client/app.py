import json

from client import Client, create_or_update_client


def lambda_handler(message, context):
    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]

    request_data = json.loads(message["body"])

    client = Client(user_id, **request_data)
    create_or_update_client(client)
    return {"statusCode": 201, "headers": {}, "body": json.dumps(client.__dict__)}
