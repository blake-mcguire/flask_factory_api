from typing import List
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, TIMESTAMP, ForeignKey
from models.orderProduct import order_products
from models.product import Product




class Order(Base):
    __tablename__ = 'orders'
    
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('customer_accounts.id', ondelete='CASCADE'), nullable=False)
    order_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=db.func.current_timestamp())
    total_amount: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), server_default='pending')

    # Many-To-One: Order and CustomerAccount
    customer_account: Mapped["CustomerAccount"] = relationship("CustomerAccount", back_populates="orders")

    # Many-To-Many: Products
    products: Mapped[List["Product"]] = relationship("Product", secondary="order_products", lazy='noload')