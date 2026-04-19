from domain.models.customer import Customer


class CustomerService:

    def create_customer(self, db, name, email, phone=None):
        customer = Customer(
            name=name,
            email=email,
            phone=phone
        )
        
        db.add(customer)
        db.commit()
        
        return customer

    def get_all_customers(self, db):
        return db.query(Customer).order_by(Customer.name).all()

    def get_customer(self, db, customer_id):
        return db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

    def search_customers(self, db, keyword):
        return db.query(Customer).filter(
            Customer.name.ilike(f"%{keyword}%")
        ).all()

    def update_customer(self, db, customer_id, **kwargs):
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            return None

        for k, v in kwargs.items():
            setattr(customer, k, v)

        db.commit()
        
        return customer

    def delete_customer(self, db, customer_id):
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            return False

        db.delete(customer)
        db.commit()
        
        return True