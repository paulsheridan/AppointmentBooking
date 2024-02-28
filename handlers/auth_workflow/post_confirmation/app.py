from datetime import datetime

from user import User, create_or_update_user


def lambda_handler(message, context):

    request = message["request"]["userAttributes"]

    user = User(
        request["sub"],
        request["nickname"],
        request["email"],
        datetime.utcnow().isoformat(),
        [],
    )
    create_or_update_user(user)

    return message
