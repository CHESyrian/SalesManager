from core.services.product_service import ProductService
from core.services.customer_service import CustomerService
from core.services.order_service import OrderService


class SalesFacadeService:

    def __init__(self):
        self.product_service = ProductService()
        self.customer_service = CustomerService()
        self.order_service = OrderService()

    # -------------------------------------------------
    # Products
    # -------------------------------------------------

    def get_available_products(self, db):
        return self.product_service.get_available_products(db)

    def get_all_products(self, db):
        return self.product_service.get_all_products(db)

    def search_products(self, db, keyword):
        return self.product_service.search_products(db, keyword)

    # -------------------------------------------------
    # Customers
    # -------------------------------------------------

    def get_customers(self, db):
        return self.customer_service.get_all_customers(db)

    def search_customers(self, db, keyword):
        return self.customer_service.search_customers(db, keyword)

    def get_customer(self, db, customer_id):
        return self.customer_service.get_customer(db, customer_id)

    # -------------------------------------------------
    # Orders / Sales
    # -------------------------------------------------

    def checkout(self, db, customer_id, items):
        return self.order_service.create_order(db, customer_id, items)

    def get_orders(self, db):
        return self.order_service.get_all_orders(db)

    def get_order(self, db, order_id):
        return self.order_service.get_order(db, order_id)

    def cancel_order(self, db, order_id):
        return self.order_service.cancel_order(db, order_id)

    def get_customer_orders(self, db, customer_id):
        return self.order_service.get_customer_orders(db, customer_id)