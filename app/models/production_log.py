from datetime import datetime
from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey, Date


class ProductionLog(db.Model):
    __tablename__ = 'production_log'
    id = Column(Integer, primary_key=True)
    production_date = Column(Date, nullable=False, default=datetime.now)
    product_part_no = Column(Integer,
                             ForeignKey('product.part_no', name='fk_production_log_product_part_no'),
                             nullable=False)
    quantity_produced = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'production_date': self.production_date,
            'product_part_no': self.product_part_no,
            'quantity_produced': self.quantity_produced
        }
