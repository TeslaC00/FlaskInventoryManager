from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.extensions import db


class Product(db.Model):
    """
    Represents a Goods record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.
    weight-gram,length-cm,pieces

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Goods model.
        name (Column): The name of the good, which acts as the primary key for the Goods table. It is a non-nullable string of maximum length 50.
        unit (Column): Stores the unit type of the goods. It is a non-nullable string of maximum length 10, describing the measurement unit (e.g., kg, liters, etc.).
        quantity (Column): Stores the quantity of the goods. It is of type Integer and cannot be null, indicating the current stock quantity.
        part_no (Column): Stores the part number of the goods. It is a unique, non-nullable Integer, identifying the specific part.

    The Goods model includes a method `to_dict` which converts the Goods record into a dictionary,
    facilitating easy JSON serialization for api responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Goods instance,
        including 'good_name', 'unit_type', 'quantity', and 'part_no'.
    """

    __tablename__ = 'product'
    part_no = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    c_gst = Column(Float, nullable=False)
    s_gst = Column(Float, nullable=False)
    i_gst = Column(Float, nullable=False)
    bill_items = relationship('BillItem', backref='product')
    scraps = relationship('ProductScrap', backref='product')
    materials = relationship('Material', secondary='product_material', backref='products')

    def to_dict(self):
        """
        Converts the Goods instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Goods model's attributes,
            including 'good_name', 'unit_type', 'quantity', and 'part_no'.
        """
        return {
            'part_no': self.part_no,
            'name': self.name,
            'unit_id': self.unit_id,
            'quantity': self.quantity,
            'price': self.price,
            'c_gst': self.c_gst,
            's_gst': self.s_gst,
            'i_gst': self.i_gst
        }
