from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from infrastructure.database.base import Base
from domain.models.mixins import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    price = Column(Numeric, nullable=False)
    stock_qty = Column(Integer, default=0)
    order_items = relationship("OrderItem", back_populates="product")