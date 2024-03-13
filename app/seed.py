# seed.py

import random
import string
from datetime import datetime

from app import db, create_app
from app.models import Bill, Buyer, Challan, Goods, Goods_Records, Raw_Material, Raw_Material_Records, Returned_Good, \
    Supplier, User, Write_off

app = create_app()
app.app_context().push()


# Function to generate a random string
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Function to seed the database
def seed():
    # Seed Suppliers
    supplier_data = [
        {'name': 'Supplier A', 'GST_No': 'ABCD1234', 'state_code': 1, 'state_name': 'State 1', 'supplier_id': 1},
        {'name': 'Supplier B', 'GST_No': 'EFGH5678', 'state_code': 2, 'state_name': 'State 2', 'supplier_id': 2}
        # Add more suppliers as needed
    ]
    for data in supplier_data:
        supplier = Supplier(**data)
        db.session.add(supplier)

    # Seed Buyers
    buyer_data = [
        {'name': 'Buyer X', 'GST_No': 'IJKL9012', 'state_code': 3, 'state_name': 'State 3', 'buyer_id': 1},
        {'name': 'Buyer Y', 'GST_No': 'MNOP3456', 'state_code': 4, 'state_name': 'State 4', 'buyer_id': 2}
        # Add more buyers as needed
    ]
    for data in buyer_data:
        buyer = Buyer(**data)
        db.session.add(buyer)

    # Seed Raw Materials
    raw_material_data = [
        {'name': 'Raw Material 1', 'unit_type': 'kg', 'quantity': 100},
        {'name': 'Raw Material 2', 'unit_type': 'liter', 'quantity': 200}
        # Add more raw materials as needed
    ]
    for data in raw_material_data:
        raw_material = Raw_Material(**data)
        db.session.add(raw_material)

    # Seed Goods
    goods_data = [
        {'name': 'Product A', 'unit_type': 'unit', 'quantity': 50},
        {'name': 'Product B', 'unit_type': 'unit', 'quantity': 100}
        # Add more goods as needed
    ]
    for data in goods_data:
        goods = Goods(**data)
        db.session.add(goods)

    # Seed Users
    user_data = [
        {'Username': 'user1', 'password': 'password1', 'user_type': 'admin'},
        {'Username': 'user2', 'password': 'password2', 'user_type': 'regular'}
        # Add more users as needed
    ]
    for data in user_data:
        user = User(**data)
        db.session.add(user)

    # Seed Write Off
    write_off_data = [
        {'write_offs': 'Write Off 1'},
        {'write_offs': 'Write Off 2'}
        # Add more write off as needed
    ]
    for data in write_off_data:
        write_off = Write_off(**data)
        db.session.add(write_off)

    # Seed Raw Material Records
    raw_material_records_data = [
        {'date': datetime(2024, 3, 1), 'quantity_used': 20, 'name': 'Raw Material 1'},
        {'date': datetime(2024, 3, 2), 'quantity_used': 30, 'name': 'Raw Material 2'}
        # Add more raw material records as needed
    ]
    for data in raw_material_records_data:
        raw_material_record = Raw_Material_Records(**data)
        db.session.add(raw_material_record)

    # Seed Goods Records
    goods_records_data = [
        {'date': datetime(2024, 3, 1), 'quantity_produced': 10, 'name': 'Product A'},
        {'date': datetime(2024, 3, 2), 'quantity_produced': 20, 'name': 'Product B'}
        # Add more goods records as needed
    ]
    for data in goods_records_data:
        goods_record = Goods_Records(**data)
        db.session.add(goods_record)

    # Seed Challans
    challan_data = [
        {'price': 50, 'challan_no': 123, 'date': datetime(2024, 3, 1), 'quantity': 10, 'supplier_id': 1,
         'name': 'Raw Material 1'},
        {'price': 100, 'challan_no': 456, 'date': datetime(2024, 3, 2), 'quantity': 20, 'supplier_id': 2,
         'name': 'Raw Material 2'}
        # Add more challans as needed
    ]
    for data in challan_data:
        challan = Challan(**data)
        db.session.add(challan)

    # Seed Bills
    bill_data = [
        {'price': 200, 'bill_no': 789, 'quantity': 5, 'date': datetime(2024, 3, 1), 'buyer_id': 1, 'name': 'Product A'},
        {'price': 300, 'bill_no': 101112, 'quantity': 10, 'date': datetime(2024, 3, 2), 'buyer_id': 2,
         'name': 'Product B'}
        # Add more bills as needed
    ]
    for data in bill_data:
        bill = Bill(**data)
        db.session.add(bill)

    # Seed Returned Goods
    returned_good_data = [
        {'date': datetime(2024, 3, 1), 'quantity': 3, 'buyer_id': 1, 'name': 'Product A'},
        {'date': datetime(2024, 3, 2), 'quantity': 6, 'buyer_id': 2, 'name': 'Product B'}
        # Add more returned goods as needed
    ]
    for data in returned_good_data:
        returned_good = Returned_Good(**data)
        db.session.add(returned_good)

    db.session.commit()


if __name__ == '__main__':
    seed()
