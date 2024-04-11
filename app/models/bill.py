from app.database import db


class Bill(db.Model):
    """
    Represents a Bill record in the database.
    This model stores information about goods purchased by the buyers.
    It interacts with Buyer and Goods models.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        bill_no (Integer): Stores the bill number. Not null.
        quantity (Integer): Stores the quantity of goods in the bill. Not null.
        date (Date): Stores the date on which the bill was issued. Not null.
        buyer_id (Integer): Foreign key links to the Buyer's ID. Not null.
        product_name (str,50): Foreign key links to the Good's name. Not null.
        buyer (relationship): Establishes a relationship with the Buyer model.
        product (relationship): Establishes a relationship with the Goods model.
        __table_args__: Additional table options, including a composite primary key('date','buyer_id','good_name').
    """
    __tablename__ = 'bill'
    bill_no = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id', name='fk_bill_buyer_id'), nullable=False)
    product_name = db.Column(db.String(50), db.ForeignKey('product.name', name='fk_bill_product_name'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    __table_args__ = (db.PrimaryKeyConstraint(date, buyer_id, product_name, name='pk_bill'),)

    def to_dict(self):
        return {
            'bill_no': self.bill_no,
            'buyer_id': self.buyer_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'date': self.date,
            'remarks': self.remarks,
        }
