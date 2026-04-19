from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView,
    QMessageBox, QComboBox
)

from ui.modules.sales.controller import SalesController


class SalesView(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = SalesController()

        # STATE
        self.products_data = []
        self.cart_items = []
        self.selected_customer_id = None

        self.build_ui()
        self.apply_style()
        self.load_products()
        self.load_customers()

    # -----------------------------
    # UI
    # -----------------------------
    def build_ui(self):

        self.main = QVBoxLayout(self)

        # =========================
        # CUSTOMER SELECT (DB ONLY)
        # =========================
        self.bar_layout  = QHBoxLayout()
        
        self.customer_combo = QComboBox()
        self.customer_combo.currentIndexChanged.connect(self.select_customer)
        self.bar_layout.addWidget(self.customer_combo, 2)
        
        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.refresh)
        self.bar_layout.addWidget(self.refresh_btn, 1)
        
        self.main.addLayout(self.bar_layout)

        # SEARCH
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search products...")
        self.search.textChanged.connect(self.filter_products)

        self.main.addWidget(self.search)

        # BODY
        self.body = QHBoxLayout()

        # LEFT - PRODUCTS
        self.left_panel = QFrame()
        self.left_layout = QVBoxLayout(self.left_panel)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout(self.container)

        self.scroll.setWidget(self.container)

        self.left_layout.addWidget(self.scroll)

        # RIGHT - CART
        self.right_panel = QFrame()
        self.right_layout = QVBoxLayout(self.right_panel)

        self.right_title = QLabel("Cart")

        self.cart = QTableWidget()
        self.cart.setColumnCount(4)
        self.cart.setHorizontalHeaderLabels([
            "Item", "Quantity", "Price", "Total"
        ])

        self.cart.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.cart.cellClicked.connect(self.cart_click)

        self.total_label = QLabel("SYP 0.00")

        self.checkout_btn = QPushButton("CHECKOUT")
        self.checkout_btn.clicked.connect(self.checkout)

        self.clear_btn = QPushButton("CLEAR CART")
        self.clear_btn.clicked.connect(self.clear_cart)

        self.right_layout.addWidget(self.right_title)
        self.right_layout.addWidget(self.cart)
        self.right_layout.addWidget(self.total_label)
        self.right_layout.addWidget(self.checkout_btn)
        self.right_layout.addWidget(self.clear_btn)

        self.body.addWidget(self.left_panel)
        self.body.addWidget(self.right_panel)

        self.main.addLayout(self.body)

    # -----------------------------
    # LOAD CUSTOMERS (DB ONLY)
    # -----------------------------
    def load_customers(self):

        customers = self.controller.get_customers()

        self.customer_combo.clear()

        # Walk-in option
        self.customer_combo.addItem("Walk-in Customer", None)

        for c in customers:
            self.customer_combo.addItem(
                f"{c.name} | {c.phone}",
                c.id
            )

    # -----------------------------
    # SELECT CUSTOMER
    # -----------------------------
    def select_customer(self):

        self.selected_customer_id = self.customer_combo.currentData()

    # -----------------------------
    # LOAD PRODUCTS
    # -----------------------------
    def load_products(self):

        self.products_data = self.controller.load_products()
        self.render_products(self.products_data)

    # -----------------------------
    # FILTER PRODUCTS
    # -----------------------------
    def filter_products(self):

        text = self.search.text().lower().strip()

        if not text:
            self.render_products(self.products_data)
            return

        filtered = [
            p for p in self.products_data
            if text in p.name.lower()
        ]

        self.render_products(filtered)

    # -----------------------------
    # PRODUCT CARDS
    # -----------------------------
    def render_products(self, products):

        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        row = 0
        col = 0

        for product in products:

            card = QFrame()
            card.setFixedSize(150, 150)

            layout = QVBoxLayout(card)

            name  = QLabel(product.name)
            price = QLabel(f"SYP {product.price}")
            stock = QLabel(f"Stock: {product.stock_qty}")

            btn = QPushButton("ADD")
            btn.clicked.connect(
                lambda _, p=product: self.add_to_cart(p)
            )

            layout.addWidget(name)
            layout.addWidget(price)
            layout.addWidget(stock)
            layout.addStretch()
            layout.addWidget(btn)

            self.grid.addWidget(card, row, col)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    # -----------------------------
    # CART LOGIC
    # -----------------------------
    def add_to_cart(self, product):

        for item in self.cart_items:
            if item["product"].id == product.id:
                item["qty"] += 1
                self.render_cart()
                return

        self.cart_items.append({
            "product": product,
            "qty": 1
        })

        self.render_cart()

    # -----------------------------
    # CART RENDER
    # -----------------------------
    def render_cart(self):

        self.cart.setRowCount(0)

        total = 0

        for item in self.cart_items:

            product = item["product"]
            qty = item["qty"]

            row = self.cart.rowCount()
            self.cart.insertRow(row)

            line_total = qty * float(product.price)
            total += line_total

            self.cart.setItem(row, 0, QTableWidgetItem(product.name))
            self.cart.setItem(row, 1, QTableWidgetItem(f"{qty}"))
            self.cart.setItem(row, 2, QTableWidgetItem(str(product.price)))
            self.cart.setItem(row, 3, QTableWidgetItem(f"{line_total:.2f}"))

            self.cart.item(row, 0).setData(1000, product.id)

        self.total_label.setText(f"SYP {total:.2f}")

    # -----------------------------
    # CART INTERACTION
    # -----------------------------
    def cart_click(self, row, column):

        product_id = self.cart.item(row, 0).data(1000)

        item = next(
            (i for i in self.cart_items if i["product"].id == product_id),
            None
        )

        if not item:
            return

        if column == 1:
            item["qty"] += 1

        elif column == 2:
            item["qty"] -= 1
            if item["qty"] <= 0:
                self.cart_items.remove(item)

        elif column == 3:
            self.cart_items.remove(item)

        self.render_cart()

    # -----------------------------
    # CLEAR CART
    # -----------------------------
    def clear_cart(self):

        self.cart_items = []
        self.render_cart()

    # -----------------------------
    # CHECKOUT (FIXED)
    # -----------------------------
    def checkout(self):

        if not self.cart_items:
            QMessageBox.warning(self, "Cart", "Cart is empty")
            return

        items = []

        for item in self.cart_items:
            items.append({
                "product_id": item["product"].id,
                "qty": item["qty"]
            })

        try:
            # fallback to walk-in if none selected
            customer_id = self.selected_customer_id or 1

            self.controller.checkout(
                customer_id=customer_id,
                items=items
            )

            QMessageBox.information(
                self,
                "Success",
                "Order completed"
            )

            self.clear_cart()
            self.load_products()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )
        
    def refresh(self):
        self.load_customers()
        self.load_products()
        
    # -----------------------------
    # STYLE
    # -----------------------------
    def apply_style(self):

        self.setStyleSheet("""

        QWidget {
            background: #0f1115;
            color: white;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QFrame {
            background: #1a1d24;
            border-radius: 12px;
        }

        QLineEdit, QComboBox {
            background: #252932;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 10px;
        }

        QPushButton {
            background: #00c853;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }

        QPushButton:hover {
            background: #00e676;
        }

        QTableWidget {
            background: #252932;
            border: 1px solid #333;
            border-radius: 10px;
        }

        QHeaderView::section {
            background: #1f232b;
            padding: 8px;
            border: none;
            font-weight: bold;
        }

        QLabel {
            font-weight: bold;
        }

        """)