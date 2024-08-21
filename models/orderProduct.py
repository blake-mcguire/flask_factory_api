from sqlalchemy import Table, Column, Integer, ForeignKey
from database import db

order_products = Table(
    'order_products', db.metadata,
    Column('order_id', Integer, ForeignKey('orders.order_id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.product_id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1)
)