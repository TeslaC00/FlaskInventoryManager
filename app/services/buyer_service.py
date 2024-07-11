from app.models import Buyer
from app.repositories.buyer_repository import BuyerRepository


class BuyerService:
    def __init__(self, buyer_repository: BuyerRepository):
        self.buyer_repository = buyer_repository

    def get_all_buyers(self, filters=None, pagination_parameters=None):
        return self.buyer_repository.get_all(filters, pagination_parameters)

    def get_buyer_by_id(self, buyer_id):
        return self.buyer_repository.get_by_id(buyer_id)

    def add_buyer(self, data):
        buyer = Buyer(**data)
        return self.buyer_repository.add(buyer)

    def update_buyer(self, buyer_id, data):
        buyer = self.buyer_repository.get_by_id(buyer_id)
        if buyer:
            for key, value in data.items():
                setattr(buyer, key, value)
            return self.buyer_repository.update(buyer)
        return None

    def delete_buyer(self, buyer_id):
        buyer = self.buyer_repository.get_by_id(buyer_id)
        if buyer:
            self.buyer_repository.delete(buyer)
        return buyer
