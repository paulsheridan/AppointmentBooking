import boto3
import os
import json
from boto3.dynamodb.conditions import Key

from item import Item


class Appointment(Item):

    def __init__(self, client_email, user_id, start_datetime, end_datetime, approved):
        self.client_email = client_email
        self.user_id = user_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.approved = approved

    @classmethod
    def from_item(cls, item):
        return cls(
            item["client_email"],
            item["user_id"],
            item["start_datetime"],
            item["end_datetime"],
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
            "item_type": "appointment",
        }


def create_appointment(appointment):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")
    table_name = os.environ.get("TABLE_NAME", "Appointments")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    table = table_resource.Table(table_name)

    table.put_item(
        TableName=table_name, Item=appointment.to_item()
    )  # Can the table name be gotten rid of here for the sake of DRYing out the code?
    return appointment


def get_appointment(email, start_datetime):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")
    table_name = os.environ.get("TABLE_NAME", "Appointments")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    table = table_resource.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key("hash_key").eq(email)
        & Key("range_key").eq(start_datetime)
    )
    return Appointment(**response["Item"])
