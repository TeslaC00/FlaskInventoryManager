from sqlalchemy import Column, Integer, Enum, ForeignKey, Date
from app.extensions import db
from app.models.enums import MaterialScrapType


class MaterialScrap(db.Model):
    __tablename__ = 'material_scrap'
    id = Column(Integer, primary_key=True)
    material_part_no = Column(Integer,
                              ForeignKey('material.part_no', name='fk_material_scrap_material_part_no'),
                              nullable=False)
    quantity = Column(Integer, nullable=False)
    scrap_type = Column(Enum(MaterialScrapType), nullable=False)
    date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'material_part_no': self.material_part_no,
            'date': self.date,
            'scrap_type': self.scrap_type.value,
            'quantity': self.quantity
        }
