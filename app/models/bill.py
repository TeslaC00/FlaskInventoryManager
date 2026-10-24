from app.database import db
from datetime import datetime


class Bill(db.Model):
    """
    Represents a Bill record in the database.
    This model stores information about goods purchased by the buyers.
    It interacts with Buyer and Goods models.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        id (Integer): Stores the bill number. Not null.
        quantity (Integer): Stores the quantity of goods in the bill. Not null.
        date (Date): Stores the date on which the bill was issued. Not null.
        buyer_id (Integer): Foreign key links to the Buyer's ID. Not null.
        product_name (str,50): Foreign key links to the Good's name. Not null.
        buyer (relationship): Establishes a relationship with the Buyer model.
        product (relationship): Establishes a relationship with the Goods model.
        __table_args__: Additional table options, including a composite primary key('date','buyer_id','good_name').
    """
    __tablename__ = 'bill'
    id = db.Column(db.Integer, nullable=False)
    purchase_order = db.Column(db.String(20), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id', name='fk_bill_buyer_id'), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.today())
    bill_items = db.relationship('BillItem', backref='bill', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'purchase_order': self.purchase_order,
            'date': self.date,
            'buyer_id': self.buyer_id,
            'total_price': self.total_price,
        }
