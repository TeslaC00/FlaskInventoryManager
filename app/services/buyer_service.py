from app.errors.not_found_error import NotFoundError
from app.models import Buyer
from app.repositories.buyer_repository import BuyerRepository


class BuyerService:

    @staticmethod
    def get_all_buyers(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return BuyerRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Buyers: {str(e)}")

    @staticmethod
    def get_buyer_by_id(buyer_id: int) -> Buyer:
        buyer = BuyerRepository.get_by_id(buyer_id)
        if not buyer:
            raise NotFoundError(f"Buyer with id {buyer_id} not found")
        return buyer

    @staticmethod
    def add_buyer(**data: dict) -> Buyer:
        buyer = Buyer(**data)
        try:
            return BuyerRepository.add(buyer)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Buyer: {str(e)}")

    @staticmethod
    def update_buyer(buyer_id: int, data: dict) -> Buyer:
        # Fetch existing buyer
        existing_buyer = BuyerService.get_buyer_by_id(buyer_id)

        # Update fields in the existing buyer
        for key, value in data.items():
            setattr(existing_buyer, key, value)

        # Pass updated buyer object to the repository
        try:
            return BuyerRepository.update(existing_buyer)
        except Exception as e:
            raise RuntimeError(f"Error updating Buyer: {str(e)}")

    @staticmethod
    def delete_buyer(buyer_id: int) -> None:
        try:
            BuyerRepository.delete(buyer_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Buyer: {str(e)}")
