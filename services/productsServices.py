from flask import request, jsonify
from models.product import Product
from database import db
from marshmallow import ValidationError
from sqlalchemy import select, delete
from models.orderProduct import order_products


def create_product(data):
    product_name = data['product_name']
    description = data['description']
    price = data['price']
    stock_quantity = data['stock_quantity']
    
    product_name_query = select(Product).where(Product.product_name == product_name)
    product = db.session.execute(product_name_query).scalar_one_or_none()
    
    if product:
        
        product.stock_quantity += stock_quantity
        
        return {
            "status": "new shipment recieved",
            "message": "New shipment has been added to the inventory of the existing product"
        }
    else:
    # Create a new product
        new_product = Product(
            product_name=product_name,
            description=description,
            price=price,
            stock_quantity=stock_quantity
        )
        db.session.add(new_product)

    db.session.commit()
    db.session.refresh(new_product)
    return new_product

def get_product_by_id(product_id):
    product = db.session.query(Product).get(product_id)
    if product:
        return {
            "status": "success",
            "data": {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity
            }
        }
    
    return {
        "status": "fail",
        "message": "product not found"
    }

def update_product(product_id, data):
    product_query = select(Product).where(Product.product_id == product_id)
    product = db.session.execute(product_query).scalar_one_or_none()
    
    if not product:
        return {
            "status": "fail",
            "message": "Product Not Found"
        }
        
    if 'product_id' in data:
        product.product_id = data['product_id']
    
    if 'product_name' in data:
        product.product_name = data['product_name']
    
    if 'description' in data:
        product.description = data['description']
    
    if 'stock_quantity' in data: 
        product.stock_quantity = data['stock_quantity']
        
    if 'price' in data:
        product.price = data['price']
    
    try:
        db.session.commit()
        return {
            "status": "success",
            "message": "product updated succesfully"
        }
    
    except Exception as e:
        return {
            "status": "fail",
            "message": f"Failed To update Product: {str(e)}"
        }

def get_all_products():
    products = db.session.query(Product).all()
    return products

def delete_product(product_id):
    product_query = select(Product).where(Product.product_id == product_id)
    product = db.session.execute(product_query).scalar_one_or_none()
    
    if not product:
        return {
            "status": "fail",
            "message": "Product Not found"
        }
    try:
        order_products_query = select(order_products).where(order_products.c.product_id == product_id)
        order_products_entries = db.session.execute(order_products_query).fetchall()
        
        for entry in order_products_entries:
            delete_order_product = delete(order_products).where(
                order_products.c.order_id == entry.order_id,
                order_products.c.product_id == entry.product_id
            )
            db.session.execute(delete_order_product)
        
        # Delete the product
        db.session.delete(product)
        db.session.commit()
        
        return {
            "status": "success",
            "message": "Product deleted successfully"
        }
    
    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to delete Product: {str(e)}"
        }