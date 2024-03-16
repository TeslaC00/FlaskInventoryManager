from app import db


class Raw_Materials_Scrap(db.Model):
    __tablename__ = 'Raw_Materials_Scrap'
    date = db.Column(db.Date, nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    type_of_scrap = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    raw_material = db.relationship('Raw_Material', backref='raw_materials_scrap')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'raw_material_name'),)
