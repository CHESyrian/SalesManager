from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.database.base import Base
from domain.models.mixins import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True)
    customer_id  = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Numeric, default=0.0)
    status       = Column(String(20), default="pending")
    created_at   = Column(DateTime, default=datetime.utcnow)
    customer     = relationship("Customer", back_populates="orders")
    items        = relationship("OrderItem", back_populates="order", 
                                cascade="all, delete-orphan")