from app.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class PersonBase(db.model):
    """
        Represents a Person(Buyer, Supplier) record within a relational database, modeled using SQLAlchemy ORM
        as part of the application's database schema.

        Attributes:
            __tablename__ (str): Specifies the name of the table in the database for the Buyer model.
            id (Column): The primary key for the Buyer table. It is an auto-incrementing integer.
            name (Column): Stores the name of the person. It is a non-nullable string of maximum length 50.
            GST_No (Column): Stores the GST number of the person. It is a unique, non-nullable string of maximum length 15.
            state_code (Column): Stores the foreign key of IndianState model associated with the person.

        The Buyer model includes a method `to_dict` which converts the Buyer record into a dictionary,
        facilitating easy JSON serialization for api responses or other purposes.

        Methods:
            to_dict(self): Returns a dictionary representation of the Buyer instance,
            including person_name, GST_No, state_code, state_name, and person_id.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    GST_No = Column(String(15), nullable=False)
    state_code = Column(Integer, ForeignKey('indian_state.id'), nullable=False)
    address = Column(Text, nullable=False)
    state = relationship('IndianState', backref='suppliers', lazy='joined')

    def to_dict(self):
        """
        Converts the Buyer instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Buyer model's attributes,
            including 'person_name', 'GST_No', 'state_code', 'state_name', and 'person_id'.
        """
        return {
            'id': self.id,
            'name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'address': self.address
        }
