from pydantic import EmailStr, validator, field_serializer
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class Appointment(Item):
    user_id: UUID
    client_email: EmailStr
    start: datetime
    end: datetime  # TODO: validate that end is after start and that they're both on the same day
    confirmed: bool = False
    canceled: bool = False  # TODO: validate that these are mutually exclusive

    def pk(self) -> str:
        return f"USER#{self.user_id}"

    def sk(self) -> str:
        return f"APPT#{self.start}"


def create_or_update_appointment(appointment: Appointment) -> Appointment:
    table = get_dynamodb_table()
    # TODO: Make sure there's a legit user attached. I created an appointment with a deleted user
    table.put_item(Item=appointment.to_item())
    return appointment


def get_appointment(user_id: str, start: str) -> Appointment:
    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").eq(f"APPT#{start}")
    )
    return Appointment(**response["Items"][0])


def list_appointments(user_id: str, start: str, end: str) -> list[Appointment]:
    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").between(f"APPT#{start}", f"APPT#{end}")
    )
    return [Appointment(**item) for item in response["Items"]]


def patch_appointment_status(
    user_id: str, start: str, confirmed: bool, canceled: bool
) -> dict:
    table = get_dynamodb_table()
    response = table.update_item(
        Key={"PK": f"USER#{user_id}", "SK": f"APPT#{start}"},
        UpdateExpression="SET confirmed=:confirmed, canceled=:canceled",
        ExpressionAttributeValues={":confirmed": confirmed, ":canceled": canceled},
        ReturnValues="UPDATED_NEW",
    )
    return response
