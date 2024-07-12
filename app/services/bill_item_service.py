from app.errors.not_found_error import NotFoundError
from app.models import BillItem
from app.repositories.bill_item_repository import BillItemRepository


class BillItemService:
    @staticmethod
    def get_all_bill_items(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return BillItemRepository.get_all(page, per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching BillItems: {str(e)}")

    @staticmethod
    def get_bill_item_by_id(bill_item_id: int) -> BillItem:
        bill_item = BillItemRepository.get_by_id(bill_item_id)
        if not bill_item:
            raise NotFoundError(f"BillItem with id {bill_item_id} not found")
        return bill_item

    @staticmethod
    def add_bill_item(**data: dict) -> BillItem:
        bill_item = BillItem(**data)
        try:
            return BillItemRepository.add(bill_item)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating BillItem: {str(e)}")

    @staticmethod
    def update_bill_item(bill_item_id: int, data: dict) -> BillItem:
        existing_bill_item = BillItemService.get_bill_item_by_id(bill_item_id)

        for key, value in data.items():
            setattr(existing_bill_item, key, value)

        try:
            return BillItemRepository.update(existing_bill_item)
        except Exception as e:
            raise RuntimeError(f"Error updating BillItem: {str(e)}")

    @staticmethod
    def delete_bill_item(bill_item_id: int) -> None:
        try:
            BillItemRepository.delete(bill_item_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting BillItem: {str(e)}")
