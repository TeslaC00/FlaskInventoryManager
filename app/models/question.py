from app.extensions import db


# Note: This is a Static Model and all values should be predefined.
#       This is available in readonly access to user.
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)

    @staticmethod
    def load_static_data():
        data = [
            {"id": 1, "question": "What is your name?"},
            {"id": 2, "question": "What is your date of birth?"},
            {"id": 3, "question": "What is your favorite color?"},
            {"id": 4, "question": "What is your mother's maiden name?"},
            {"id": 5, "question": "What was the name of your first pet?"}
        ]
        for item in data:
            question = Question(id=item['id'], question=item['question'])
            db.session.add(question)
        db.session.commit()
