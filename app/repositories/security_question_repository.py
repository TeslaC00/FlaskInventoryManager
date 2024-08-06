from typing import Optional

from app.models import SecurityQuestion, UserSecurityQuestions
from app.extensions import db


class SecurityQuestionRepository:
    @staticmethod
    def get_all():
        return SecurityQuestion.query.all()

    @staticmethod
    def get_by_id(user_id: int, question_id: int) -> Optional[UserSecurityQuestions]:
        return UserSecurityQuestions.query.filter_by(user_id=user_id, question_id=question_id).first()

    @staticmethod
    def add(user_question: UserSecurityQuestions) -> UserSecurityQuestions:
        db.session.add(user_question)
        db.session.commit()
        return user_question
