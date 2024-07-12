from app.errors.not_found_error import NotFoundError
from app.models import Bill
from app.repositories.bill_repository import BillRepository


class BillService:
    @staticmethod
    def get_all_bills(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return BillRepository.get_all(page, per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Bills: {str(e)}")

    @staticmethod
    def get_bill_by_id(bill_id: int) -> Bill:
        bill = BillRepository.get_by_id(bill_id)
        if not bill:
            raise NotFoundError(f"Bill with id {bill_id} not found")
        return bill

    @staticmethod
    def add_bill(**data: dict) -> Bill:
        bill = Bill(**data)
        try:
            return BillRepository.add(bill)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Bill: {str(e)}")

    @staticmethod
    def update_total_price(bill_id: int) -> Bill:
        bill = BillRepository.get_by_id(bill_id)
        bill.total_price = sum(item.price * item.quantity for item in bill.bill_items)
        return BillRepository.update(bill)

    @staticmethod
    def update_bill(bill_id: int, data: dict) -> Bill:
        existing_bill = BillService.get_bill_by_id(bill_id)

        for key, value in data.items():
            setattr(existing_bill, key, value)

        try:
            return BillRepository.update(existing_bill)
        except Exception as e:
            raise RuntimeError(f"Error updating Bill: {str(e)}")

    @staticmethod
    def delete_bill(bill_id: int) -> None:
        bill = BillService.get_bill_by_id(bill_id)
        try:
            from app.services.bill_item_service import BillItemService
            for bill_item in bill.bill_items:
                BillItemService.delete_bill_item(bill_item.id)
            BillRepository.delete(bill_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Buyer: {str(e)}")
