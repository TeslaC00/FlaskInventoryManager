import warnings

from app.database import db


@DeprecationWarning
class Raw_Material_Records(db.Model):
    """
    Represents a record of raw material usage within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema. This model is designed to track the usage of various
    raw materials over time, facilitating inventory management and production planning.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Material_Records model.
        date (db.Column): The date on which the raw materials were used. It is of type Date and cannot be null.
        quantity_used (db.Column): Stores the quantity of the raw material used on the given date. It is of type Integer and cannot be null, representing the consumption of the raw material.
        raw_material_name (db.Column): A foreign key linking to the Raw_Material model based on the raw_material_name. It is a string of maximum length 50, denoting the name of the used raw material.
        raw_material (db.relationship): Defines a relationship between the Raw_Material_Records and Raw_Material models. This allows navigation from a given Raw_Material_Records instance to its associated Raw_Material.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting of 'date' and 'raw_material_name' to ensure unique records for each type of raw material on each date.

    The Raw_Material_Records model includes a method `to_dict` which converts the record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Material_Records instance,
        including 'date', 'quantity_used', and 'raw_material_name'.
    """

    __tablename__ = 'raw_material_records'
    date = db.Column(db.Date, nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('raw_material.raw_material_name'))
    raw_material = db.relationship('raw_material', backref='raw_material_records')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'raw_material_name'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn("YourModel is deprecated. Please migrate to a new model.", DeprecationWarning)

    def to_dict(self):
        """
        Converts the Raw_Material_Records instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Material_Records model's attributes,
            including 'date', 'quantity_used', and 'raw_material_name'.
        """
        return {
            'date': self.date,
            'quantity_used': self.quantity_used,
            'raw_material_name': self.raw_material_name,
        }
