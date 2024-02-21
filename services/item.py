import json
from abc import ABC, abstractmethod


class Item(ABC):

    @abstractmethod
    def get_pk():
        pass

    @abstractmethod
    def get_sk():
        pass

    def keys(self):
        return {"PK": self.get_pk(), "SK": self.get_sk()}

    @abstractmethod
    def to_item():
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
