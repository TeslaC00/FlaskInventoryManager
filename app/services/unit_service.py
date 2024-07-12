from app.models import Unit
from app.repositories.unit_repository import UnitRepository
from app.errors.not_found_error import NotFoundError


class UnitService:
    @staticmethod
    def get_all_units():
        try:
            return UnitRepository.get_all()
        except Exception as e:
            raise RuntimeError(f"Error fetching Unit: {str(e)}")

    @staticmethod
    def get_unit_by_id(unit_id: int) -> Unit:
        unit = UnitRepository.get_by_id(unit_id)
        if not unit:
            raise NotFoundError(f"Unit with id {unit_id} not found")
        return unit

    @staticmethod
    def add_unit(**data: dict) -> Unit:
        unit = Unit(**data)
        try:
            return UnitRepository.add(unit)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Unit: {str(e)}")

    @staticmethod
    def update_unit(unit_id: int, data: dict) -> Unit:
        # Fetch existing unit
        existing_unit = UnitService.get_unit_by_id(unit_id)

        # Update fields in the existing unit
        for key, value in data.items():
            setattr(existing_unit, key, value)

        # Pass updated unit object to the repository
        try:
            return UnitRepository.update(existing_unit)
        except Exception as e:
            raise RuntimeError(f"Error updating Unit: {str(e)}")

    @staticmethod
    def delete_unit(unit_id: int) -> None:
        try:
            UnitRepository.delete(unit_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Unit: {str(e)}")
