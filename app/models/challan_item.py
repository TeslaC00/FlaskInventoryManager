from app.database import db


class ChallanItem(db.Model):
    __tablename__ = 'challan_item'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    challan_id = db.Column(db.Integer, db.ForeignKey('challan.id'), nullable=False)
    material_part_no = db.Column(db.Integer, db.ForeignKey('material.part_no', name='fk_challan_item_material_part_no'),
                                 nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'quantity': self.quantity,
            'challan_id': self.challan_id,
            'material_part_no': self.material_part_no
        }
