from app.database import db


class Goods_Scrap(db.Model):
    __tablename__ = 'Goods_Scrap'
    date = db.Column(db.Date, nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    goods = db.relationship('Goods', backref='goods_scrap')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'good_name'),)

    def to_dict(self):
        return {
            'date': self.date,
            'good_name': self.good_name,
            'quantity': self.quantity
        }
