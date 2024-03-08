from uuid import UUID
from pydantic import BaseModel, FutureDate, field_serializer
from datetime import time
from typing import List
from boto3.dynamodb.conditions import Key


from item import Item
from table_util import get_dynamodb_table


class DailySchedule(BaseModel):
    weekday: int
    open: time
    close: time

    @field_serializer("open", "close", check_fields=False)
    def serialize_time(self, time: time):
        return time.isoformat()


class Service(Item):
    service_id: UUID
    user_id: UUID
    name: str
    active: bool
    duration: int
    max_per_day: int
    start: FutureDate
    end: FutureDate
    schedule: List[DailySchedule]

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"SRVC#{self.service_id}"

    def to_item(self):
        return {
            **self.keys(),
            **self.model_dump(),
            "item_type": "service",
        }


def create_service(service):
    table = get_dynamodb_table()
    table.put_item(Item=service.to_item())
    return service


def get_service(user_id, service_id):
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").eq(f"SRVC#{service_id}")
    )
    return [Service(**item) for item in response["Items"]]
