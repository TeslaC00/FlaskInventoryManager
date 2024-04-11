from app.database import db


class MaterialPartNo(db.Model):
    """
    Represents a mapping between raw materials and their part numbers from specific suppliers,
    within a relational database, modeled using SQLAlchemy ORM as part of the application's
    database schema. This model facilitates the tracking of raw materials by their unique part numbers
    as provided by different suppliers, enhancing inventory management and procurement processes.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Raw_Materials_Part_No model.
        supplier_id (db.Column): A foreign key that links to the Supplier model based on the supplier_id. It is of type
        Integer and cannot be null, identifying the supplier of the raw material.
        material_name (db.Column): A foreign key linking to the Raw_Material model based on the raw_material_name. It is
        a string of maximum length 50, denoting the name of the raw material, and cannot be null.
        part_no (db.Column): Stores the part number assigned to the raw material by the supplier. It is of type Integer
        and cannot be null, providing a unique identifier for the raw material as recognized by the supplier.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting
        of 'supplier_id' and 'raw_material_name' to ensure unique mappings between suppliers, raw materials, and part
        numbers.

    The Raw_Materials_Part_No model includes a method `to_dict` which converts the mapping into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Raw_Materials_Part_No instance,
        including 'supplier_id', 'raw_material_name', and 'part_no'.
    """

    __tablename__ = 'material_part_no'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', name='fk_material_part_no_supplier_id'),
                            nullable=False)
    material_name = db.Column(db.String(50), db.ForeignKey('material.name', name='fk_material_part_no_material_name'),
                              nullable=False)
    part_no = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(supplier_id, material_name, name='pk_materials_part_no'),)

    def to_dict(self):
        """
        Converts the Raw_Materials_Part_No instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Raw_Materials_Part_No model's attributes,
            including 'supplier_id', 'raw_material_name', and 'part_no'.
        """
        return {
            'supplier_id': self.supplier_id,
            'material_name': self.material_name,
            'part_no': self.part_no,
        }
