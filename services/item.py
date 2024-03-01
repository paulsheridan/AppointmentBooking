from pydantic import BaseModel
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
