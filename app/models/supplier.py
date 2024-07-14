from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class Supplier(db.Model):
    """
    Represents a supplier entity within a relational database, modeled using SQLAlchemy ORM as part
    of the application's database schema. This model is designed to store and manage information
    about suppliers who provide raw materials or goods to the business. It includes details such
    as the supplier's name, GST number, and location.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Supplier model.
        name (Column): Stores the name of the supplier. It is a string of maximum length 50 characters and cannot be null.
        GST_No (Column): Holds the GST (Goods and Services Tax) number of the supplier, which is a unique identifier for businesses in India. It is a string of length 15 characters and cannot be null.
        state_code (Column): Contains the state code where the supplier is located. It is an integer representing a specific state within the country, and cannot be null.
        state_name (Column): The name of the state where the supplier operates. It is a string of maximum length 30 characters and cannot be null.
        id (Column): A unique identifier for the supplier within the database. It is an integer and serves as the primary key for the Supplier table.

    The Supplier model includes a method `to_dict` which converts the supplier entity into a dictionary,
    facilitating easy JSON serialization for api responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Supplier instance, including
        'supplier_name', 'GST_No', 'state_code', 'state_name', and 'supplier_id'.
    """

    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    GST_No = Column(String(15), nullable=False)
    state_code = Column(Integer, ForeignKey('indian_state.code'), nullable=False)
    address = Column(Text, nullable=False)
    # supplier relationship with challan using 'challans' -> both does automatic join (eager loading)
    # challan relationship with supplier using 'supplier'(backref)
    challans = relationship('Challan', backref='supplier')
    state = relationship('IndianState', backref='suppliers', lazy=True)

    def to_dict(self):
        """
        Converts the Supplier instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Supplier model's attributes, including
            'supplier_name', 'GST_No', 'state_code', 'state_name', and 'supplier_id'.
        """
        return {
            'id': self.id,
            'name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'address': self.address
        }
