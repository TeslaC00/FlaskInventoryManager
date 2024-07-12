from app.errors.not_found_error import NotFoundError
from app.models import Challan
from app.repositories.challan_repository import ChallanRepository
from app.logger import logger


class ChallanService:
    @staticmethod
    def get_all_challans(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return ChallanRepository.get_all(page, per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Challans: {str(e)}")

    @staticmethod
    def get_challan_by_id(challan_id: int) -> Challan:
        challan = ChallanRepository.get_by_id(challan_id)
        if not challan:
            raise NotFoundError(f"Challan with id {challan_id} not found")
        return challan

    @staticmethod
    def add_challan(**data: dict) -> Challan:
        challan = Challan(**data)
        try:
            return ChallanRepository.add(challan)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Challan: {str(e)}")

    @staticmethod
    def update_total_price(challan_id: int) -> Challan:
        challan = ChallanRepository.get_by_id(challan_id)
        logger.info(challan)
        logger.info(f'price before{challan.total_price}')
        challan.total_price = sum(item.price * item.quantity for item in challan.challan_items)
        logger.info(f'price after{challan.total_price}')
        return ChallanRepository.update(challan)

    @staticmethod
    def update_challan(challan_id: int, data: dict) -> Challan:
        existing_challan = ChallanService.get_challan_by_id(challan_id)

        for key, value in data.items():
            setattr(existing_challan, key, value)

        try:
            return ChallanRepository.update(existing_challan)
        except Exception as e:
            raise RuntimeError(f"Error updating Challan: {str(e)}")

    @staticmethod
    def delete_challan(challan_id: int) -> None:
        challan = ChallanService.get_challan_by_id(challan_id)
        try:
            from app.services.challan_item_service import ChallanItemService
            for challan_item in challan.challan_items:
                ChallanItemService.delete_challan_item(challan_item.id)
            ChallanRepository.delete(challan_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Buyer: {str(e)}")
