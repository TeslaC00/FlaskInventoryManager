from app import db


class Challan(db.Model):
    __tablename__ = 'Challan'
    price = db.Column(db.Integer, nullable=False)
    challan_no = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Supplier.supplier_id'), nullable=False)
    name = db.Column(db.String(50), db.ForeignKey('Raw_Material.name'), nullable=False)
    supplier = db.relationship('Supplier', backref='challans')
    raw_material = db.relationship('Raw_Material', backref='challans')
    __table_args__ = (db.PrimaryKeyConstraint('date','supplier_id','name',name='challan_pkey'),)
