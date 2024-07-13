from app.errors.not_found_error import NotFoundError
from app.models import Permission
from app.repositories.permission_repository import PermissionRepository


class PermissionService:
    @staticmethod
    def get_all_permissions():
        try:
            return PermissionRepository.get_all()
        except Exception as e:
            raise RuntimeError(f"Error fetching Permissions: {str(e)}")

    @staticmethod
    def get_permission_by_id(permission_id: int) -> Permission:
        permission = PermissionRepository.get_by_id(permission_id)
        if not permission:
            raise NotFoundError(f"Permission with id {permission_id} not found")
        return permission

    @staticmethod
    def add_permission(**data: dict) -> Permission:
        permission = Permission(**data)
        try:
            return PermissionRepository.add(permission)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating Permission: {str(e)}")

    @staticmethod
    def update_permission(permission_id: int, data: dict) -> Permission:
        # Fetch existing permission
        existing_permission = PermissionService.get_permission_by_id(permission_id)

        # Update fields in the existing permission
        for key, value in data.items():
            setattr(existing_permission, key, value)

        # Pass updated permission object to the repository
        try:
            return PermissionRepository.update(existing_permission)
        except Exception as e:
            raise RuntimeError(f"Error updating Permission: {str(e)}")

    @staticmethod
    def delete_permission(permission_id: int) -> None:
        try:
            PermissionRepository.delete(permission_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting Permission: {str(e)}")
