from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime, date
from abc import abstractmethod


class Item(BaseModel):

    @abstractmethod
    def pk():
        pass

    @abstractmethod
    def sk():
        pass

    def keys(self) -> dict:
        return {"PK": self.pk(), "SK": self.sk()}

    def to_item(self) -> dict:
        return {
            **self.keys(),
            **self.model_dump(),
            "item_type": self.__class__.__name__.lower(),
        }

    @field_serializer("user_id", "service_id", check_fields=False)
    def serialize_uuid(self, user_id: UUID) -> str:
        return str(user_id)

    @field_serializer("start", "end", "date_created", check_fields=False)
    def serialize_datetime(self, datetime: datetime) -> str:
        return datetime.isoformat("T", "minutes")

    @field_serializer("start", "end", check_fields=False)
    def serialize_date(self, date: date) -> str:
        return date.isoformat()
