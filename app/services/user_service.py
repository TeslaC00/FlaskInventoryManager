from typing import Optional

from app.errors.not_found_error import NotFoundError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.role_service import RoleService
from app.services.security_question_service import SecurityQuestionService


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
    def get_user_by_username(username: str) -> Optional[User]:
        return UserRepository.get_by_username(username=username)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        return UserRepository.get_by_email(email=email)

    @staticmethod
    def add_user(**data: dict) -> User:
        try:
            questions = data.pop('questions')
            user = UserRepository.add(**data)
            for i in questions:
                SecurityQuestionService.add_question(user.id, i['id'], i['answer'])
            return user
        except KeyError as ke:
            raise KeyError(f"Security Question and Answers not found in data: {str(ke)}")
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
    def update_user_tracking(user: User) -> None:
        # TODO: add logic for updating user tracking attributes
        UserRepository.update(user)

    @staticmethod
    def delete_user_by_id(user_id: int) -> None:
        try:
            UserRepository.delete(user_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting User: {str(e)}")

    @staticmethod
    def authenticate_user(user: User, password: str) -> bool:
        if UserRepository.verify_password(user, password):
            return True
        return False

    @staticmethod
    def authenticate_user_answer(user: User, answer: str) -> bool:
        return UserRepository.verify_answer(user, answer)

    @staticmethod
    def reset_password(user: User, password: str) -> None:
        if not user:
            raise NotFoundError("Null user given")
        UserRepository.reset_password(user, password)
