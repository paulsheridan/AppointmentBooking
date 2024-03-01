from uuid import UUID
from datetime import date

from item import Item

class WorkDay(Item):
    user_id: UUID
    date = date
    time_slots = dict

    @classmethod
    def from_item(cls, item):
        return cls(
            item["user_id"],
            item["date"],
            item["time_slots"],
        )

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"DATE#{self.date}"

    def to_item(self):
        return {
            **self.keys(),
            "user_id": self.user_id,
            "date": self.date,
            "time_slots": self.time_slots,
            "item_type": "work_day",
        }
