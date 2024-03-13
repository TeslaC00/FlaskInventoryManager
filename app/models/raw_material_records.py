from app import db


class Raw_Material_Records(db.Model):
    __tablename__ = 'Raw_Material_Records'
    date = db.Column(db.Date, nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), db.ForeignKey('Raw_Material.name'))
    raw_material = db.relationship('Raw_Material', backref='raw_material_records')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'name'),)
