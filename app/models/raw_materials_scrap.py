from app.database import db


class Raw_Materials_Scrap(db.Model):
    __tablename__ = 'Raw_Materials_Scrap'
    date = db.Column(db.Date, nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    type_of_scrap = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    raw_material = db.relationship('Raw_Material', backref='raw_materials_scrap')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'raw_material_name'),)

    def to_dict(self):
        return {
            'date': self.date,
            'raw_material_name': self.raw_material_name,
            'type_of_scrap': self.type_of_scrap,
            'quantity': self.quantity
        }
