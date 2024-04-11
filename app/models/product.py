from app.database import db


class Product(db.Model):
    """
    Represents a Goods record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Goods model.
        name (db.Column): The name of the good, which acts as the primary key for the Goods table. It is a non-nullable string of maximum length 50.
        unit_type (db.Column): Stores the unit type of the goods. It is a non-nullable string of maximum length 10, describing the measurement unit (e.g., kg, liters, etc.).
        quantity (db.Column): Stores the quantity of the goods. It is of type Integer and cannot be null, indicating the current stock quantity.
        part_no (db.Column): Stores the part number of the goods. It is a unique, non-nullable Integer, identifying the specific part.

    The Goods model includes a method `to_dict` which converts the Goods record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Goods instance,
        including 'good_name', 'unit_type', 'quantity', and 'part_no'.
    """

    __tablename__ = 'product'
    name = db.Column(db.String(50), primary_key=True)
    part_no = db.Column(db.Integer, nullable=False, unique=True)
    unit_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    bills = db.relationship('Bill', backref='product')
    product_prices = db.relationship('ProductPrice', backref='product')
    product_returned = db.relationship('ProductReturned', backref='product')
    product_scraps = db.relationship('ProductScrap', backref='product')
    production_logs = db.relationship('ProductionLog', backref='product')

    def to_dict(self):
        """
        Converts the Goods instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Goods model's attributes,
            including 'good_name', 'unit_type', 'quantity', and 'part_no'.
        """
        return {
            'product_name': self.name,
            'part_no': self.part_no,
            'unit_type': self.unit_type,
            'quantity': self.quantity,
        }
