from flask import Blueprint, render_template, request, jsonify
from app.models.raw_material import Raw_Material
from app import db
from app.models import Goods

form_bp = Blueprint('form_bp', __name__)

# Sample data for autocomplete
ITEMS = ["Item1", "Item2", "Item3", "Item4"]


@form_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Here you can handle the form data
        print(request.form)
    return render_template('form.html', items=ITEMS)


@form_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    results = Goods.query.filter(Goods.good_name.like(f'%{search}%')).limit(10).all()
    # Return good_name for both "id" and "name" in the JSON response
    return jsonify(matching_results=[{"id": item.good_name, "name": item.good_name} for item in results])

