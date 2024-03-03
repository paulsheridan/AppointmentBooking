import json

from client import get_client


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    email = message["pathParameters"]["email"]

    clients = get_client(user_id, email)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(
            [client.model_dump(exclude={"user_id"}) for client in clients]
        ),
    }
