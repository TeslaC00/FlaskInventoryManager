from app.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class PersonBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    GST_No = Column(String(15), nullable=False)
    state_code = Column(Integer, ForeignKey('indian_state.id'), nullable=False)
    address = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'GST_No': self.GST_No,
            'state_code': self.state_code,
            'address': self.address
        }
