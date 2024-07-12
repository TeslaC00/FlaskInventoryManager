from app.errors.not_found_error import NotFoundError
from app.models import Product
from app.repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_all_products(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return ProductRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Products: {str(e)}")

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        return product

    @staticmethod
    def add_product(**data: dict) -> Product:
        product = Product(**data)
        try:
            return ProductRepository.add(product)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Product: {str(e)}")

    @staticmethod
    def update_product(product_id: int, data: dict) -> Product:
        # Fetch existing product
        existing_product = ProductService.get_product_by_id(product_id)

        # Update fields in the existing product
        for key, value in data.items():
            setattr(existing_product, key, value)

        # Pass updated product object to the repository
        try:
            return ProductRepository.update(existing_product)
        except Exception as e:
            raise RuntimeError(f"Error updating Product: {str(e)}")

    @staticmethod
    def delete_product(product_id: int) -> None:
        try:
            ProductRepository.delete(product_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Product: {str(e)}")
