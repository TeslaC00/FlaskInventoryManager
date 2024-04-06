from app.database import db


class MaterialPrice(db.Model):
    __tablename__ = 'material_price'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', name='fk_material_price_supplier_id'),
                            nullable=False)
    material_name = db.Column(db.String(50), db.ForeignKey('material.name', name='fk_material_price_material_name'),
                              nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(material_name, supplier_id, date, name='pk_material_price'),)

    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'material_name': self.material_name,
            'price': self.price,
            'date': self.date
        }
