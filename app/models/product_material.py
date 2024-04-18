from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint


class ProductMaterial(db.Model):
    __tablename__ = 'product_material'
    product_part_no = Column(Integer,
                             ForeignKey('product.part_no', name='fk_product_material_product_part_no'),
                             nullable=False)
    material_part_no = Column(Integer,
                              ForeignKey('material.part_no', name='fk_product_material_material_part_no'),
                              nullable=False)
    quantity = Column(Integer, nullable=False)
    __table_args__ = (PrimaryKeyConstraint('product_part_no', 'material_part_no', name='pk_product_material'),)

    def to_dict(self):
        return {
            'product_part_no': self.product_part_no,
            'material_part_no': self.material_part_no,
            'quantity': self.quantity
        }
