from app.database import db


class ProductReturned(db.Model):
    """
    Represents records of goods returned by buyers, encapsulated within a relational database
    using SQLAlchemy ORM. This model is crucial for tracking returns, analyzing return rates,
    and managing inventory effectively.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Returned_Good model.
        date (db.Column): The date on which the good was returned. It is of type Date and cannot be null, serving as a key part of identifying a return record.
        quantity (db.Column): The quantity of the good returned. It is of type Integer and cannot be null, indicating how much of the product was returned.
        buyer_id (db.Column): A foreign key linking to the Buyer model based on the buyer_id. It cannot be null and helps in identifying which buyer returned the goods.
        product_name (db.Column): A foreign key linking to the Goods model based on the good_name. It is a string of maximum length 50, denoting the name of the good that was returned, and cannot be null.
        buyer (db.relationship): Establishes a relationship with the Buyer model, allowing navigation from a given return record to its associated buyer.
        product (db.relationship): Establishes a relationship with the Goods model, facilitating access from a return record to the detailed information of the returned good.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting of 'date', 'good_name', and 'buyer_id', ensuring unique return records for each combination of date, good, and buyer.

    The Returned_Good model includes a method `to_dict` which allows for the conversion of return records into a dictionary format,
    simplifying the process of JSON serialization for API responses or other data exchange purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Returned_Good instance, including keys for 'date', 'quantity', 'buyer_id', and 'good_name'.
    """

    __tablename__ = 'product_returned'
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id', name='fk_product_returned_buyer_id'), nullable=False)
    product_name = db.Column(db.String(50), db.ForeignKey('product.name', name='fk_product_returned_product_name'),
                             nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(date, product_name, buyer_id, name='pk_good_returned'),)

    def to_dict(self):
        """
        Converts the Returned_Good instance into a dictionary format for easier serialization.

        Returns:
            dict: A dictionary containing the return record details, with keys for 'date', 'quantity', 'buyer_id', and 'good_name'.
        """
        return {
            'buyer_id': self.buyer_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'date': self.date,
        }
