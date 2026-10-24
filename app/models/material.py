from app.database import db


class Material(db.Model):
    """
    Represents a raw material record within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema. This model is designed to maintain information
    about various raw materials used in the production process.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Material model.
        name (db.Column): The name of the raw material, which serves as the primary key for the Raw_Material table. It
        is a non-nullable string of maximum length 50.
        unit_type (db.Column): Specifies the unit of measure for the raw material (e.g., kg, liters). It is a
        non-nullable string of maximum length 10.
        quantity (db.Column): Represents the current stock quantity of the raw material. It is a non-nullable integer,
        indicating how much of the material is available.

    The Raw_Material model includes a method `to_dict` which converts the raw material record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Material instance,
        including 'raw_material_name', 'unit_type', and 'quantity'.
    """

    __tablename__ = 'material'
    name = db.Column(db.String(50), primary_key=True)
    part_no = db.Column(db.Integer, nullable=False, unique=True)
    unit_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    challans = db.relationship('Challan', backref='material')
    material_part_nos = db.relationship('MaterialPartNo', backref='material')
    material_prices = db.relationship('MaterialPrice', backref='material')
    material_scraps = db.relationship('MaterialScrap', backref='material')
    production_logs = db.relationship('ProductionLog', backref='material')

    def to_dict(self):
        """
        Converts the Raw_Material instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Material model's attributes,
            including 'raw_material_name', 'unit_type', and 'quantity'.
        """
        return {
            'material_name': self.name,
            'unit_type': self.unit_type,
            'quantity': self.quantity
        }
