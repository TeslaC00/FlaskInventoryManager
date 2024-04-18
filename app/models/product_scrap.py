from app.extensions import db
from sqlalchemy import Column, Integer, Enum, ForeignKey, PrimaryKeyConstraint, Date
import enum


class ProductScrapType(enum.Enum):
    OK_MATERIAL = 'ok_material'
    NOT_GOOD = 'not_good'
    INTERNAL_REJECTION = 'internal_rejection'
    EXTERNAL_REJECTION = 'external_rejection'


class ProductScrap(db.Model):
    """
    Represents a record of scrapped goods within a relational database, modeled using SQLAlchemy ORM
    as part of the application's database schema. This model is designed to track goods that are identified
    as scrap or waste during production or after quality checks.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database for the Goods_Scrap model.
        date (Column): The date on which the goods were identified as scrap. It is of type Date and cannot be null.
        product_part_no (Column): A foreign key linking to the Goods model based on the good_name. It indicates the name of the good that was scrapped. It is a string of maximum length 50 and cannot be null.
        quantity (Column): Stores the quantity of the scrapped goods. It is of type Integer and cannot be null, representing how many units of the good were scrapped.
        product (relationship): Defines a relationship between the Goods_Scrap and Goods models. This allows navigation from a given Goods_Scrap instance to its associated Goods.
        __table_args__ (tuple): Defines additional table options. Here, it specifies a composite primary key consisting of 'date' and 'good_name' to ensure unique records for each type of good on each date.

    The Goods_Scrap model includes a method `to_dict` which converts the record into a dictionary,
    facilitating easy JSON serialization for API responses or other purposes.

    Methods:
        to_dict(self): Returns a dictionary representation of the Goods_Scrap instance,
        including 'date', 'good_name', and 'quantity'.
    """

    __tablename__ = 'product_scrap'
    product_part_no = Column(Integer, ForeignKey('product.part_no', name='fk_product_scrap_product_part_no'),
                             nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    scrap_type = Column(Enum(ProductScrapType), nullable=False)
    __table_args__ = (PrimaryKeyConstraint('date', 'product_part_no', name='pk_product_scrap'),)

    def to_dict(self):
        """
        Converts the Goods_Scrap instance into a dictionary.

        Returns:
            dict: A dictionary with keys corresponding to the Goods_Scrap model's attributes,
            including 'date', 'good_name', and 'quantity'.
        """
        return {
            'part_no': self.product_part_no,
            'date': self.date,
            'quantity': self.quantity,
            'scrap_type': self.scrap_type.name
        }
