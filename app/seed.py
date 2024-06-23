# seed.py
from datetime import datetime
from json import load

from dotenv import load_dotenv

from app.logger import logger as log
from app.models import BillItem, ChallanItem, ProductMaterial
from app.models import Buyer, Supplier, Material, Product, Bill, Challan, ProductScrap, MaterialScrap
from app import create_app
from app.extensions import db

load_dotenv()


def read_json(filename):
    with open('data/' + filename, 'r') as file:
        data = load(file)
    return data


def convert_date(date_string):
    date_format = '%y/%m/%d'  # Adjust format as needed
    return datetime.strptime(date_string, date_format).date()


def seed():
    log.info('started seed')

    for item in read_json('suppliers.json'):
        record = Supplier(**item)
        db.session.add(record)

    log.info(f'Added Supplier records')

    for item in read_json('buyers.json'):
        record = Buyer(**item)
        db.session.add(record)

    log.info(f'Added Buyer records')

    for item in read_json('materials.json'):
        record = Material(**item)
        db.session.add(record)

    log.info(f'Added Material records')

    for item in read_json('products.json'):
        record = Product(**item)
        db.session.add(record)

    log.info(f'Added Product records')

    for item in read_json('bills.json'):
        # to remove in production
        item['date'] = convert_date(item['date'])
        record = Bill(**item)
        db.session.add(record)

    log.info(f'Added Bill records')

    for item in read_json('bill_items.json'):
        record = BillItem(**item)
        db.session.add(record)

    log.info(f'Added BillItem records')

    for item in read_json('challans.json'):
        # to remove in production
        item['date'] = convert_date(item['date'])
        record = Challan(**item)
        db.session.add(record)

    log.info(f'Added Challan records')

    for item in read_json('challan_items.json'):
        record = ChallanItem(**item)
        db.session.add(record)

    log.info(f'Added ChallanItem records')

    for item in read_json('product_scraps.json'):
        # to remove in production
        item['date'] = convert_date(item['date'])
        record = ProductScrap(**item)
        db.session.add(record)

    log.info(f'Added ProductScrap records')

    for item in read_json('material_scraps.json'):
        # to remove in production
        item['date'] = convert_date(item['date'])
        record = MaterialScrap(**item)
        db.session.add(record)

    log.info(f'Added MaterialScrap records')

    for item in read_json('product_materials.json'):
        record = ProductMaterial(**item)
        db.session.add(record)

    db.session.commit()


if __name__ == '__main__':
    with create_app().app_context():
        seed()
