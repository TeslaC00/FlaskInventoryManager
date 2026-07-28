from app.errors.not_found_error import NotFoundError
from app.models import Role
from app.repositories.role_repository import RoleRepository


class RoleService:
    @staticmethod
    def get_all_roles(**filters: dict):
        try:
            return RoleRepository.get_all(**filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching Role: {str(e)}")

    @staticmethod
    def get_role_by_id(role_id: int) -> Role:
        role = RoleRepository.get_by_id(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")
        return role

    @staticmethod
    def add_role(**data: dict) -> Role:
        try:
            return RoleRepository.add(**data)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Role: {str(e)}")

    @staticmethod
    def update_role(role_id: int, data: dict) -> Role:
        # Fetch existing role
        existing_role = RoleService.get_role_by_id(role_id)

        for key, value in data.items():
            setattr(existing_role, key, value)

        try:
            return RoleRepository.update(existing_role)
        except Exception as e:
            raise RuntimeError(f"Error updating Role: {str(e)}")

    @staticmethod
    def delete_role_by_id(role_id: int) -> None:
        try:
            RoleRepository.delete(role_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Role: {str(e)}")
