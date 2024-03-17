from app.database import db


class Goods_Records(db.Model):
    __tablename__ = 'Goods_Records'
    date = db.Column(db.Date, nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'))
    goods = db.relationship('Goods', backref='goods_records')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'good_name'),)
