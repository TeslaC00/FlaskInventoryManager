from app.database import db


class Raw_Materials_Part_No(db.Model):
    __tablename__ = 'Raw_Materials_Part_No'
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.supplier_id'), nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    part_no = db.Column(db.Integer, nullable=False)
    supplier = db.relationship('Supplier', backref='part_no')
    raw_material = db.relationship('Raw_Material', backref='part_no')
    __table_args__ = (db.PrimaryKeyConstraint('supplier_id', 'raw_material_name'),)

    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'raw_material_name': self.raw_material_name,
            'part_no': self.part_no,
        }
