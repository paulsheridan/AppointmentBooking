import json

from user import get_user


def lambda_handler(message, context):

    if "pathParameters" not in message or message["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    user = get_user(user_id)

    return {"statusCode": 200, "headers": {}, "body": json.dumps(user)}
