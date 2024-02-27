from user import User, create_user


def lambda_handler(message, context):

    request = message["request"]["userAttributes"]

    user = User(request["sub"], request["email"])
    create_user(user)

    return message
