from pydantic import EmailStr
from uuid import UUID
from pydantic_extra_types.phone_numbers import PhoneNumber
from boto3.dynamodb.conditions import Key

from item import Item
from table_util import get_dynamodb_table


class Client(Item):
    user_id: UUID
    email: EmailStr
    name: str
    pronouns: str
    over_18: bool
    preferred_contact: str
    phone_number: PhoneNumber

    def pk(self) -> str:
        return f"USER#{self.user_id}"

    def sk(self) -> str:
        return f"CLIENT#{self.email}"


def create_or_update_client(client: Client) -> Client:
    table = get_dynamodb_table()

    table.put_item(Item=client.to_item())
    return client


def get_client(user_id: str, email: str) -> Client:
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").eq(f"CLIENT#{email}")
    )
    return Client(**response["Items"][0])


def list_clients(user_id: str) -> Client:
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").begins_with("CLIENT#"),
    )
    return [Client(**item) for item in response["Items"]]
