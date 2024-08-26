from app.extensions import db


class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    materials = db.relationship('Material', backref='unit')  # using dynamic will return a query
    products = db.relationship('Product', backref='unit')
