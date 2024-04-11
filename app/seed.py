from json import load

from app import create_app
from app.database import db
from app.logger import logger as log
from app.models import Buyer, Supplier, Material, Product, Bill, Challan, ProductionLog, \
    ProductReturned, MaterialPartNo, User, WriteOff, ProductScrap, MaterialScrap

create_app().app_context().push()


def read_json(filename):
    with open(filename, 'r') as file:
        data = load(file)
    return data


def seed():
    log.info('started seed')

    for item in read_json('data/suppliers.json'):
        record = Supplier(**item)
        db.session.add(record)

    log.info(f'Added Supplier records')

    for item in read_json('data/buyers.json'):
        record = Buyer(**item)
        db.session.add(record)

    log.info(f'Added Buyer records')

    for item in read_json('data/materials.json'):
        record = Material(**item)
        db.session.add(record)

    log.info(f'Added Material records')

    for item in read_json('data/products.json'):
        record = Product(**item)
        db.session.add(record)

    log.info(f'Added Product records')

    for item in read_json('data/bills.json'):
        record = Bill(**item)
        db.session.add(record)

    log.info(f'Added Bill records')

    for item in read_json('data/good_returned.json'):
        record = ProductReturned(**item)
        db.session.add(record)

    log.info(f'Added ProductReturned records')

    for item in read_json('data/challans.json'):
        record = Challan(**item)
        db.session.add(record)

    log.info(f'Added Challan records')

    for item in read_json('data/raw_material_part_no.json'):
        record = MaterialPartNo(**item)
        db.session.add(record)

    log.info(f'Added MaterialPartNo records')

    for item in read_json('data/users.json'):
        record = User(**item)
        db.session.add(record)

    log.info(f'Added User records')

    for item in read_json('data/product_scraps.json'):
        record = ProductScrap(**item)
        db.session.add(record)

    log.info(f'Added ProductScrap records')

    for item in read_json('data/materials_scraps.json'):
        record = MaterialScrap(**item)
        db.session.add(record)

    log.info(f'Added MaterialScrap records')

    for item in read_json('data/production_logs.json'):
        record = ProductionLog(**item)
        db.session.add(record)

    log.info(f'Added ProductionLog records')

    record = WriteOff(write_offs="A write off that has written off the inventory")
    db.session.add(record)

    db.session.commit()


# Function to seed the database
if __name__ == '__main__':
    seed()
