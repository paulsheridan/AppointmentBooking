import json

from appointment import Appointment, create_or_update_appointment
from client import Client, create_or_update_client


def lambda_handler(message, context):
    # TODO: get availability and verify that the time slot is open
    # TODO: if it's available, remove the time slot that has been requested, then continue

    request_data = json.loads(message["body"])

    client = Client(
        user_id = request_data["user_id"],
        email = request_data["client_email"],
        name = request_data["name"],
        pronouns = request_data["pronouns"],
        over_18 = request_data["over_18"],
        preferred_contact = request_data["preferred_contact"],
        phone_number = request_data["phone_number"],
    )

    appointment = Appointment(
        user_id = request_data["user_id"],
        client_email = request_data["client_email"],
        start_datetime = request_data["start_datetime"],
        end_datetime = request_data["end_datetime"],
        confirmed = False,
        canceled = False,
    )

    create_or_update_client(client)
    create_or_update_appointment(appointment)

    response_data = {
        "appointment": appointment.model_dump(exclude={"user_id"}),
        "client": client.model_dump(exclude={"user_id"}),
    }
    return {"statusCode": 201, "headers": {}, "body": json.dumps(response_data)}
