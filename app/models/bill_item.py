from sqlalchemy import Column, Integer, ForeignKey, Float
from app.extensions import db


class BillItem(db.Model):
    __tablename__ = 'bill_item'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    c_gst = Column(Float, nullable=False)
    s_gst = Column(Float, nullable=False)
    i_gst = Column(Float, nullable=False, default=0)
    bill_id = Column(Integer, ForeignKey('bill.id'), nullable=False)
    product_part_no = Column(Integer, ForeignKey('product.part_no', name='fk_bill_item_product_part_no'),
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
