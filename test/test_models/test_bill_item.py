import pytest
from app.models import BillItem, Bill, Product


def test_bill_item_creation(session):
    test_bill = session.query(Bill).first()
    test_product = session.query(Product).first()

    bill_item = BillItem(
        quantity=2,
        price=50.0,
        c_gst=5.0,
        s_gst=5.0,
        i_gst=0.0,
        bill_id=test_bill.id,
        product_part_no=test_product.part_no
    )
    session.add(bill_item)
    session.commit()

    assert bill_item.id is not None
    assert bill_item.quantity == 2
    assert bill_item.price == 50.0
    assert bill_item.c_gst == 5.0
    assert bill_item.s_gst == 5.0
    assert bill_item.i_gst == 0.0
    assert bill_item.bill_id == test_bill.id
    assert bill_item.product_part_no == test_product.part_no


def test_to_dict_method(session):
    test_bill = session.query(Bill).first()
    test_product = session.query(Product).first()

    bill_item = BillItem(
        quantity=2,
        price=50.0,
        c_gst=5.0,
        s_gst=5.0,
        i_gst=0.0,
        bill_id=test_bill.id,
        product_part_no=test_product.part_no
    )
    session.add(bill_item)
    session.commit()

    bill_item_dict = bill_item.to_dict()
    assert bill_item_dict['id'] == bill_item.id
    assert bill_item_dict['quantity'] == 2
    assert bill_item_dict['price'] == 50.0
    assert bill_item_dict['c_gst'] == 5.0
    assert bill_item_dict['s_gst'] == 5.0
    assert bill_item_dict['i_gst'] == 0.0
    assert bill_item_dict['bill_id'] == test_bill.id
    assert bill_item_dict['product_part_no'] == test_product.part_no


@pytest.mark.parametrize("field, value", [
    ("quantity", None),
    ("price", None),
    ("c_gst", None),
    ("s_gst", None),
    ("bill_id", None),
    ("product_part_no", None)
])
def test_bill_item_missing_required_fields(session, field, value):
    bill_item_data = {'quantity': 2, 'price': 50.0, 'c_gst': 5.0, 's_gst': 5.0, 'i_gst': 0.0,
                      'bill_id': session.query(Bill).first().id,
                      'product_part_no': session.query(Product).first().part_no, field: value}

    with pytest.raises(ValueError):
        bill_item = BillItem(**bill_item_data)
        session.add(bill_item)
        session.commit()


def test_bill_item_relationship_with_bill(session):
    test_bill = session.query(Bill).first()
    test_product = session.query(Product).first()

    bill_item = BillItem(
        quantity=2,
        price=50.0,
        c_gst=5.0,
        s_gst=5.0,
        i_gst=0.0,
        bill_id=test_bill.id,
        product_part_no=test_product.part_no
    )
    session.add(bill_item)
    session.commit()

    assert bill_item.bill.id == test_bill.id
    assert bill_item.bill.purchase_order == 'PO123456'


def test_bill_item_relationship_with_product(session):
    test_bill = session.query(Bill).first()
    test_product = session.query(Product).first()

    bill_item = BillItem(
        quantity=2,
        price=50.0,
        c_gst=5.0,
        s_gst=5.0,
        i_gst=0.0,
        bill_id=test_bill.id,
        product_part_no=test_product.part_no
    )
    session.add(bill_item)
    session.commit()

    assert bill_item.product.part_no == test_product.part_no
    assert bill_item.product.name == 'test_product'
