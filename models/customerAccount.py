from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from models.roles import Role
from models.order import Order


class CustomerAccount(Base):
    __tablename__ = 'customer_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    role_id: Mapped[int] = mapped_column(db.ForeignKey('roles.role_id'))
    
    role: Mapped["Role"] = db.relationship("Role")
    
    orders: Mapped[list["Order"]] = db.relationship("Order", back_populates="customer_account")