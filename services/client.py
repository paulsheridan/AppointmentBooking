from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


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
            "item_type": "client",
        }


def create_client(client):
    table = get_dynamodb_table()

    table.put_item(Item=client.to_item())
    return client


def get_client(user_id, email):
    table = get_dynamodb_table()

    user_id_key = f"USER#{user_id}"
    email_key = f"CLIENT#{email}"

    response = table.query(
        KeyConditionExpression=Key("hash_key").eq(user_id_key)
        & Key("range_key").eq(email_key)
    )
    return Client(**response["Item"])


def list_clients(user_id):
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("hash_key").eq(user_id)
        & Key("range_key").begins_with("CLIENT#"),
    )
    return [Client.from_item(item) for item in response["Items"]]
