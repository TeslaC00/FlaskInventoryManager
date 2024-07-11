from abc import ABC, abstractmethod

from app.models import Buyer


class BuyerRepository(ABC):
    @abstractmethod
    def get_all(self, filters=None, pagination_parameters=None):
        pass

    @abstractmethod
    def get_by_id(self, buyer_id):
        pass

    @abstractmethod
    def add(self, buyer: Buyer):
        pass

    @abstractmethod
    def update(self, buyer: Buyer):
        pass

    @abstractmethod
    def delete(self, buyer_id):
        pass
