from app.extensions import db
from enum import Enum


class MaterialScrapType(Enum):
    OK_MATERIAL = 1
    NOT_GOOD = 2
    INTERNAL_REJECTION = 3


class MaterialScrap(db.Model):
    """
    Represents records of scrap generated from raw materials within a relational database,
    modeled using SQLAlchemy ORM as part of the application's database schema. This model is
    designed to track the scrap resulting from the usage or processing of raw materials, helping
    in waste management and cost analysis.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Materials_Scrap model.
        date (Column): The date on which the scrap was recorded. It is of type Date and cannot be null, providing a
        temporal reference for scrap records.
        material_part_no (Column): A foreign key linking to the Raw_Material model based on the raw_material_name. It is a
        string of maximum length 50, denoting the name of the raw material that generated the scrap, and cannot be null.
        scrap_type (Column): Specifies the type of scrap generated. It is a string of maximum length 3, and cannot
        be null. This might denote different categories or conditions of scrap.
        quantity (Column): Stores the quantity of the scrap generated. It is of type Integer and cannot be null,
        representing the volume or amount of waste produced.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting
        of 'date' and 'raw_material_name', ensuring unique scrap records for each raw material on each date.

    The Raw_Materials_Scrap model includes a method `to_dict` which converts the scrap record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Materials_Scrap instance,
        including 'date', 'raw_material_name', 'type_of_scrap', and 'quantity'.
    """

    __tablename__ = 'material_scrap'
    material_part_no = db.Column(db.Integer,
                                 db.ForeignKey('material.part_no', name='fk_material_scrap_material_part_no'),
                                 nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    scrap_type = db.Column(db.Enum(MaterialScrapType), nullable=False)
    date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(date, material_part_no, name='pk_material_scrap'),)

    def to_dict(self):
        """
        Converts the Raw_Materials_Scrap instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Materials_Scrap model's attributes,
            including 'date', 'raw_material_name', 'type_of_scrap', and 'quantity'.
        """
        return {
            'material_part_no': self.material_part_no,
            'date': self.date,
            'scrap_type': self.scrap_type,
            'quantity': self.quantity
        }
