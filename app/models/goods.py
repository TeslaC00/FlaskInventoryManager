from app.database import db


class Goods(db.Model):
    __tablename__ = 'Goods'
    good_name = db.Column(db.String(50), primary_key=True)
    unit_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    part_no = db.Column(db.Integer, nullable=False, unique=True)
