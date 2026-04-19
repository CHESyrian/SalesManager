from infrastructure.database.session import SessionLocal
from core.services.order_service import OrderService
from core.services.product_service import ProductService


class DashboardController:

    def __init__(self):
        # 🔥 Single session for dashboard lifetime
        self.db = SessionLocal()

        self.orders = OrderService()
        self.products = ProductService()

    # -------------------------------------------------
    # KPI: TODAY SALES
    # -------------------------------------------------

    def get_today_sales(self):

        orders = self.orders.get_all_orders(self.db)

        return sum(
            float(o.total_amount or 0)
            for o in orders
            if o.status == "completed"
        )

    # -------------------------------------------------
    # KPI: TOTAL ORDERS
    # -------------------------------------------------

    def get_orders_count(self):
        return len(self.orders.get_all_orders(self.db))

    # -------------------------------------------------
    # KPI: PRODUCTS
    # -------------------------------------------------

    def get_products_count(self):
        return len(self.products.get_all_products(self.db))

    # -------------------------------------------------
    # LOW STOCK
    # -------------------------------------------------

    def get_low_stock(self, threshold=5):

        products = self.products.get_all_products(self.db)

        return [
            p for p in products
            if p.stock_qty <= threshold
        ]

    # -------------------------------------------------
    # RECENT ORDERS
    # -------------------------------------------------

    def get_recent_orders(self, limit=5):

        orders = self.orders.get_all_orders(self.db)

        return sorted(
            orders,
            key=lambda x: x.id,
            reverse=True
        )[:limit]

    # -------------------------------------------------
    # WEEKLY SALES CHART DATA
    # -------------------------------------------------

    def get_weekly_sales(self):

        orders = self.orders.get_all_orders(self.db)

        data = {}

        for o in orders:
            if o.status != "completed":
                continue

            day = o.created_at.date()
            data[day] = data.get(day, 0) + float(o.total_amount or 0)

        return sorted(data.items())

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------

    def close(self):
        if self.db:
            self.db.close()
            self.db = None