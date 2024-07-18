from datetime import datetime
from json import load

from dotenv import load_dotenv

from app.logger import logger as log
from app.models import BillItem, ChallanItem, ProductMaterial
from app.models import Buyer, Supplier, Material, Product, Bill, Challan, ProductScrap, MaterialScrap, Unit
from app.models import IndianState
from app.models import Question, Role, User, RolesUsers
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

    # Load and add Unit records
    for item in read_json('units.json'):
        record = Unit(**item)
        db.session.add(record)

    # Load and add Supplier records
    for item in read_json('suppliers.json'):
        record = Supplier(**item)
        db.session.add(record)

    log.info(f'Added Supplier records')

    # Load and add Buyer records
    for item in read_json('buyers.json'):
        record = Buyer(**item)
        db.session.add(record)

    log.info(f'Added Buyer records')

    # Load and add Material records
    for item in read_json('materials.json'):
        record = Material(**item)
        db.session.add(record)

    log.info(f'Added Material records')

    # Load and add Product records
    for item in read_json('products.json'):
        record = Product(**item)
        db.session.add(record)

    log.info(f'Added Product records')

    # Load and add Bill records
    for item in read_json('bills.json'):
        item['date'] = convert_date(item['date'])
        record = Bill(**item)
        db.session.add(record)

    log.info(f'Added Bill records')

    # Load and add BillItem records
    for item in read_json('bill_items.json'):
        record = BillItem(**item)
        db.session.add(record)

    log.info(f'Added BillItem records')

    # Load and add Challan records
    for item in read_json('challans.json'):
        item['date'] = convert_date(item['date'])
        record = Challan(**item)
        db.session.add(record)

    log.info(f'Added Challan records')

    # Load and add ChallanItem records
    for item in read_json('challan_items.json'):
        record = ChallanItem(**item)
        db.session.add(record)

    log.info(f'Added ChallanItem records')

    # Load and add ProductScrap records
    for item in read_json('product_scraps.json'):
        item['date'] = convert_date(item['date'])
        record = ProductScrap(**item)
        db.session.add(record)

    log.info(f'Added ProductScrap records')

    # Load and add MaterialScrap records
    for item in read_json('material_scraps.json'):
        item['date'] = convert_date(item['date'])
        record = MaterialScrap(**item)
        db.session.add(record)

    log.info(f'Added MaterialScrap records')

    # Load and add ProductMaterial records
    for item in read_json('product_materials.json'):
        record = ProductMaterial(**item)
        db.session.add(record)

    # Load and add data for Question, Role, User, and RolesUsers models
    user_data = read_json('user.json')

    for item in user_data['questions']:
        record = Question(**item)
        db.session.add(record)

    log.info(f'Added Question records')

    for item in user_data['roles']:
        record = Role(**item)
        db.session.add(record)

    log.info(f'Added Role records')

    for item in user_data['users']:
        record = User(**item)
        db.session.add(record)

    log.info(f'Added User records')

    for item in user_data['roles_users']:
        record = RolesUsers(**item)
        db.session.add(record)

    log.info(f'Added RolesUsers records')

    db.session.commit()

    IndianState.load_state()
    log.info('State Data loaded')

    Question.load_static_data()
    log.info('Questions saved')


if __name__ == '__main__':
    with create_app().app_context():
        seed()
