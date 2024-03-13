from app import db


class Goods_Records(db.Model):
    __tablename__ = 'Goods_Records'
    date = db.Column(db.Date, nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), db.ForeignKey('Goods.name'))
    goods = db.relationship('Goods', backref='goods_records')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'name'),)
