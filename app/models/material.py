from app.database import db
from enum import Enum


class UnitType(Enum):
    GRAM = 1,
    CENTIMETER = 2,
    PIECE = 3


class Material(db.Model):
    """
    Represents a raw material record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema. This model is designed to maintain information
    about various raw materials used in the production process.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Material model.
        name (db.Column): The name of the raw material, which serves as the primary key for the Raw_Material table. It is a non-nullable string of maximum length 50.
        unit (db.Column): Specifies the unit of measure for the raw material (e.g., kg, liters). It is a non-nullable string of maximum length 10.
        quantity (db.Column): Represents the current stock quantity of the raw material. It is a non-nullable integer, indicating how much of the material is available.

    The Raw_Material model includes a method `to_dict` which converts the raw material record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Material instance,
        including 'raw_material_name', 'unit_type', and 'quantity'.
    """

    __tablename__ = 'material'
    part_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    unit = db.Column(db.Enum(UnitType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    challan_items = db.relationship('ChallanItem', backref='material')
    scraps = db.relationship('MaterialScrap', backref='material')

    def to_dict(self):
        """
        Converts the Raw_Material instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Material model's attributes,
            including 'raw_material_name', 'unit_type', and 'quantity'.
        """
        return {
            'part_no': self.part_no,
            'name': self.name,
            'unit': self.unit,
            'quantity': self.quantity
        }
