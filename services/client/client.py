import boto3
import os
from boto3.dynamodb.conditions import Key

from item import Item

class Client(Item):
    def __init__(
        self,
        email,
        name,
        pronouns,
        over_18,
        preferred_contact,
        phone_number,
    ):
        self.email = email
        self.name = name
        self.pronouns = pronouns
        self.over_18 = over_18
        self.preferred_contact = preferred_contact
        self.phone_number = phone_number

    def get_pk(self):
        return f"CLIENT#{self.email}"

    def get_sk(self):
        return f"CLIENT#{self.email}"

    def to_item(self):
        return {
            **self.keys(),
            "name": self.name,
            "pronouns": self.pronouns,
            "over_18": self.over_18,
            "preferred_contact": self.preferred_contact,
            "phone_number": self.phone_number
        }


def create_client(client):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")

    if aws_environment == "AWS_SAM_LOCAL":
        appointments_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        appointments_table = boto3.resource("dynamodb", region_name=region)

    table = appointments_table.Table("Appointments")

    table.put_item(TableName="Appointments", Item=client.to_item())
    return client

def get_client(email):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")

    if aws_environment == "AWS_SAM_LOCAL":
        appointments_table = boto3.resource(
            "dynamodb", endpoint_url="http://dynamodb:8000"
        )
    else:
        appointments_table = boto3.resource("dynamodb", region_name=region)

    table = appointments_table.Table("Appointments")

    response = table.query(
        KeyConditionExpression=Key("hash_key").eq(email)
        & Key("range_key").eq(email)
    )
    return Client(**response["Item"])
