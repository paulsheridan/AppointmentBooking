from uuid import UUID
from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime, time
from typing import List, Optional
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
    start: datetime
    end: datetime
    schedule: List[DailySchedule]

    def pk(self) -> str:
        return f"USER#{self.user_id}"

    def sk(self) -> str:
        return f"SRVC#{self.service_id}"

    def get_daily_schedule(self, to_find: int) -> Optional[DailySchedule]:
        low, high = 0, len(self.schedule) - 1

        while low <= high:
            mid = (high + low) // 2
            if self.schedule[mid].weekday < to_find:
                low = mid + 1
            elif self.schedule[mid].weekday > to_find:
                high = mid - 1
            else:
                return self.schedule[mid]
        return None


def create_service(service: Service) -> Service:
    table = get_dynamodb_table()
    # TODO: validate that dates are in the future, since Service won't anymore.
    table.put_item(Item=service.to_item())
    return service


def get_service(user_id: str, service_id: str) -> Service:
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression=Key("PK").eq(f"USER#{user_id}")
        & Key("SK").eq(f"SRVC#{service_id}")
    )
    return Service(**response["Items"][0])
