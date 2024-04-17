from app.database import db


class Bill(db.Model):
    """
    Represents a Bill record in the database.
    This model stores information about goods purchased by the buyers.
    It interacts with Buyer and Goods models.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        bill_no (Integer): Stores the bill number. Not null.
        total_price (Integer): Stores the quantity of goods in the bill. Not null.
        date (Date): Stores the date on which the bill was issued. Not null.
        buyer_id (Integer): Foreign key links to the Buyer's ID. Not null.
        product_name (str,50): Foreign key links to the Good's name. Not null.
        buyer (relationship): Establishes a relationship with the Buyer model.
        product (relationship): Establishes a relationship with the Goods model.
        __table_args__: Additional table options, including a composite primary key('date','buyer_id','good_name').
    """
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id', name='fk_bill_buyer_id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    purchase_order = db.Column(db.String(30), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    bill_items = db.relationship('BillItem', backref='bill', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'total_price': self.total_price,
            'date': self.date,
            'buyer_id': self.buyer_id,
            'purchase_order': self.purchase_order
        }
