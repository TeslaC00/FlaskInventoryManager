from app.errors.not_found_error import NotFoundError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService


class UserService:
    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return UserRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching User: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")
        return user

    @staticmethod
    def add_user(**data: dict) -> User:
        try:
            return UserRepository.add(**data)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating User: {str(e)}")

    @staticmethod
    def update_user(user_id: int, data: dict) -> User:
        # Fetch existing user
        existing_user = UserService.get_user_by_id(user_id)

        if 'active' in data:
            if data['active']:
                UserRepository.activate(existing_user)
            else:
                UserRepository.deactivate(existing_user)

        if 'role_ids' in data:
            roles = []
            for role_id in data['role_ids']:
                roles.append(RoleService.get_role_by_id(role_id))
        try:
            return UserRepository.update(existing_user)
        except Exception as e:
            raise RuntimeError(f"Error updating User: {str(e)}")

    @staticmethod
    def delete_user_by_id(user_id: int) -> None:
        try:
            UserRepository.delete(user_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting User: {str(e)}")
