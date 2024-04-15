from datetime import datetime

from app.database import db


class ProductionLog(db.Model):
    __tablename__ = 'production_log'
    id = db.Column(db.Integer, primary_key=True)
    production_date = db.Column(db.Date, nullable=False, default=datetime.now)
    product_part_no = db.Column(db.Integer,
                                db.ForeignKey('product.part_no', name='fk_production_log_product_part_no'),
                                nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'production_date': self.production_date,
            'product_part_no': self.product_part_no,
            'quantity_produced': self.quantity_produced
        }
