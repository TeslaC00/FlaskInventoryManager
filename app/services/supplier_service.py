from app.errors.not_found_error import NotFoundError
from app.models import Supplier
from app.repositories.supplier_repository import SupplierRepository


class SupplierService:
    @staticmethod
    def get_all_suppliers(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return SupplierRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Supplier: {str(e)}")

    @staticmethod
    def get_supplier_by_id(supplier_id: int) -> Supplier:
        supplier = SupplierRepository.get_by_id(supplier_id)
        if not supplier:
            raise NotFoundError(f"Supplier with id {supplier_id} not found")
        return supplier

    @staticmethod
    def add_supplier(**data: dict) -> Supplier:
        supplier = Supplier(**data)
        try:
            return SupplierRepository.add(supplier)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Supplier: {str(e)}")

    @staticmethod
    def update_supplier(supplier_id: int, data: dict) -> Supplier:
        # Fetch existing supplier
        existing_supplier = SupplierService.get_supplier_by_id(supplier_id)

        # Update fields in the existing supplier
        for key, value in data.items():
            setattr(existing_supplier, key, value)

        # Pass updated supplier object to the repository
        try:
            return SupplierRepository.update(existing_supplier)
        except Exception as e:
            raise RuntimeError(f"Error updating Supplier: {str(e)}")

    @staticmethod
    def delete_supplier(supplier_id: int) -> None:
        try:
            SupplierRepository.delete(supplier_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Supplier: {str(e)}")
