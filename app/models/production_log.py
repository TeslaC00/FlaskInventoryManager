from datetime import datetime

from app.database import db


class ProductionLog(db.Model):
    __tablename__ = 'production_log'
    id = db.Column(db.Integer, primary_key=True)
    production_date = db.Column(db.Date, nullable=False, default=datetime.now)
    product_name = db.Column(db.String(50), db.ForeignKey('product.name', name='fk_production_log_product_name'),
                             nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    material_name = db.Column(db.String(50), db.ForeignKey('material.name', name='fk_production_log_material_name'),
                              nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'production_date': self.production_date,
            'product_name': self.product_name,
            'quantity_produced': self.quantity_produced,
            'material_name': self.material_name,
            'quantity_used': self.quantity_used
        }
