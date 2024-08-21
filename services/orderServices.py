from sqlalchemy import select
from models.product import Product
from models.order import Order
from models.orderProduct import order_products
from database import db
from datetime import datetime

def create_order(data):
    account_id = data['account_id']
    product_ids = data['products']  

    total_amount = 0
    for product_id in product_ids:
        product_query = select(Product).where(Product.product_id == product_id)
        product_obj = db.session.execute(product_query).scalar_one_or_none()
        
        if not product_obj:
            return {
                "status": "fail",
                "message": f"Product with ID {product_id} not found"
            }
        
        total_amount += product_obj.price

    new_order = Order(
        account_id=account_id,
        order_date=datetime.utcnow(),
        total_amount=total_amount,
        status='pending'
    )
    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)

    for product_id in product_ids:
        db.session.execute(order_products.insert().values(
            order_id=new_order.order_id,
            product_id=product_id,
            quantity=1  
        ))

    db.session.commit()

    return {
        "status": "success",
        "message": "Order placed successfully",
        "order_id": new_order.order_id
    }
    


def retrieve_order(order_id):
    order = db.session.query(Order).filter_by(order_id=order_id).first()
    
    if not order:
        return {
            "status": "fail",
            "message": f"Order with ID {order_id} not found"
        }
    
    order_products_list = db.session.query(order_products).filter_by(order_id=order_id).all()
    
    print(f"Order Products List: {order_products_list}")

    products = []
    for order_product in order_products_list:
        product_query = db.session.query(Product).filter_by(product_id=order_product.product_id).first()
        if product_query:
            products.append(product_query)

    print(f"Products: {products}")

    response = {
        "status": "success",
        "order_id": order.order_id,
        "account_id": order.account_id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status,
        "products": [
            {
                'product_id': product.product_id,
                'name': product.product_name,
                'price': product.price,
            } for product in products
        ]
    }
    
    return response