from app import db


class Bill(db.Model):
    __tablename__ = 'Bill'
    price = db.Column(db.Integer, nullable=False)
    bill_no = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('Buyer.buyer_id'), nullable=False)
    name = db.Column(db.String(50), db.ForeignKey('Goods.name'), nullable=False)
    buyer = db.relationship('Buyer', backref='bills')
    goods = db.relationship('Goods', backref='bills')
    __table_args__ = (db.PrimaryKeyConstraint('date','buyer_id','name',name='bill_pkey'),)
