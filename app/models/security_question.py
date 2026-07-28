from app.extensions import db


# Note: This is a Static Model and all values should be predefined.
#       This is available in readonly access to user.
class SecurityQuestion(db.Model):
    __tablename__ = 'security_question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
