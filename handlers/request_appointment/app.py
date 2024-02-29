import json

from appointment import Appointment, create_unconfirmed_appointment
from client import Client, create_or_update_client


def lambda_handler(message, context):
    # TODO: get availability and verify that the time slot is open
    # TODO: if it's available, remove the time slot that has been requested, then continue

    request_data = json.loads(message["body"])

    client = Client(
        request_data["user_id"],
        request_data["client_email"],
        request_data["name"],
        request_data["pronouns"],
        request_data["over_18"],
        request_data["preferred_contact"],
        request_data["phone_number"],
    )

    appointment = Appointment(
        request_data["user_id"],
        request_data["client_email"],
        request_data["start_datetime"],
        request_data["end_datetime"],
    )

    create_or_update_client(client)
    create_unconfirmed_appointment(appointment)

    response_data = {
        "appointment": appointment.__dict__,
        "client": client.__dict__,
    }
    return {"statusCode": 201, "headers": {}, "body": json.dumps(response_data)}
