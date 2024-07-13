from app.errors.not_found_error import NotFoundError
from app.models import ProductScrap
from app.repositories.product_scrap_repository import ProductScrapRepository


class ProductScrapService:
    @staticmethod
    def get_all_product_scraps(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return ProductScrapRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching ProductScraps: {str(e)}")

    @staticmethod
    def get_product_scrap_by_id(product_part_no: int, date: str) -> ProductScrap:
        product_scrap = ProductScrapRepository.get_by_id(product_part_no, date)
        if not product_scrap:
            raise NotFoundError(f"ProductScrap with id {product_part_no, date} not found")
        return product_scrap

    @staticmethod
    def add_product_scrap(**data: dict) -> ProductScrap:
        product_scrap = ProductScrap(**data)
        try:
            new_product_scrap = ProductScrapRepository.add(product_scrap)
            from app.services.product_service import ProductService
            ProductService.add_quantity(-new_product_scrap.quantity, new_product_scrap.product_part_no)
            return new_product_scrap
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating ProductScrap: {str(e)}")

    @staticmethod
    def update_product_scrap(product_part_no: int, date: str, data: dict) -> ProductScrap:
        existing_product_scrap = ProductScrapService.get_product_scrap_by_id(product_part_no, date)
        initial_quantity = existing_product_scrap.quantity
        for key, value in data.items():
            setattr(existing_product_scrap, key, value)
        try:
            product_scrap = ProductScrapRepository.update(existing_product_scrap)
            from app.services.product_service import ProductService
            ProductService.add_quantity(initial_quantity - product_scrap.quantity, product_part_no)
            return product_scrap
        except Exception as e:
            raise RuntimeError(f"Error updating ProductScrap: {str(e)}")

    @staticmethod
    def delete_product_scrap(product_part_no: int, date: str) -> None:
        try:
            initial_quantity = ProductScrapService.get_product_scrap_by_id(product_part_no, date).quantity
            ProductScrapRepository.delete(product_part_no, date)
            from app.services.product_service import ProductService
            ProductService.add_quantity(initial_quantity, product_part_no)
        except Exception as e:
            raise RuntimeError(f"Error deleting ProductScrap: {str(e)}")
