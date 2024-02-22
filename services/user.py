import boto3
import os

from boto3.dynamodb.conditions import Key

from item import Item


class User(Item):
    def __init__(self, user_id, username, email, date_created):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.date_created = date_created

    @classmethod
    def from_item(cls, item):
        return cls(
            item["user_id"],
            item["username"],
            item["email"],
            item["date_created"],
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
            "item_type": "user"
        }
