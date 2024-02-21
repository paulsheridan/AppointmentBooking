import json

from client import Client, create_client


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    request_data = json.loads(message["body"])
    client = Client(**request_data)

    create_client(client)

    return {"statusCode": 201, "headers": {}, "body": json.dumps(client.__dict__)}
