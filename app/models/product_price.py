from app.database import db


class ProductPrice(db.Model):
    __tablename__ = 'product_price'
    product_name = db.Column(db.String(50), db.ForeignKey('product.name', name='fk_product_price_product_name'),
                             nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint(product_name, date, name='pk_product_price'),)

    def to_dict(self):
        return {
            'product_name': self.product_name,
            'price': self.price,
            'date': self.date,
        }
