import json

from client import Client, create_client, list_clients


def lambda_handler(message, context):

    if "httpMethod" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    clients = list_clients()
    return {"statusCode": 200, "headers": {}, "body": json.dumps([client.toJSON() for client in clients])}
