from flask import Blueprint, render_template,request
from app.models.raw_material import Raw_Material

form_bp = Blueprint('form_bp', __name__)

# Sample data for autocomplete
ITEMS = ["Item1", "Item2", "Item3", "Item4"]


@form_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Here you can handle the form data
        print(request.form)
    return render_template('form.html', items=ITEMS)
