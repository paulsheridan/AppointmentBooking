import boto3
import os
import json

from boto3.dynamodb.conditions import Key
from datetime import datetime

from item import Item


class Appointment(Item):
    def __init__(self, email, start_datetime, end_datetime):
        self.email = email
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    @classmethod
    def from_item(cls, item):
        return cls(
            item["email"],
            item["start_datetime"],
            item["end_datetime"]
        )

    def get_pk(self):
        return f"CLIENT#{self.email}"

    def get_sk(self):
        return f"APPT#{self.start_datetime}"

    def to_item(self):
        return {
            **self.keys(),
            "email": self.email,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
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

    table.put_item(TableName=table_name, Item=appointment.to_item())
    return appointment


def get_client(email, start_datetime):
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
