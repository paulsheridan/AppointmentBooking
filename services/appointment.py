from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class Appointment(Item):

    def __init__(
        self,
        client_email,
        user_id,
        start_datetime,
        end_datetime,
        confirmed=False,
        canceled=False,
    ):
        self.client_email = client_email
        self.user_id = user_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.confirmed = confirmed
        self.canceled = canceled

    @classmethod
    def from_item(cls, item):
        return cls(
            item["client_email"],
            item["user_id"],
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
            "client_email": self.client_email,
            "user_id": self.user_id,
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
    user_id_key = f"USER#{user_id}"
    start_datetime_key = f"APPT#{start_datetime}"

    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key)
        & Key("SK").eq(start_datetime_key)
    )
    return Appointment(**response["Item"])


def confirm_appointment(user_id, start_datetime):
    user_id_key = f"USER#{user_id}"
    start_datetime_key = f"APPT#{start_datetime}"

    table = get_dynamodb_table()
    response = table.update_item(
        KeyConditionExpression=Key("PK").eq(user_id_key)
        & Key("SK").eq(start_datetime_key),
        UpdateExpression="SET Confirmed=:confirmed, Canceled=:canceled",
        ExpressionAttributeValues={":confirmed": True, ":canceled": False},
        ReturnValues="UPDATED_NEW",
    )
    return response


def cancel_appointment(user_id, start_datetime):
    user_id_key = f"USER#{user_id}"
    start_datetime_key = f"APPT#{start_datetime}"

    table = get_dynamodb_table()
    response = table.update_item(
        KeyConditionExpression=Key("PK").eq(user_id_key)
        & Key("SK").eq(start_datetime_key),
        UpdateExpression="SET Confirmed=:confirmed, Canceled=:canceled",
        ExpressionAttributeValues={":confirmed": False, ":canceled": True},
        ReturnValues="UPDATED_NEW",
    )
    return response
