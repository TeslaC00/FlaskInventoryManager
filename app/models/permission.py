from app.extensions import db


# Note: This is a Static Model and all values should be predefined.
#       This is available in readonly access to user.
class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255), nullable=False)
