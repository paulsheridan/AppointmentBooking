import json

from client import list_clients


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]

    clients = list_clients(user_id)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps([client.__dict__ for client in clients]),
    }
