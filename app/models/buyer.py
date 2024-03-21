from app.database import db

class Buyer(db.Model):
    """
    Represents a Buyer record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Buyer model.
        buyer_name (db.Column): Stores the name of the buyer. It is a non-nullable string of maximum length 50.
        GST_No (db.Column): Stores the GST number of the buyer. It is a unique, non-nullable string of maximum length 15.
        state_code (db.Column): Stores the state code associated with the buyer. It is a non-nullable integer.
        state_name (db.Column): Stores the name of the state associated with the buyer. It is a non-nullable string of maximum length 30.
        buyer_id (db.Column): The primary key for the Buyer table. It is an auto-incrementing integer.

    The Buyer model includes a method `to_dict` which converts the Buyer record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Buyer instance,
        including buyer_name, GST_No, state_code, state_name, and buyer_id.
    """

    __tablename__ = 'Buyer'
    buyer_name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    buyer_id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        """
        Converts the Buyer instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Buyer model's attributes,
            including 'buyer_name', 'GST_No', 'state_code', 'state_name', and 'buyer_id'.
        """
        return {
            'buyer_name': self.buyer_name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'state_name': self.state_name,
            'buyer_id': self.buyer_id
        }
