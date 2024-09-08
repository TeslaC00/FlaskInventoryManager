from sqlalchemy.orm import relationship
from app.models.person_base import PersonBase


class Supplier(PersonBase):
    __tablename__ = 'supplier'
    # supplier relationship with challan using 'challans' -> both does automatic join (eager loading)
    # challan relationship with supplier using 'supplier'(backref)
    challans = relationship('Challan', backref='supplier', lazy=True)
