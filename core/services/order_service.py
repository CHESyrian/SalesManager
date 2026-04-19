from decimal import Decimal

from domain.models.order import Order
from domain.models.order_item import OrderItem
from domain.models.product import Product
from domain.models.customer import Customer
from domain.models.inventory_log import InventoryLog


class OrderService:

    def create_order(self, db, customer_id, cart_items):

        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise Exception("Customer not found.")

        if not cart_items:
            raise Exception("Cart is empty.")

        product_ids = [i["product_id"] for i in cart_items]

        products = db.query(Product).filter(
            Product.id.in_(product_ids)
        ).all()

        product_map = {p.id: p for p in products}

        # ---------------------------
        # validate stock
        # ---------------------------
        for item in cart_items:
            product = product_map.get(item["product_id"])

            if not product:
                raise Exception("Product not found.")

            if product.stock_qty < item["qty"]:
                raise Exception(f"Insufficient stock for {product.name}")

        # ---------------------------
        # create order
        # ---------------------------
        order = Order(
            customer_id=customer_id,
            status="completed",
            total_amount=Decimal("0.00")
        )
        
        db.add(order)
        db.flush()

        total = Decimal("0.00")
        
        # ---------------------------
        # order items + stock update
        # ---------------------------
        for item in cart_items:
            product = product_map[item["product_id"]]
            qty = item["qty"]

            price = Decimal(str(product.price))
            total += price * qty

            db.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=price
            ))

            product.stock_qty -= qty

            db.add(InventoryLog(
                product_id=product.id,
                change_qty=-qty,
                reason="sale"
            ))
        order.total_amount = total
        
        db.commit()
        
        return order

    # -------------------------------------------------

    def get_all_orders(self, db):
        return db.query(Order).order_by(Order.id.desc()).all()

    # -------------------------------------------------

    def get_order(self, db, order_id):
        return db.query(Order).filter(
            Order.id == order_id
        ).first()

    # -------------------------------------------------

    def cancel_order(self, db, order_id):

        order = db.query(Order).filter(
            Order.id == order_id
        ).first()

        if not order:
            raise Exception("Order not found.")

        if order.status == "cancelled":
            raise Exception("Order already cancelled.")

        for item in order.items:
            product = item.product
            product.stock_qty += item.quantity

            db.add(InventoryLog(
                product_id=product.id,
                change_qty=item.quantity,
                reason="cancel_order"
            ))

        order.status = "cancelled"
        
        db.commit()
        
        return order

    # -------------------------------------------------

    def get_customer_orders(self, db, customer_id):
        return db.query(Order).filter(
            Order.customer_id == customer_id
        ).order_by(Order.id.desc()).all()