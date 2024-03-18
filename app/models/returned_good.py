from app import db


class Returned_Good(db.Model):
    __tablename__ = 'Returned_Good'
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('Buyer.buyer_id'), nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'), nullable=False)
    buyer = db.relationship('Buyer', backref='returned_goods')
    goods = db.relationship('Goods', backref='returned_goods')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'good_name', 'buyer_id', name='returned_goods__pkey'),)

    def to_dict(self):
        return {
            'date': self.date,
            'quantity': self.quantity,
            'buyer_id': self.buyer_id,
            'good_name': self.good_name,
        }
