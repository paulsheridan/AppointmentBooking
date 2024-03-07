from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime
from abc import abstractmethod


class Item(BaseModel):

    @abstractmethod
    def pk():
        pass

    @abstractmethod
    def sk():
        pass

    def keys(self):
        return {"PK": self.pk(), "SK": self.sk()}

    @abstractmethod
    def to_item():
        pass

    @field_serializer("user_id", "service_id", check_fields=False)
    def serialize_uuid(self, user_id: UUID):
        return str(user_id)

    @field_serializer("start_datetime", "end_datetime", "date_created", check_fields=False)
    def serialize_datetime(self, datetime: datetime):
        return datetime.isoformat("T", "minutes")

    @field_serializer("start", "end", check_fields=False)
    def serialize_date(self, date: datetime.date):
        return date.isoformat()
