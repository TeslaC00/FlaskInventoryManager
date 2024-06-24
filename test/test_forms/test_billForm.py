import os

import pytest
from datetime import date
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy.testing import db

from app import create_app
from app.forms.bill_wtform import SalesForm, ItemForm  # Replace with your actual import

# Sample valid data for the forms
valid_item_data = {
    'name': 'Item 1',
    'rate': Decimal('100.50'),
    'quantity': 10,
}

valid_sales_data = {
    'gst_no': '29ABCDE1234F2Z5',
    'date': date.today(),
    'bill_no': 12345,
    'items': [valid_item_data],
    'sgst': Decimal('9.0'),
    'cgst': Decimal('9.0'),
    'igst': Decimal('0.0'),
}


@pytest.fixture(scope='session')
def app():
    os.environ['FLASK_ENV'] = 'testing'
    load_dotenv()
    app = create_app()

    with app.app_context():
        yield app



@pytest.fixture
def valid_item_form(app):
    with app.app_context():
        return ItemForm(data=valid_item_data)


@pytest.fixture
def valid_sales_form(app):
    with app.app_context():
        return SalesForm(data=valid_sales_data)


class TestBillForm:

    def test_valid_item_form(self, valid_item_form):
        assert valid_item_form.validate() is True

    def test_invalid_item_form_missing_rate(self):
        invalid_data = valid_item_data.copy()
        invalid_data.pop('rate')
        form = ItemForm(data=invalid_data)
        assert form.validate() is False

    def test_invalid_item_form_negative_quantity(self):
        invalid_data = valid_item_data.copy()
        invalid_data['quantity'] = -1
        form = ItemForm(data=invalid_data)
        assert form.validate() is False

    def test_valid_sales_form(self, valid_sales_form):
        assert valid_sales_form.validate() is True

    def test_invalid_sales_form_missing_gst_no(self):
        invalid_data = valid_sales_data.copy()
        invalid_data.pop('gst_no')
        form = SalesForm(data=invalid_data)
        assert form.validate() is False

    def test_invalid_sales_form_with_invalid_item(self):
        invalid_data = valid_sales_data.copy()
        invalid_data['items'][0]['quantity'] = -1  # Invalid quantity in item
        form = SalesForm(data=invalid_data)
        assert form.validate() is False

    def test_invalid_sales_form_with_no_items(self):
        invalid_data = valid_sales_data.copy()
        invalid_data['items'] = []
        form = SalesForm(data=invalid_data)
        assert form.validate() is False

    def test_sales_form_optional_igst(self):
        valid_data = valid_sales_data.copy()
        valid_data['igst'] = Decimal('0.0')  # Optional field set to valid value
        form = SalesForm(data=valid_data)
        assert form.validate() is True

    @pytest.mark.parametrize("sgst, cgst, igst, expected", [
        (Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), True),  # Lower boundary
        (Decimal('100.0'), Decimal('100.0'), Decimal('100.0'), True),  # Upper reasonable boundary
        (Decimal('-1.0'), Decimal('9.0'), Decimal('0.0'), False),  # Invalid SGST
        (Decimal('9.0'), Decimal('-1.0'), Decimal('0.0'), False),  # Invalid CGST
        (Decimal('9.0'), Decimal('9.0'), Decimal('-2.0'), False),  # Invalid IGST
    ])
    def test_sales_form_boundary_values(self, sgst, cgst, igst, expected):
        data = valid_sales_data.copy()
        data['sgst'] = sgst
        data['cgst'] = cgst
        data['igst'] = igst
        form = SalesForm(data=data)
        assert form.validate() == expected
