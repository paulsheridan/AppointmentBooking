from pydantic import EmailStr, validator, field_serializer
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class Appointment(Item):
    user_id: UUID
    client_email: EmailStr
    start_datetime: datetime
    end_datetime: datetime
    confirmed: bool = False
    canceled: bool = False

    @field_serializer('user_id')
    def serialize_uuid(self, user_id: UUID):
        return str(user_id)

    @field_serializer('start_datetime', 'end_datetime')
    def serialize_datetime(self, datetime: datetime):
        return datetime.isoformat()

    @classmethod
    def from_item(cls, item):
        return cls(
            item["user_id"],
            item["client_email"],
            item["start_datetime"],
            item["end_datetime"],
            item["confirmed"],
            item["canceled"],
        )

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"APPT#{self.start_datetime}"

    def to_item(self):
        return {
            **self.keys(),
            "user_id": self.user_id,
            "client_email": self.client_email,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "confirmed": self.confirmed,
            "canceled": self.canceled,
            "item_type": "appointment",
        }


def create_unconfirmed_appointment(appointment):
    appointment.confirmed = False
    appointment.canceled = False

    table = get_dynamodb_table()
    table.put_item(Item=appointment.to_item())
    return appointment


def get_appointment(user_id, start_datetime):
    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").eq(f"APPT#{start_datetime}")
    )
    return [Appointment(**item) for item in response["Items"]]


def list_schedule(user_id, start, end):
    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").between(f"APPT#{start}", f"APPT#{end}")
    )
    return [Appointment.from_item(item) for item in response["Items"]]


def patch_appointment_status(user_id, start_datetime, confirmed, canceled):
    table = get_dynamodb_table()
    response = table.update_item(
        Key={"PK": f"USER#{user_id}", "SK": f"APPT#{start_datetime}"},
        UpdateExpression="SET confirmed=:confirmed, canceled=:canceled",
        ExpressionAttributeValues={":confirmed": confirmed, ":canceled": canceled},
        ReturnValues="UPDATED_NEW",
    )
    return response
