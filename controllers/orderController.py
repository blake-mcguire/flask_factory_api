from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderServices
from marshmallow import ValidationError
from utils.util import token_required
from limiter import limiter
from caching import cache

@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def create_order():
    try:
        order_data = order_schema.load(request.json)
        response = orderServices.create_order(order_data)
        return jsonify(response), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@token_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def retrieve_order(order_id):
    try:
        response = orderServices.retrieve_order(order_id)
        return jsonify(response), 200 
    except ValidationError as e:
        return jsonify(e.messages), 400