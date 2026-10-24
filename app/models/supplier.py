from app.database import db


class Supplier(db.Model):

    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    challans = db.relationship('Challan', backref='supplier')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'state_name': self.state_name,
            'address': self.address,
        }
