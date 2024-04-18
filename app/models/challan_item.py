from sqlalchemy import Column, Integer, ForeignKey, Float
from app.extensions import db


class ChallanItem(db.Model):
    __tablename__ = 'challan_item'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    challan_id = Column(Integer, ForeignKey('challan.id'), nullable=False)
    material_part_no = Column(Integer, ForeignKey('material.part_no', name='fk_challan_item_material_part_no'),
                              nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'quantity': self.quantity,
            'challan_id': self.challan_id,
            'material_part_no': self.material_part_no
        }
