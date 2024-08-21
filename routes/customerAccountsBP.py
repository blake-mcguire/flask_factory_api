from flask import Blueprint
from limiter import limiter 
from controllers.customerAccountController import (
    delete_account,
    get_account_by_id,
    get_all_customer_accounts,
    update_customer_account,
    login,
    create_account  #
)

account_blueprint = Blueprint('customer_bp', __name__)

# Define the routes
account_blueprint.route('/<int:account_id>', methods=['DELETE'])(limiter.limit("5 per minute")(delete_account))
account_blueprint.route('/search/<int:account_id>', methods=['GET'])(limiter.limit("5 per minute")(get_account_by_id))
account_blueprint.get('/')(limiter.limit("5 per minute")(get_all_customer_accounts))
account_blueprint.put('/<int:account_id>')(limiter.limit("5 per minute")(update_customer_account))
account_blueprint.post('/login')(limiter.limit("5 per minute")(login)) 
account_blueprint.post('/')(limiter.limit("5 per minute")(create_account))
