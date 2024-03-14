from app import db


class Raw_Material(db.Model):
    __tablename__ = 'Raw_Material'
    raw_material_name = db.Column(db.String(50), primary_key=True)
    unit_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
