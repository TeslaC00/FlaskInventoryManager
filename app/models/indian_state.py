from app.extensions import db


# Note: This is a Static Model and all values should be predefined.
#       This is available in readonly access to user.
class IndianState(db.Model):
    __tablename__ = 'indian_state'
    id = db.Column(db.Integer, primary_key=True)  # use as state code
    name = db.Column(db.String(80), unique=True, nullable=False)
    abbreviation = db.Column(db.String(10), unique=True, nullable=False)
