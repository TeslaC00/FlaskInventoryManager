from app.database import db

class Bill(db.Model):
    """
    Represents a Bill record within a relational database,
    modeled using SQLAlchemy ORM as part of the application's database schema.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        price (db.Column): Stores the price of the goods in the bill. It is of type Integer and cannot be null.
        bill_no (db.Column): Stores the bill number. It is of type Integer and cannot be null.
        quantity (db.Column): Stores the quantity of goods in the bill. It is of type Integer and cannot be null.
        date (db.Column): Stores the date on which the bill was issued. It is of type Date and cannot be null.
        buyer_id (db.Column): Foreign key linking to the Buyer's ID. It is of type Integer, cannot be null, and establishes a relationship with the Buyer table.
        good_name (db.Column): Foreign key linking to the Goods' name. It is of type String with a maximum of 50 characters, cannot be null, and establishes a relationship with the Goods table.
        buyer (db.relationship): Defines a relationship between the Bill and Buyer models. This allows navigation from a given Bill to its associated Buyer.
        goods (db.relationship): Defines a relationship between the Bill and Goods models. This allows navigation from a given Bill to the related Goods.
        __table_args__: Defines additional table options, including a composite primary key consisting of 'date', 'buyer_id', and 'good_name'.

    This model is part of a larger database schema and interacts with the Buyer and Goods models through its foreign keys and relationships.
    The composite primary key ensures that each bill record is unique based on the combination of date, buyer_id, and good_name.
    """
    __tablename__ = 'Bill'
    price = db.Column(db.Integer, nullable=False)
    bill_no = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('Buyer.buyer_id'), nullable=False)
    good_name = db.Column(db.String(50), db.ForeignKey('Goods.good_name'), nullable=False)
    buyer = db.relationship('Buyer', backref='bills')
    goods = db.relationship('Goods', backref='bills')
    __table_args__ = (db.PrimaryKeyConstraint('date', 'buyer_id', 'good_name', name='bill_pkey'),)
