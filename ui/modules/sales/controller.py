from infrastructure.database.session import SessionLocal
from core.services.sales_facade_service import SalesFacadeService


class SalesController:

    def __init__(self):
        # 🔥 session belongs ONLY here (screen lifecycle)
        self.db = SessionLocal()

        self.facade = SalesFacadeService()

    # -------------------------------------------------
    # Products
    # -------------------------------------------------

    def load_products(self):
        return self.facade.get_available_products(self.db)

    def get_all_products(self):
        return self.facade.get_all_products(self.db)

    def search_products(self, keyword):
        return self.facade.search_products(self.db, keyword)

    # -------------------------------------------------
    # Customers
    # -------------------------------------------------

    def get_customers(self):
        return self.facade.get_customers(self.db)

    def search_customers(self, keyword):
        return self.facade.search_customers(self.db, keyword)

    def get_customer(self, customer_id):
        return self.facade.get_customer(self.db, customer_id)

    # -------------------------------------------------
    # Orders / Sales
    # -------------------------------------------------

    def checkout(self, customer_id, items):
        return self.facade.checkout(self.db, customer_id, items)

        

    def get_orders(self):
        return self.facade.get_orders(self.db)

    def get_order(self, order_id):
        return self.facade.get_order(self.db, order_id)

    def cancel_order(self, order_id):
        return self.facade.cancel_order(self.db, order_id)

    def get_customer_orders(self, customer_id):
        return self.facade.get_customer_orders(self.db, customer_id)

    # -------------------------------------------------
    # Lifecycle (IMPORTANT)
    # -------------------------------------------------

    def close(self):
        """
        Must be called when the Sales screen is closed.
        Prevents connection leaks.
        """
        if self.db:
            self.db.close()
            self.db = None