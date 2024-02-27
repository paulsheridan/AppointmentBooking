from boto3.dynamodb.conditions import Key

from item import Item


class WorkDay(Item):
    def __init__(self, user_id, date, time_slots):
        self.user_id = user_id
        self.date = date
        self.time_slots = time_slots

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
