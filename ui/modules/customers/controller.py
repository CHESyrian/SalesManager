from infrastructure.database.session import SessionLocal
from core.services.customer_service import CustomerService


class CustomersController:

    def __init__(self):
        # 🔥 Controller owns DB session (screen lifecycle)
        self.db = SessionLocal()
        self.service = CustomerService()

    # -------------------------------------------------

    def get_all(self):
        return self.service.get_all_customers(self.db)

    # -------------------------------------------------

    def search(self, keyword):
        return self.service.search_customers(self.db, keyword)

    # -------------------------------------------------

    def create(self, name, email, phone=None, address=None):
        return self.service.create_customer(
            self.db,
            name=name,
            email=email,
            phone=phone
        )

    # -------------------------------------------------

    def update(self, customer_id, name, email, phone=None, address=None):
        return self.service.update_customer(
            self.db,
            customer_id,
            name=name,
            email=email,
            phone=phone
        )

    # -------------------------------------------------

    def delete(self, customer_id):
        return self.service.delete_customer(self.db, customer_id)

    # -------------------------------------------------
    # Lifecycle (IMPORTANT)
    # -------------------------------------------------

    def close(self):
        if self.db:
            self.db.close()
            self.db = None