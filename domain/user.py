from pydantic import EmailStr
from typing import List
from uuid import UUID
from datetime import datetime
from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class User(Item):
    user_id: UUID
    username: str
    email: EmailStr
    date_created: datetime

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"USER#{self.user_id}"

    def to_item(self):
        return {
            **self.keys(),
            **self.model_dump(),
            "item_type": "user",
        }


def get_user(user_id):
    table = get_dynamodb_table()

    user_id_key = f"USER#{user_id}"
    response = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(user_id_key)
    )
    return [User(**item) for item in response["Items"]]


def create_or_update_user(user):
    table = get_dynamodb_table()

    table.put_item(Item=user.to_item())
    return user
