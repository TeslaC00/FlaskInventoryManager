import pytest

from app.models import Buyer, Material, IndianState, Supplier
from app.extensions import db


@pytest.fixture(scope='module')
def new_indian_state():
    indian_state = IndianState(name='Test', abbreviation='T')
    db.session.add(indian_state)
    db.session.commit()
    return indian_state


@pytest.fixture(scope='module')
def new_buyer(new_indian_state):
    buyer = Buyer(name='test', GST_No='123456789012345', state_code=new_indian_state.id, address='test address')
    db.session.add(buyer)
    db.session.commit()
    return buyer


@pytest.fixture(scope='module')
def new_supplier(new_indian_state):
    supplier = Supplier(name='test', GST_No='123456789012345', state_code=new_indian_state.id, address='test address')
    db.session.add(supplier)
    db.session.commit()
    return supplier


@pytest.fixture(scope='module')
def new_material():
    material = Material(part_no=1, name='material', unit_id=1, quantity=10)
    db.session.add(material)
    db.session.commit()
    return material
