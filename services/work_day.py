from uuid import UUID
from datetime import date

from item import Item

class WorkDay(Item):
    user_id: UUID
    date_scheduled: date
    time_slots: dict

    def pk(self):
        return f"USER#{self.user_id}"

    def sk(self):
        return f"DATE#{self.date_scheduled}"

    def to_item(self):
        return {
            **self.keys(),
            **self.model_dump(),
            "item_type": "work_day",
        }
