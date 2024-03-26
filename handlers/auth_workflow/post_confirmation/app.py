import datetime

from user import User, create_or_update_user


def lambda_handler(message, context):
    request = message["request"]["userAttributes"]

    user = User(
        user_id=request["sub"],
        username=request["nickname"],
        email=request["email"],
        date_created=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    create_or_update_user(user)

    return message
