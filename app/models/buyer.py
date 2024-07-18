from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class Buyer(db.Model):
    """
    Represents a Buyer record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Buyer model.
        name (Column): Stores the name of the buyer. It is a non-nullable string of maximum length 50.
        GST_No (Column): Stores the GST number of the buyer. It is a unique, non-nullable string of maximum length 15.
        state_code (Column): Stores the state code associated with the buyer. It is a non-nullable integer.
        state_name (Column): Stores the name of the state associated with the buyer. It is a non-nullable string of maximum length 30.
        id (Column): The primary key for the Buyer table. It is an auto-incrementing integer.

    The Buyer model includes a method `to_dict` which converts the Buyer record into a dictionary,
    facilitating easy JSON serialization for api responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Buyer instance,
        including buyer_name, GST_No, state_code, state_name, and buyer_id.
    """

    __tablename__ = 'buyer'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    GST_No = Column(String(15), nullable=False)
    state_code = Column(Integer, ForeignKey('indian_state.id'), nullable=False)
    address = Column(Text, nullable=False)
    bills = relationship('Bill', backref='buyer', lazy=True)
    state = relationship('IndianState', backref='buyers', lazy=True)

    def to_dict(self):
        """
        Converts the Buyer instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Buyer model's attributes,
            including 'buyer_name', 'GST_No', 'state_code', 'state_name', and 'buyer_id'.
        """
        return {
            'id': self.id,
            'name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'address': self.address
        }
