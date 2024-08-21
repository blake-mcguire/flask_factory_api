from flask import Blueprint
from controllers.productController import (
    delete_product,
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    
)

product_blueprint = Blueprint('product_bp', __name__)

product_blueprint.post('/')(create_product)
product_blueprint.get('/')(get_all_products)
product_blueprint.get('/<int:product_id>')(get_product_by_id)
product_blueprint.delete('/<int:product_id>')(delete_product)
product_blueprint.put('/<int:product_id>')(update_product)