from app.database import db


class Challan(db.Model):
    """
    Represents a Challan record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Challan model.
        price (db.Column): Stores the price of the raw material in the challan. It is of type Integer and cannot be null.
        challan_no (db.Column): Stores the challan number. It is of type Integer and cannot be null.
        date (db.Column): Stores the date on which the challan was issued. It is of type Date and cannot be null.
        quantity (db.Column): Stores the quantity of raw material in the challan. It is of type Integer and cannot be null.
        supplier_id (db.Column): Foreign key linking to the Supplier's ID. It is of type Integer, cannot be null, and establishes a relationship with the Supplier table.
        raw_material_name (db.Column): Foreign key linking to the Raw Material's name. It is of type String with a maximum of 50 characters, cannot be null, and establishes a relationship with the Raw_Material table.
        supplier (db.relationship): Defines a relationship between the Challan and Supplier models. This allows navigation from a given Challan to its associated Supplier.
        raw_material (db.relationship): Defines a relationship between the Challan and Raw_Material models. This allows navigation from a given Challan to the related Raw Material.
        __table_args__: Defines additional table options, including a composite primary key consisting of 'date', 'supplier_id', and 'raw_material_name'.

    The Challan model includes a method `to_dict` which converts the Challan record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Challan instance,
        including 'price', 'challan_no', 'date', 'quantity', 'supplier_id', and 'raw_material_name'.
    """

    __tablename__ = 'Challan'
    price = db.Column(db.Integer, nullable=False)
    challan_no = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.supplier_id'), nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    supplier = db.relationship('Supplier', backref='challans')
    raw_material = db.relationship('Raw_Material', backref='challans')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'supplier_id', 'raw_material_name', name='challan_pkey'),)

    def to_dict(self):
        """
        Converts the Challan instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Challan model's attributes,
            including 'price', 'challan_no', 'date', 'quantity', 'supplier_id', and 'raw_material_name'.
        """
        return {
            'price': self.price,
            'challan_no': self.challan_no,
            'date': self.date,
            'quantity': self.quantity,
            'supplier_id': self.supplier_id,
            'raw_material_name': self.raw_material_name
        }
