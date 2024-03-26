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

    def pk(self) -> str:
        return f"USER#{self.user_id}"

    def sk(self) -> str:
        return f"USER#{self.user_id}"


def get_user(user_id: str) -> User:
    table = get_dynamodb_table()

    user_id_key: str = f"USER#{user_id}"
    response: dict = table.query(
        KeyConditionExpression=Key("PK").eq(user_id_key) & Key("SK").eq(user_id_key)
    )
    return User(**response["Items"][0])


def create_or_update_user(user: User) -> User:
    table = get_dynamodb_table()

    table.put_item(Item=user.to_item())
    return user
