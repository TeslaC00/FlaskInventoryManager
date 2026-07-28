from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from app.extensions import db


class Challan(db.Model):
    """
    Represents a Challan record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Challan model.
        total_price (Column): Stores the price of the raw material in the challan. It is of type Integer and cannot be
        null.
        challan_no (Column): Stores the challan number. It is of type Integer and cannot be null.
        date (Column): Stores the date on which the challan was issued. It is of type Date and cannot be null.
        supplier_id (Column): Foreign key linking to the Supplier's ID. It is of type Integer, cannot be null, and
        establishes a relationship with the Supplier table.

    The Challan model includes a method `to_dict` which converts the Challan record into a dictionary,
    facilitating easy JSON serialization for api responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Challan instance,
        including 'price', 'challan_no', 'date', 'quantity', 'supplier_id', and 'raw_material_name'.
    """

    __tablename__ = 'challan'
    id = Column(Integer, primary_key=True)
    challan_no = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id', name='fk_challan_supplier_id'), nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    remarks = Column(Text, nullable=True)
    # Challan relationship with ChallanItem using 'challan_items' -> both does automatic join (eager loading)
    # ChallanItem relationship with Challan using 'challan'(backref)
    challan_items = relationship('ChallanItem', backref='challan')

    def to_dict(self):
        """
        Converts the Challan instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Challan model's attributes,
            including 'price', 'challan_no', 'date', 'quantity', 'supplier_id', and 'raw_material_name'.
        """
        return {
            'id': self.id,
            'challan_no': self.challan_no,
            'supplier_id': self.supplier_id,
            'total_price': self.total_price,
            'date': self.date,
            'remarks': self.remarks
        }
