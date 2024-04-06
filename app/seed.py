from json import load

from app import create_app
from app.database import db
from app.models import Buyer, Supplier, Material, Product, Bill, Challan, Goods_Records, Raw_Material_Records, \
    ProductReturned, MaterialPartNo, User, WriteOff, ProductScrap, MaterialScrap

create_app().app_context().push()


def read_json(filename):
    with open(filename, 'r') as file:
        data = load(file)
    return data


def seed():
    for item in read_json('data/suppliers.json'):
        record = Supplier(**item)
        db.session.add(record)

    for item in read_json('data/buyers.json'):
        record = Buyer(**item)
        db.session.add(record)

    for item in read_json('data/raw_materials.json'):
        record = Material(**item)
        db.session.add(record)

    for item in read_json('data/goods.json'):
        record = Product(**item)
        db.session.add(record)

    for item in read_json('data/bills.json'):
        record = Bill(**item)
        db.session.add(record)

    for item in read_json('data/returned_good.json'):
        record = ProductReturned(**item)
        db.session.add(record)

    for item in read_json('data/challans.json'):
        record = Challan(**item)
        db.session.add(record)

    for item in read_json('data/raw_material_part_no.json'):
        record = MaterialPartNo(**item)
        db.session.add(record)

    for item in read_json('data/goods_records.json'):
        record = Goods_Records(**item)
        db.session.add(record)

    for item in read_json('data/raw_material_records.json'):
        record = Raw_Material_Records(**item)
        db.session.add(record)

    for item in read_json('data/users.json'):
        record = User(**item)
        db.session.add(record)

    for item in read_json('data/goods_scrap.json'):
        record = ProductScrap(**item)
        db.session.add(record)

    for item in read_json('data/raw_materials_scrap.json'):
        record = MaterialScrap(**item)
        db.session.add(record)

    record = WriteOff(write_offs="A write off that has written off the inventory")
    db.session.add(record)

    db.session.commit()


# Function to seed the database
if __name__ == '__main__':
    seed()
