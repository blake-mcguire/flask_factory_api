from flask import Blueprint
from controllers.customerController import (
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer
)

customer_blueprint = Blueprint('customerbp', __name__)

customer_blueprint.post('/')(create_customer)
customer_blueprint.get('/search/<int:id>')(get_customer_by_id)
customer_blueprint.get('/')(get_all_customers)
customer_blueprint.delete('/<int:id>')(delete_customer)
customer_blueprint.put('/<int:id>')(update_customer)