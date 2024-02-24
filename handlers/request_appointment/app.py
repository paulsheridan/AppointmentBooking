import json

from appointment import Appointment, create_unconfirmed_appointment
from client import Client, create_or_update_client


def lambda_handler(message, context):

    if "body" not in message or message["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"msg": "Bad Request"}),
        }

    # TODO: get availability and verify that the time slot is open
    # TODO: if it's available, remove the time slot that has been requested, then continue o

    appointment_data = json.loads(message["body"]["appointment"])
    client_data = json.loads(message["body"]["client"])
    appointment = Appointment(**appointment_data)
    client = Client(**client_data)

    create_or_update_client(client)
    create_unconfirmed_appointment(appointment)

    # TODO: Return the client as well
    return {"statusCode": 201, "headers": {}, "body": json.dumps(appointment.__dict__)}
