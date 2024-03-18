from flask import render_template, redirect, Blueprint

from app.models import Goods, Raw_Material, Raw_Material_Records

inventory_bp = Blueprint('inventory_bp', __name__)


@inventory_bp.route('/')
def show_inventory():
    raw_material_data = Raw_Material.query.all()
    produced_good_data = Goods.query.all()
    table1 = [record.to_dict() for record in raw_material_data]
    table2 = [record.to_dict() for record in produced_good_data]
    return render_template('inventory.html', table1=table1, table2=table2)
