from json import load

from app import db, create_app
from app.models import Buyer, Supplier, Raw_Material, Goods, Bill, Challan, Goods_Records, Raw_Material_Records, \
    Returned_Good, RawMaterialsPartNo, User, Write_off

app = create_app()
app.app_context().push()


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
        record = Raw_Material(**item)
        db.session.add(record)

    for item in read_json('data/goods.json'):
        record = Goods(**item)
        db.session.add(record)

    for item in read_json('data/bills.json'):
        record = Bill(**item)
        db.session.add(record)

    for item in read_json('data/returned_good.json'):
        record = Returned_Good(**item)
        db.session.add(record)

    for item in read_json('data/challans.json'):
        record = Challan(**item)
        db.session.add(record)

    for item in read_json('data/raw_material_part_no.json'):
        record = RawMaterialsPartNo(**item)
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

    record = Write_off(write_offs="A write off that has written off the inventory")
    db.session.add(record)

    db.session.commit()


# Function to seed the database
if __name__ == '__main__':
    seed()
