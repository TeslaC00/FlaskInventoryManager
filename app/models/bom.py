import warnings

from app.database import db


@DeprecationWarning
class Bom(db.Model):
    __tablename__ = 'bom'
    product_name = db.Column(db.String(50), db.ForeignKey('product.name', name='fk_bom_product_name'), nullable=False)
    material_name = db.Column(db.String(50), db.ForeignKey('material.name', name='fk_bom_material_name'),
                              nullable=False)
    date = db.Column(db.Date, nullable=False)
    ratio = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(product_name, material_name, name='pk_bom'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn("YourModel is deprecated. Please migrate to a new model.", DeprecationWarning)

    def to_dict(self):
        return {
            'product_name': self.product_name,
            'material_name': self.material_name,
            'date': self.date,
            'ratio': self.ratio
        }

# Query for getting ratio with date
# bom_entry = Bom.query.filter(
#     Bom.good_name == good_name,
#     Bom.raw_material_name == raw_material_name,
#     Bom.date <= desired_date
# ).order_by(Bom.date.desc()).first()
