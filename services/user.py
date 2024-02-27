from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class User(Item):
    def __init__(self, user_id, username, email, date_created, availability):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.date_created = date_created
        self.availability = availability

    @classmethod
    def from_item(cls, item):
        return cls(
            item["user_id"],
            item["username"],
            item["email"],
            item["date_created"],
            item["availability"],
        )

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"USER#{self.user_id}"

    def to_item(self):
        return {
            **self.keys(),
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "date_created": self.date_created,
            "availability": self.availabilty,
            "item_type": "user",
        }


def get_user(user_id):
    table = get_dynamodb_table()

    user_id_key = f"USER#{user_id}"

    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(user_id_key)
    )
    return User(**response["Item"])
