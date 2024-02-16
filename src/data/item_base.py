from abc import ABC, abstractmethod

class Item(ABC):

    @abstractmethod
    def get_pk():
        pass

    @abstractmethod
    def get_sk():
        pass

    def keys(self):
        return {
            "PK": self.pk,
            "SK": self.sk
        }

    @abstractmethod
    def to_item():
        pass
