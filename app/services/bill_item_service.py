from typing import List

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
    def add_bill_item(bill_id: int, **data: dict) -> BillItem:
        bill_item = BillItem(
            quantity=data['quantity'],
            price=data['price'],
            c_gst=data['c_gst'],
            s_gst=data['s_gst'],
            i_gst=data['i_gst'],
            product_part_no=data['product_part_no'],
            bill_id=bill_id
        )
        try:
            new_bill_item = BillItemRepository.add(bill_item)
            from app.services.product_service import ProductService
            ProductService.add_quantity(-new_bill_item.quantity, new_bill_item.product_part_no)
            return new_bill_item
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating BillItem: {str(e)}")

    @staticmethod
    def add_all_bill_items(data: List) -> None:
        for bill_item in data:
            BillItemService.add_bill_item(**bill_item)

    @staticmethod
    def update_bill_item(bill_item_id: int, data: dict) -> BillItem:
        existing_bill_item = BillItemService.get_bill_item_by_id(bill_item_id)
        initial_quantity = existing_bill_item.quantity

        for key, value in data.items():
            setattr(existing_bill_item, key, value)

        try:
            bill_item = BillItemRepository.update(existing_bill_item)
            from app.services.bill_service import BillService
            BillService.update_total_price(bill_item.bill_id)
            from app.services.product_service import ProductService
            ProductService.add_quantity(initial_quantity - bill_item.quantity, bill_item.product_part_no)
            return bill_item
        except Exception as e:
            raise RuntimeError(f"Error updating BillItem: {str(e)}")

    @staticmethod
    def delete_bill_item(bill_item_id: int) -> None:
        try:
            bill_item = BillItemService.get_bill_item_by_id(bill_item_id)
            BillItemRepository.delete(bill_item_id)
            from app.services.bill_service import BillService
            BillService.update_total_price(bill_item.bill_id)
            from app.services.product_service import ProductService
            ProductService.add_quantity(bill_item.quantity, bill_item.product_part_no)
        except Exception as e:
            raise RuntimeError(f"Error deleting BillItem: {str(e)}")
