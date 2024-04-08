from flask import Blueprint, jsonify, request, flash

from app.database import db
from app.forms.buyer_form import BuyerForm
from app.logger import logger
from app.models import Buyer

buyer_routes = Blueprint('buyer', __name__)


@buyer_routes.route('/api/buyer', methods=['GET', 'POST'])
def add_buyer():
    form = BuyerForm()
    if form.validate_on_submit() and request.method == 'POST':
        buyer = Buyer(
            name=form.name.data,
            GST_No=form.GST_No.data,
            state_code=form.state_code.data,
            state_name=form.state_name.data,
        )
        db.session.add(buyer)
        db.session.commit()
        logger.info(f'Added Buyer {buyer.to_dict()} to buyer table')
        flash(f'New Buyer {buyer.name} Added', 'success')


@buyer_routes.route('/api/buyers', methods=['GET'])
def get_buyers():
    buyers = Buyer.query.all()
    logger.info('Fetched all buyers')
    return jsonify(buyers)


@buyer_routes.route('/api/buyer/<int:buyer_id>', methods=['GET'])
def get_buyer(buyer_id):
    buyer = Buyer.query.get(buyer_id)
    if buyer:
        logger.info(f'Fetched Buyer {buyer.to_dict()}')
        return jsonify(buyer)
    else:
        logger.error(f'Buyer {buyer_id} not found')
        flash(f'Buyer {buyer_id} not found', 'error')


@buyer_routes.route('/api/buyer/<int:buyer_id>', methods=['GET', 'POST'])
def update_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    form = BuyerForm(obj=buyer)
    if form.validate_on_submit() and request.method == 'POST':
        logger.info(f'Updating Buyer {buyer.to_dict()}')
        form.populate_obj(buyer)
        db.session.commit()
        logger.info(f'Updated Buyer {buyer.to_dict()}')
        flash(f'Updated Buyer {buyer.name}', 'success')


@buyer_routes.route('/api/buyer/<int:buyer_id>', methods=['POST'])
def delete_buyer(buyer_id):
    buyer = Buyer.query.get(buyer_id)
    if buyer:
        db.session.delete(buyer)
        db.session.commit()
        logger.info(f'Deleted Buyer {buyer.to_dict()}')
        flash(f'Buyer {buyer.name} deleted', 'success')
    else:
        logger.error(f'Buyer {buyer_id} not found')
        flash(f'Buyer {buyer_id} not found', 'error')
