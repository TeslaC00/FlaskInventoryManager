from flask import Blueprint, request, flash, jsonify, render_template, redirect, url_for

from app.database import db
from app.forms.product_form import ProductForm
from app.logger import logger
from app.models import Product

product_routes = Blueprint('product', __name__)


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


@product_routes.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    logger.info(f'Fetched all Products')
    return render_template("show_products.html", products=products)
    # return jsonify(products)


@product_routes.route('/api/product/<string:name>', methods=['GET'])
def get_product(name):
    product = Product.query.get(name)
    if product:
        logger.info(f'Fetched product {product.to_dict()}')
        return jsonify(product)
    else:
        logger.error(f'Product {name} not found')
        flash(f'Product {name} not found', 'error')


@product_routes.route('/api/product/<string:name>', methods=['GET', 'POST'])
def update_product(name):
    product = Product.query.get(name)
    form = ProductForm(obj=product)
    form.name.render_kw = {'readonly': True}
    if form.validate_on_submit() and request.method == 'POST':
        logger.info(f'Updating product {product.to_dict()}')
        form.populate_obj(product)
        db.session.commit()
        logger.info(f'Product {product.to_dict()} updated')
        flash(f'Product {product.name} updated', 'success')


@product_routes.route('/api/product/<string:name>', methods=['POST'])
def delete_product(name):
    product = Product.query.get(name)
    if product:
        db.session.delete(product)
        db.session.commit()
        logger.info(f'Deleted Product {product.to_dict()}')
        flash(f'Product {product.name} deleted', 'success')
    else:
        logger.error(f'Product {name} not found')
        flash(f'Product {name} not found', 'error')
