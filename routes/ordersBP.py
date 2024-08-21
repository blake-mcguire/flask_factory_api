from flask import Blueprint
from controllers.orderController import (
    retrieve_order,
    create_order
)

order_blueprint = Blueprint('order_bp', __name__)

order_blueprint.post('/')(create_order)
order_blueprint.get('/<int:order_id>')(retrieve_order)