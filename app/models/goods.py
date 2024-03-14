from app import db


class Goods(db.Model):
    __tablename__ = 'Goods'
    name = db.Column(db.String(50), primary_key=True)
    unit_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
