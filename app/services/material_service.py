from app.errors.not_found_error import NotFoundError
from app.models import Material
from app.repositories.material_repository import MaterialRepository


class MaterialService:
    @staticmethod
    def get_all_materials(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return MaterialRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Materials: {str(e)}")

    @staticmethod
    def get_material_by_id(material_id: int) -> Material:
        material = MaterialRepository.get_by_id(material_id)
        if not material:
            raise NotFoundError(f"Material with id {material_id} not found")
        return material

    @staticmethod
    def add_material(**data: dict) -> Material:
        material = Material(**data)
        try:
            return MaterialRepository.add(material)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Material: {str(e)}")

    @staticmethod
    def update_material(material_id: int, data: dict) -> Material:
        # Fetch existing material
        existing_material = MaterialService.get_material_by_id(material_id)

        # Update fields in the existing material
        for key, value in data.items():
            setattr(existing_material, key, value)

        # Pass updated material object to the repository
        try:
            return MaterialRepository.update(existing_material)
        except Exception as e:
            raise RuntimeError(f"Error updating Material: {str(e)}")

    @staticmethod
    def delete_material(material_id: int) -> None:
        try:
            MaterialRepository.delete(material_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Material: {str(e)}")
