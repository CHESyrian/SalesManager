from infrastructure.database.session import SessionLocal
from core.services.product_service import ProductService


class ProductsController:

    def __init__(self):
        # 🔥 Controller owns session (screen lifecycle)
        self.db = SessionLocal()
        self.service = ProductService()

    # -------------------------------------------------
    # Products
    # -------------------------------------------------

    def get_all_products(self):
        return self.service.get_all_products(self.db)

    def get_available_products(self):
        return self.service.get_available_products(self.db)

    def search_products(self, keyword):
        return self.service.search_products(self.db, keyword)

    def add_product(self, name, sku, price, stock_qty):
        return self.service.create_product(
            self.db, name, sku, price, stock_qty
        )

    def update_product(self, product_id, name, sku, price, stock_qty):
        return self.service.update_product(
            self.db,
            product_id,
            name=name,
            sku=sku,
            price=price,
            stock_qty=stock_qty
        )

    def delete_product(self, product_id):
        return self.service.delete_product(self.db, product_id)

    # -------------------------------------------------
    # Lifecycle (IMPORTANT)
    # -------------------------------------------------

    def close(self):
        if self.db:
            self.db.close()
            self.db = None