from sqlalchemy import PrimaryKeyConstraint

from app.extensions import db


class UserSecurityQuestions(db.Model):
    __tablename__ = 'user_security_questions'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('security_question.id'), nullable=False)
    answer_hash = db.Column(db.String, nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'question_id'),)
