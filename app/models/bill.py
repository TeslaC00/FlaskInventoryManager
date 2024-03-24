from app.database import db


class Bill(db.Model):
    """
    Represents a Bill record in the database.
    This model stores information about goods purchased by the buyers.
    It interacts with Buyer and Goods models.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        price (Integer): Stores the price of the goods in the bill. Not null.
        bill_no (Integer): Stores the bill number. Not null.
        quantity (Integer): Stores the quantity of goods in the bill. Not null.
        date (Date): Stores the date on which the bill was issued. Not null.
        buyer_id (Integer): Foreign key links to the Buyer's ID. Not null.
        good_name (str,50): Foreign key links to the Good's name. Not null.
        buyer (relationship): Establishes a relationship with the Buyer model.
        goods (relationship): Establishes a relationship with the Goods model.
        __table_args__: Additional table options, including a composite primary key('date','buyer_id','good_name').
    """
    __tablename__ = 'Bill'
    price = db.Column(db.Integer, nullable=False)
    bill_no = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('Buyer.buyer_id'), nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'), nullable=False)
    buyer = db.relationship('Buyer', backref='bills')
    goods = db.relationship('Goods', backref='bills')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'buyer_id', 'good_name', name='bill_pkey'),)
