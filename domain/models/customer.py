from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database.base import Base
from domain.models.mixins import TimestampMixin


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id      = Column(Integer, primary_key=True)
    name    = Column(String(100), nullable=False, index=True)
    phone   = Column(String(30))
    email   = Column(String(100))
    address = Column(String(255))
    orders  = relationship("Order", back_populates="customer", 
                           cascade="all, delete-orphan")