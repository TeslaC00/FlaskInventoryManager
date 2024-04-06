import warnings

from app.database import db


@DeprecationWarning
class Goods_Records(db.Model):
    """
    Represents a Goods_Records record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema. This model is designed to track the production
    records of goods over time.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Goods_Records model.
        date (db.Column): The date on which the goods were produced or recorded. It is of type Date and cannot be null.
        quantity_produced (db.Column): Stores the quantity of goods produced on the given date. It is of type Integer and cannot be null.
        good_name (db.Column): A foreign key linking to the Goods model based on the good_name. It is a string of maximum length 50.
        goods (db.relationship): Defines a relationship between the Goods_Records and Goods models. This allows navigation from a given Goods_Records instance to its associated Goods.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting of 'date' and 'good_name' to ensure unique records for each good on each date.

    The Goods_Records model includes a method `to_dict` which converts the record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Goods_Records instance,
        including 'date', 'quantity_produced', and 'good_name'.
    """

    __tablename__ = 'goods_records'
    date = db.Column(db.Date, nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('goods.good_name'))
    goods = db.relationship('goods', backref='goods_records')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'good_name'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn("YourModel is deprecated. Please migrate to a new model.", DeprecationWarning)

    def to_dict(self):
        """
        Converts the Goods_Records instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Goods_Records model's attributes,
            including 'date', 'quantity_produced', and 'good_name'.
        """
        return {
            'date': self.date,
            'quantity_produced': self.quantity_produced,
            'product_name': self.good_name
        }
