from sqlalchemy.orm import relationship
from app.models.person_base import PersonBase


class Buyer(PersonBase):
    __tablename__ = 'buyer'
    bills = relationship('Bill', backref='buyer', lazy=True)
