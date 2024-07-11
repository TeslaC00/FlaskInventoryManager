from app.extensions import db


class Permission(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
