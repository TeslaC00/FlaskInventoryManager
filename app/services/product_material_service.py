from app.errors.not_found_error import NotFoundError
from app.models import ProductMaterial
from app.repositories.product_material_repository import ProductMaterialRepository


class ProductMaterialService:

    @staticmethod
    def get_all_product_materials(page: int = 1, per_page: int = 10):
        try:
            return ProductMaterialRepository.get_all(page=page, per_page=per_page)
        except Exception as e:
            raise RuntimeError(f"Error fetching ProductMaterials: {str(e)}")

    @staticmethod
    def get_product_material_by_id(product_part_no: int, material_part_no: int) -> ProductMaterial:
        product_material = ProductMaterialRepository.get_by_id(product_part_no, material_part_no)
        if not product_material:
            raise NotFoundError(f"ProductMaterial with id {product_part_no, material_part_no} not found")
        return product_material

    @staticmethod
    def add_product_material(**data: dict) -> ProductMaterial:
        product_material = ProductMaterial(**data)
        try:
            return ProductMaterialRepository.add(product_material)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating ProductMaterial: {str(e)}")

    @staticmethod
    def update_product_material(product_part_no: int, material_part_no: int, data: dict) -> ProductMaterial:
        # Fetch existing product_material
        existing_product_material = ProductMaterialService.get_product_material_by_id(product_part_no, material_part_no)

        # Update fields in the existing product_material
        for key, value in data.items():
            setattr(existing_product_material, key, value)

        # Pass updated product_material object to the repository
        try:
            return ProductMaterialRepository.update(existing_product_material)
        except Exception as e:
            raise RuntimeError(f"Error updating ProductMaterial: {str(e)}")

    @staticmethod
    def delete_product_material(product_part_no: int, material_part_no: int) -> None:
        try:
            ProductMaterialRepository.delete(product_part_no, material_part_no)
        except Exception as e:
            raise RuntimeError(f"Error deleting ProductMaterial: {str(e)}")
