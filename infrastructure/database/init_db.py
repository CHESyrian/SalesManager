from infrastructure.database.base import Base
from infrastructure.database.connection import engine

from domain.models.user import User
from domain.models.customer import Customer
from domain.models.product import Product
from domain.models.order import Order
from domain.models.order_item import OrderItem
from domain.models.inventory_log import InventoryLog


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()