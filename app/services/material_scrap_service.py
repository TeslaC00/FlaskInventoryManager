from app.errors.not_found_error import NotFoundError
from app.models import MaterialScrap
from app.repositories.material_scrap_repository import MaterialScrapRepository


class MaterialScrapService:
    @staticmethod
    def get_all_material_scraps(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return MaterialScrapRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching MaterialScraps: {str(e)}")

    @staticmethod
    def get_material_scrap_by_id(material_scrap_id: int) -> MaterialScrap:
        material_scrap = MaterialScrapRepository.get_by_id(material_scrap_id)
        if not material_scrap:
            raise NotFoundError(f"MaterialScrap with id {material_scrap_id} not found")
        return material_scrap

    @staticmethod
    def add_material_scrap(**data: dict) -> MaterialScrap:
        material_scrap = MaterialScrap(**data)
        try:
            new_material_scrap = MaterialScrapRepository.add(material_scrap)
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(-new_material_scrap.quantity, new_material_scrap.material_part_no)
            return new_material_scrap
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating MaterialScrap: {str(e)}")

    @staticmethod
    def update_material_scrap(material_scrap_id: int, data: dict) -> MaterialScrap:
        existing_material_scrap = MaterialScrapService.get_material_scrap_by_id(material_scrap_id)
        initial_quantity = existing_material_scrap.quantity
        for key, value in data.items():
            setattr(existing_material_scrap, key, value)
        try:
            material_scrap = MaterialScrapRepository.update(existing_material_scrap)
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(initial_quantity - material_scrap.quantity, material_scrap.material_part_no)
            return material_scrap
        except Exception as e:
            raise RuntimeError(f"Error updating MaterialScrap: {str(e)}")

    @staticmethod
    def delete_material_scrap(material_scrap_id: int) -> None:
        try:
            material_scrap = MaterialScrapService.get_material_scrap_by_id(material_scrap_id)
            MaterialScrapRepository.delete(material_scrap_id)
            from app.services.material_service import MaterialService
            MaterialService.add_quantity(material_scrap.quantity, material_scrap.material_part_no)
        except Exception as e:
            raise RuntimeError(f"Error deleting MaterialScrap: {str(e)}")
