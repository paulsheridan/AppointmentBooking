import json

from user import get_user


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]

    users = get_user(user_id)
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(
            [user.model_dump(exclude={"user_id"}) for user in users]
        ),
    }
