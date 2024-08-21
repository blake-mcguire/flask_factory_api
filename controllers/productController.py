from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productsServices
from marshmallow import ValidationError
from utils.util import token_required
from limiter import limiter
from caching import cache

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    product_created = productsServices.create_product(product_data)
    return jsonify(product_created), 201

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_all_products():
    all_products = productsServices.get_all_products()
    return products_schema.jsonify(all_products), 200

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_product_by_id(product_id):
    product = productsServices.get_product_by_id(product_id)
    return jsonify(product), 200

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def update_product(product_id):
    try:
        data = request.json
        result = productsServices.update_product(product_id, data)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def delete_product(product_id):
    result = productsServices.delete_product(product_id)
    return jsonify(result), 200