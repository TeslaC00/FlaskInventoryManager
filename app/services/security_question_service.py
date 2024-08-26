from app.errors.not_found_error import NotFoundError
from app.models import UserSecurityQuestions
from app.repositories.security_question_repository import SecurityQuestionRepository


class SecurityQuestionService:
    @staticmethod
    def get_all_questions():
        try:
            return SecurityQuestionRepository.get_all()
        except Exception as e:
            raise RuntimeError(f"Error fetching Buyers: {str(e)}")

    @staticmethod
    def add_question(user_id: int, question_id: int, answer: str) -> UserSecurityQuestions:
        question = UserSecurityQuestions(user_id=user_id, question_id=question_id, answer=answer)
        try:
            return SecurityQuestionRepository.add(question)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating UserSecurityQuestion: {str(e)}")

    @staticmethod
    def verify_answer(user_id: int, question_id: int, answer: str) -> bool:
        question = SecurityQuestionRepository.get_by_id(user_id, question_id)
        if question is None:
            raise NotFoundError(f"Security Question for user: {user_id} and question: {question_id} was not found")
        return question.answer_hash == answer
