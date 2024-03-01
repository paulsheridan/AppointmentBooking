from pydantic import EmailStr
from typing import List
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key

from item import Item
from work_day import WorkDay
from table_util import get_dynamodb_table


class User(Item):
    user_id: UUID
    username: str
    email: EmailStr
    date_created: datetime
    availability: List[WorkDay]

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
            "availability": self.availability,
            "item_type": "user",
        }


def get_user(user_id):
    table = get_dynamodb_table()

    user_id_key = f"USER#{user_id}"
    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(user_id_key)
    )
    print(response)
    return User.from_item(response["Items"][0])


def create_or_update_user(user):
    table = get_dynamodb_table()

    table.put_item(Item=user.to_item())
    return user
