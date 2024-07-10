from flask import Blueprint, request, flash, render_template, redirect, url_for

from app.extensions import db
from app.forms.product_form import ProductForm
from app.logger import logger
from app.models import Product

product_routes = Blueprint('product', __name__)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@product_routes.route('/api/product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit() and request.method == 'POST':
        product = Product(
            name=form.name.data,
            part_no=form.part_no.data,
            unit_type=form.unit_type.data,
            quantity=form.quantity.data
        )
        db.session.add(product)
        db.session.commit()
        logger.info(f'Product {product.name} added to database')
        flash(f'Product {product.name} added to database', 'success')
        return redirect(url_for('product.add_product'))
    return render_template('product.html', form=form)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@product_routes.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    logger.info(f'Fetched all Products')
    return render_template("show_products.html", products=products)
    # return jsonify(products)
