import pytest
from datetime import date
from app.models import Bill, Buyer, BillItem


def test_bill_creation(session):
    test_buyer = session.query(Buyer).first()

    bill = Bill(
        buyer_id=test_buyer.id,
        total_price=100.0,
        date=date.today(),
        purchase_order='PO123456'
    )
    session.add(bill)
    session.commit()

    assert bill.id is not None
    assert bill.buyer_id == test_buyer.id
    assert bill.total_price == 100.0
    assert bill.date == date.today()
    assert bill.purchase_order == 'PO123456'


def test_to_dict_method(session):
    test_buyer = session.query(Buyer).first()

    bill = Bill(
        buyer_id=test_buyer.id,
        total_price=100.0,
        date=date.today(),
        purchase_order='PO123456'
    )
    session.add(bill)
    session.commit()

    bill_dict = bill.to_dict()
    assert bill_dict['id'] == bill.id
    assert bill_dict['total_price'] == 100.0
    assert bill_dict['date'] == date.today()
    assert bill_dict['buyer_id'] == test_buyer.id
    assert bill_dict['purchase_order'] == 'PO123456'


@pytest.mark.parametrize("field, value", [
    ("buyer_id", None),
    ("total_price", None),
    ("date", None),
    ("purchase_order", None)
])
def test_bill_missing_required_fields(session, field, value):
    bill_data = {'buyer_id': session.query(Buyer).first().id, 'total_price': 100.0, 'date': date.today(),
                 'purchase_order': 'PO123456', field: value}

    with pytest.raises(ValueError):
        bill = Bill(**bill_data)
        session.add(bill)
        session.commit()


def test_bill_relationship_with_buyer(session):
    test_buyer = session.query(Buyer).first()

    bill = Bill(
        buyer_id=test_buyer.id,
        total_price=100.0,
        date=date.today(),
        purchase_order='PO123456'
    )
    session.add(bill)
    session.commit()

    assert bill.buyer.id == test_buyer.id
    assert bill.buyer.name == 'test_buyer'


def test_bill_relationship_with_bill_items(session):
    test_buyer = session.query(Buyer).first()

    bill = Bill(
        buyer_id=test_buyer.id,
        total_price=100.0,
        date=date.today(),
        purchase_order='PO123456'
    )
    session.add(bill)
    session.commit()

    bill_item = BillItem(
        bill_id=bill.id,
        product_name='test_goods',
        quantity=2,
        price=50.0
    )
    session.add(bill_item)
    session.commit()

    assert bill.bill_items[0].id == bill_item.id
    assert bill.bill_items[0].quantity == 2
    assert bill.bill_items[0].price == 50.0
