from app.database import db


class Supplier(db.Model):
    """
    Represents a supplier entity within a relational database, modeled using SQLAlchemy ORM as part
    of the application's database schema. This model is designed to store and manage information
    about suppliers who provide raw materials or goods to the business. It includes details such
    as the supplier's name, GST number, and location.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Supplier model.
        name (db.Column): Stores the name of the supplier. It is a string of maximum length 50 characters and cannot be null.
        GST_No (db.Column): Holds the GST (Goods and Services Tax) number of the supplier, which is a unique identifier for businesses in India. It is a string of length 15 characters and cannot be null.
        state_code (db.Column): Contains the state code where the supplier is located. It is an integer representing a specific state within the country, and cannot be null.
        state_name (db.Column): The name of the state where the supplier operates. It is a string of maximum length 30 characters and cannot be null.
        id (db.Column): A unique identifier for the supplier within the database. It is an integer and serves as the primary key for the Supplier table.

    The Supplier model includes a method `to_dict` which converts the supplier entity into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Supplier instance, including
        'supplier_name', 'GST_No', 'state_code', 'state_name', and 'supplier_id'.
    """

    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    challans = db.relationship('challan', backref='supplier')
    material_part_nos = db.relationship('material_part_no', backref='supplier')
    material_prices = db.relationship('material_price', backref='supplier')

    def to_dict(self):
        """
        Converts the Supplier instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Supplier model's attributes, including
            'supplier_name', 'GST_No', 'state_code', 'state_name', and 'supplier_id'.
        """
        return {
            'supplier_id': self.id,
            'supplier_name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'state_name': self.state_name,
        }
