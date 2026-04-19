from domain.models.product import Product


class ProductService:

    def create_product(self, db, name, sku, price, stock_qty):
        product = Product(
            name=name,
            sku=sku,
            price=price,
            stock_qty=stock_qty
        )
        db.add(product)
        db.commit()
        return product

    def get_all_products(self, db):
        return db.query(Product).order_by(Product.name).all()

    def get_available_products(self, db):
        return db.query(Product).filter(
            Product.stock_qty > 0
        ).order_by(Product.name).all()

    def get_by_sku(self, db, sku):
        return db.query(Product).filter(
            Product.sku == sku
        ).first()

    def search_products(self, db, keyword):
        return db.query(Product).filter(
            Product.name.ilike(f"%{keyword}%")
        ).all()

    def update_product(self, db, product_id, **kwargs):
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            return None

        for k, v in kwargs.items():
            setattr(product, k, v)

        db.flush()
        return product

    def delete_product(self, db, product_id):
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            return False

        db.delete(product)
        db.commit()
        return True