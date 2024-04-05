from app import db


class Bom(db.Model):
    __tablename__ = 'Bom'
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'), nullable=False)
    raw_material_name = db.Column(db.String(50), db.ForeignKey('Raw_Material.raw_material_name'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ratio = db.Column(db.Integer, nullable=False)
    goods = db.relationship('Goods', backref='bom_good')
    raw_material = db.relationship('Raw_Material', backref='bom_material')
    __table_args__ = (db.PrimaryKeyConstraint('good_name', 'raw_material_name', name='bom_pkey'),)

    def to_dict(self):
        return {
            'good_name': self.good_name,
            'raw_material_name': self.raw_material_name,
            'date': self.date,
            'ratio': self.ratio
        }

# Query for getting ratio with date
# bom_entry = Bom.query.filter(
#     Bom.good_name == good_name,
#     Bom.raw_material_name == raw_material_name,
#     Bom.date <= desired_date
# ).order_by(Bom.date.desc()).first()
