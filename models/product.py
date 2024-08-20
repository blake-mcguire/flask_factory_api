from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, Integer, String, Text

class Product(Base):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False) 