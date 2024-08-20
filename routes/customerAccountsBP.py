from flask import Blueprint
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
account_blueprint.route('/<int:account_id>', methods=['DELETE'])(delete_account)
account_blueprint.route('/search/<int:account_id>', methods=['GET'])(get_account_by_id)
account_blueprint.get('/')(get_all_customer_accounts)
account_blueprint.put('/<int:account_id>')(update_customer_account)
account_blueprint.post('/login')(login) 
account_blueprint.post('/')(create_account) 
