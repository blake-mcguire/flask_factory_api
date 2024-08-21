from flask import request, jsonify
from models.schemas.customerAccountsSchema import account_schema, accounts_schema
from services import customerAccountServices  # Import the service module as a whole
from marshmallow import ValidationError
from utils.util import admin_required, token_required
from limiter import limiter
from caching import cache


@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def login():
    try:
        credentials = request.json
        token = customerAccountServices.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'message': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def create_account():
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    account_created = customerAccountServices.create_account(account_data)
    return jsonify(account_created), 201

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_all_customer_accounts():
    all_accounts = customerAccountServices.get_all_customer_accounts()
    return accounts_schema.jsonify(all_accounts), 200

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def get_account_by_id(account_id):
    account = customerAccountServices.get_account_by_id(account_id)
    return jsonify(account), 200

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def update_customer_account(account_id):
    try:
        update_data = request.json
        result = customerAccountServices.update_customer_account(account_id, update_data)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

@admin_required
@cache.cached(timeout=60) 
@limiter.limit("5 per minute")
def delete_account(account_id):
    result = customerAccountServices.delete_account(account_id)
    return jsonify(result), 200
