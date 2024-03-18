from app import db


class Buyer(db.Model):
    __tablename__ = 'Buyer'
    buyer_name = db.Column(db.String(50), nullable=False)
    GST_No = db.Column(db.String(15), nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    buyer_id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            'buyer_name': self.buyer_name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'state_name': self.state_name,
            'buyer_id': self.buyer_id
        }
