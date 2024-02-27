import json

from client import list_clients


def lambda_handler(message, context):

    if "httpMethod" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]

    clients = list_clients(user_id)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps([client.toJSON() for client in clients]),
    }
