from typing import List

from app.errors.not_found_error import NotFoundError
from app.models import ChallanItem
from app.repositories.challan_item_repository import ChallanItemRepository
from app.logger import logger


class ChallanItemService:
    @staticmethod
    def get_all_challan_items(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return ChallanItemRepository.get_all(page, per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching ChallanItems: {str(e)}")

    @staticmethod
    def get_challan_item_by_id(challan_item_id: int) -> ChallanItem:
        challan_item = ChallanItemRepository.get_by_id(challan_item_id)
        if not challan_item:
            raise NotFoundError(f"ChallanItem with id {challan_item_id} not found")
        return challan_item

    @staticmethod
    def add_challan_item(challan_id: int, **data: dict) -> ChallanItem:
        challan_item = ChallanItem(
            quantity=data['quantity'],
            price=data['price'],
            material_part_no=data['material_part_no'],
            challan_id=challan_id
        )
        try:
            new_challan_item = ChallanItemRepository.add(challan_item)
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(new_challan_item.quantity, new_challan_item.material_part_no)
            return new_challan_item
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating ChallanItem: {str(e)}")

    @staticmethod
    def add_all_challan_items(data: List) -> None:
        for challan_item in data:
            ChallanItemService.add_challan_item(**challan_item)

    @staticmethod
    def update_challan_item(challan_item_id: int, data: dict) -> ChallanItem:
        existing_challan_item = ChallanItemService.get_challan_item_by_id(challan_item_id)
        initial_quantity = existing_challan_item.quantity

        for key, value in data.items():
            setattr(existing_challan_item, key, value)

        try:
            challan_item = ChallanItemRepository.update(existing_challan_item)
            from app.services.challan_service import ChallanService
            ChallanService.update_total_price(challan_item.challan_id)
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(challan_item.quantity - initial_quantity, challan_item.material_part_no)
            return challan_item
        except Exception as e:
            raise RuntimeError(f"Error updating ChallanItem: {str(e)}")

    @staticmethod
    def delete_challan_item(challan_item_id: int) -> None:
        try:
            challan_item = ChallanItemService.get_challan_item_by_id(challan_item_id)
            ChallanItemRepository.delete(challan_item_id)
            from app.services.challan_service import ChallanService
            logger.info(ChallanService.update_total_price(challan_item.challan_id))
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(-challan_item.quantity, challan_item.material_part_no)
        except Exception as e:
            raise RuntimeError(f"Error deleting ChallanItem: {str(e)}")
