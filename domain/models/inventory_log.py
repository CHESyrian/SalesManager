from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from infrastructure.database.base import Base


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id         = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change_qty = Column(Integer)  # +stock / -sale
    reason     = Column(String(50))  # sale / restock / adjustment
    created_at = Column(DateTime, default=datetime.utcnow)