from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerServices
from marshmallow import ValidationError
from utils.util import admin_required, token_required
from limiter import limiter
from caching import cache

@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    customer_created = customerServices.create_customer(customer_data)
    return jsonify(customer_created), 201

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_all_customers():
    all_customers=customerServices.get_all_customers()
    return customers_schema.jsonify(all_customers), 200

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_customer_by_id(id):
    customer = customerServices.get_customer_by_id(id)
    return jsonify(customer), 200

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def update_customer(id):
    try:
        data = request.json
        result = customerServices.update_customer(id, data)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def delete_customer(id):
    result = customerServices.delete_customer(id)
    return jsonify(result), 200


