from app.extensions import db


class BillItem(db.Model):
    __tablename__ = 'bill_item'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    c_gst = db.Column(db.Float, nullable=False)
    s_gst = db.Column(db.Float, nullable=False)
    i_gst = db.Column(db.Float, nullable=False, default=0)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    product_part_no = db.Column(db.Integer, db.ForeignKey('product.part_no', name='fk_bill_item_product_part_no'),
                                nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'c_gst': self.c_gst,
            's_gst': self.s_gst,
            'i_gst': self.i_gst,
            'bill_id': self.bill_id,
            'product_part_no': self.product_part_no
        }
