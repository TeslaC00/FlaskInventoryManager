from app.database import db


class Supplier(db.Model):
    __tablename__ = 'Supplier'
    supplier_name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    supplier_id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            'supplier_name': self.supplier_name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'state_name': self.state_name,
            'supplier_id': self.supplier_id
        }
