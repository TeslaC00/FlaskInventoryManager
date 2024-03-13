# seed.py

import random
import string
from datetime import datetime, timedelta

from app import db
from .models import *


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def seed():
    # Seed Suppliers
    supplier_data = []
    for i in range(100):
        supplier = {
            'name': f'Supplier {i}',
            'GST_No': generate_random_string(15),
            'state_code': random.randint(1, 50),
            'state_name': f'State {random.randint(1, 50)}',
            'supplier_id': i + 1
        }
        supplier_data.append(supplier)
    for data in supplier_data:
        supplier = Supplier(**data)
        db.session.add(supplier)

    # Seed Buyers
    buyer_data = []
    for i in range(100):
        buyer = {
            'name': f'Buyer {i}',
            'GST_No': generate_random_string(15),
            'state_code': random.randint(1, 50),
            'state_name': f'State {random.randint(1, 50)}',
            'buyer_id': i + 1
        }
        buyer_data.append(buyer)
    for data in buyer_data:
        buyer = Buyer(**data)
        db.session.add(buyer)

    # Seed Raw Materials
    raw_material_data = []
    for i in range(100):
        raw_material = {
            'name': f'Raw Material {i}',
            'unit_type': random.choice(['kg', 'litre', 'piece', 'pound', 'meter']),
            'quantity': random.randint(100, 1000)
        }
        raw_material_data.append(raw_material)
    for data in raw_material_data:
        raw_material = Raw_Material(**data)
        db.session.add(raw_material)

    # Seed Goods
    goods_data = []
    for i in range(100):
        goods = {
            'name': f'Product {i}',
            'unit_type': random.choice(['piece', 'kg', 'meter']),
            'quantity': random.randint(50, 500)
        }
        goods_data.append(goods)
    for data in goods_data:
        goods = Goods(**data)
        db.session.add(goods)

    # Seed Users
    user_data = []
    for i in range(100):
        user = {
            'Username': f'user{i}',
            'password': generate_random_string(10),
            'user_type': random.choice(['admin', 'regular'])
        }
        user_data.append(user)
    for data in user_data:
        user = User(**data)
        db.session.add(user)

    # Seed Write Offs
    write_off_data = []
    for i in range(100):
        write_off = {
            'write_offs': f'Write Off {i}'
        }
        write_off_data.append(write_off)
    for data in write_off_data:
        write_off = Write_off(**data)
        db.session.add(write_off)

    # Seed Raw Material Records
    raw_material_records_data = []
    for i in range(100):
        record_date = datetime.now() - timedelta(days=i)
        raw_material_record = {
            'date': record_date,
            'quantity_used': random.randint(10, 100),
            'name': f'Raw Material {random.randint(1, 100)}'
        }
        raw_material_records_data.append(raw_material_record)
    for data in raw_material_records_data:
        raw_material_record = Raw_Material_Records(**data)
        db.session.add(raw_material_record)

    # Seed Goods Records
    goods_records_data = []
    for i in range(100):
        record_date = datetime.now() - timedelta(days=i)
        goods_record = {
            'date': record_date,
            'quantity_produced': random.randint(10, 100),
            'name': f'Product {random.randint(1, 100)}'
        }
        goods_records_data.append(goods_record)
    for data in goods_records_data:
        goods_record = Goods_Records(**data)
        db.session.add(goods_record)

    # Seed Challans
    challan_data = []
    for i in range(100):
        challan_date = datetime.now() - timedelta(days=i)
        challan = {
            'price': random.randint(100, 1000),
            'challan_no': random.randint(1000, 9999),
            'date': challan_date,
            'quantity': random.randint(10, 100),
            'supplier_id': random.randint(1, 100),
            'name': f'Raw Material {random.randint(1, 100)}'
        }
        challan_data.append(challan)
    for data in challan_data:
        challan = Challan(**data)
        db.session.add(challan)

    # Seed Bills
    bill_data = []
    for i in range(100):
        bill_date = datetime.now() - timedelta(days=i)
        bill = {
            'price': random.randint(500, 5000),
            'bill_no': random.randint(10000, 99999),
            'quantity': random.randint(5, 50),
            'date': bill_date,
            'buyer_id': random.randint(1, 100),
            'name': f'Product {random.randint(1, 100)}'
        }
        bill_data.append(bill)
    for data in bill_data:
        bill = Bill(**data)
        db.session.add(bill)

    # Seed Returned Goods
    returned_good_data = []
    for i in range(100):
        returned_good_date = datetime.now() - timedelta(days=i)
        returned_good = {
            'date': returned_good_date,
            'quantity': random.randint(1, 10),
            'buyer_id': random.randint(1, 100),
            'name': f'Product {random.randint(1, 100)}'
        }
        returned_good_data.append(returned_good)
    for data in returned_good_data:
        returned_good = Returned_Good(**data)
        db.session.add(returned_good)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
