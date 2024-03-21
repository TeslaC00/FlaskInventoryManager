from app.database import db

class Raw_Materials_Scrap(db.Model):
    """
    Represents records of scrap generated from raw materials within a relational database,
    modeled using SQLAlchemy ORM as part of the application's database schema. This model is
    designed to track the scrap resulting from the usage or processing of raw materials, helping
    in waste management and cost analysis.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Materials_Scrap model.
        date (db.Column): The date on which the scrap was recorded. It is of type Date and cannot be null, providing a temporal reference for scrap records.
        raw_material_name (db.Column): A foreign key linking to the Raw_Material model based on the raw_material_name. It is a string of maximum length 50, denoting the name of the raw material that generated the scrap, and cannot be null.
        type_of_scrap (db.Column): Specifies the type of scrap generated. It is a string of maximum length 3, and cannot be null. This might denote different categories or conditions of scrap.
        quantity (db.Column): Stores the quantity of the scrap generated. It is of type Integer and cannot be null, representing the volume or amount of waste produced.
        raw_material (db.relationship): Defines a relationship between the Raw_Materials_Scrap and Raw_Material models. This allows navigation from a given Raw_Materials_Scrap instance to its associated Raw_Material.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting of 'date' and 'raw_material_name', ensuring unique scrap records for each raw material on each date.

    The Raw_Materials_Scrap model includes a method `to_dict` which converts the scrap record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Materials_Scrap instance,
        including 'date', 'raw_material_name', 'type_of_scrap', and 'quantity'.
    """

    __tablename__ = 'Raw_Materials_Scrap'
    date = db.Column(db.Date, nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    type_of_scrap = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    raw_material = db.relationship('Raw_Material', backref='raw_materials_scrap')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'raw_material_name'),)

    def to_dict(self):
        """
        Converts the Raw_Materials_Scrap instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Materials_Scrap model's attributes,
            including 'date', 'raw_material_name', 'type_of_scrap', and 'quantity'.
        """
        return {
            'date': self.date,
            'raw_material_name': self.raw_material_name,
            'type_of_scrap': self.type_of_scrap,
            'quantity': self.quantity
        }
