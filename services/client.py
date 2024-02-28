from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class Client(Item):
    def __init__(
        self,
        user_id,
        email,
        name,
        pronouns,
        over_18,
        preferred_contact,
        phone_number,
    ):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.pronouns = pronouns
        self.over_18 = over_18
        self.preferred_contact = preferred_contact
        self.phone_number = phone_number

    @classmethod
    def from_item(cls, item):
        return cls(
            item["user_id"],
            item["email"],
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
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "pronouns": self.pronouns,
            "over_18": self.over_18,
            "preferred_contact": self.preferred_contact,
            "phone_number": self.phone_number,
            "item_type": "client",
        }


def create_or_update_client(client):
    table = get_dynamodb_table()

    table.put_item(Item=client.to_item())
    return client


def get_client(user_id, email):
    user_id_key = f"USER#{user_id}"
    email_key = f"CLIENT#{email}"

    table = get_dynamodb_table()
    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(email_key)
    )
    return Client(**response["Item"])


def list_clients(user_id):
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id) & Key("SK").begins_with("CLIENT#"),
    )
    return [Client.from_item(item) for item in response["Items"]]
