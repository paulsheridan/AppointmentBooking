import boto3
import os

from boto3.dynamodb.conditions import Key

from item import Item


class Client(Item):
    def __init__(
        self,
        email,
        user_id,
        name,
        pronouns,
        over_18,
        preferred_contact,
        phone_number,
    ):
        self.email = email
        self.user_id = user_id
        self.name = name
        self.pronouns = pronouns
        self.over_18 = over_18
        self.preferred_contact = preferred_contact
        self.phone_number = phone_number

    @classmethod
    def from_item(cls, item):
        return cls(
            item["email"],
            item["user_id"],
            item["name"],
            item["pronouns"],
            item["over_18"],
            item["preferred_contact"],
            item["phone_number"],
        )

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"CLIENT#{self.email}"

    def to_item(self):
        return {
            **self.keys(),
            "email": self.email,
            "user_id": self.user_id,
            "name": self.name,
            "pronouns": self.pronouns,
            "over_18": self.over_18,
            "preferred_contact": self.preferred_contact,
            "phone_number": self.phone_number,
            "item_type": "client"
        }


def create_client(client):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")
    table_name = os.environ.get("TABLE_NAME", "Appointments")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    table = table_resource.Table(table_name)

    table.put_item(TableName=table_name, Item=client.to_item())
    return client


def get_client(email):
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")
    table_name = os.environ.get("TABLE_NAME", "Appointments")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    table = table_resource.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key("hash_key").eq(email) & Key("range_key").eq(email)
    )
    return Client(**response["Item"])


def list_clients():
    region = os.environ.get("REGION", "us-west-2")
    aws_environment = os.environ.get("AWSENV", "dev")
    table_name = os.environ.get("TABLE_NAME", "Appointments")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    table = table_resource.Table(table_name)

    response = table.query(
        TableName=table_name,
        KeyConditionExpression=Key('sk').begins_with("CLIENT#")
    )
    return [Client.from_item(item) for item in response["Items"]]
