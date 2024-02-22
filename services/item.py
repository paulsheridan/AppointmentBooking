import json
from abc import ABC, abstractmethod


class Item(ABC):

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

    def toJSON(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
