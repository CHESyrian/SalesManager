from infrastructure.database.session import SessionLocal
from core.services.order_service import OrderService


class OrdersController:

    def __init__(self):
        # 🔥 Controller owns DB session (screen lifecycle)
        self.db = SessionLocal()
        self.service = OrderService()

    # -------------------------------------------------

    def get_all_orders(self):
        return self.service.get_all_orders(self.db)

    # -------------------------------------------------

    def get_order(self, order_id):
        return self.service.get_order(self.db, order_id)

    # alias (optional UI convenience)
    def search_order_by_id(self, order_id):
        return self.service.get_order(self.db, order_id)

    # -------------------------------------------------

    def cancel_order(self, order_id):
        return self.service.cancel_order(self.db, order_id)

    # -------------------------------------------------
    # Lifecycle (IMPORTANT)
    # -------------------------------------------------

    def close(self):
        if self.db:
            self.db.close()
            self.db = None