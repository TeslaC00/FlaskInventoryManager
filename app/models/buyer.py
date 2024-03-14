from app import db


class Buyer(db.Model):
    __tablename__ = 'Buyer'
    name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    buyer_id = db.Column(db.Integer, primary_key=True)
