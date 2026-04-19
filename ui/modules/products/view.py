from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QFormLayout, QSpinBox, QDoubleSpinBox,
    QFrame
)

from ui.modules.products.controller import ProductsController


class ProductsView(QWidget):
    
    def __init__(self):
        
        super().__init__()

        self.controller = ProductsController()
        self.selected_id = None

        self.build_ui()
        self.load_products()

    # -------------------------------------------------

    def build_ui(self):
        
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        # LEFT
        left = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or SKU...")
        self.search_input.textChanged.connect(self.search_products)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "SKU", "Price", "Stock"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.cellClicked.connect(self.select_row)

        left.addWidget(self.search_input)
        left.addWidget(self.table)

        # RIGHT
        panel = QFrame()
        panel.setFixedWidth(360)

        right = QVBoxLayout(panel)

        form_title = QLabel("Product Details")
        form_title.setStyleSheet("font-size:20px;font-weight:bold;")

        form = QFormLayout()

        self.name_input = QLineEdit()
        self.sku_input = QLineEdit()

        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999)
        self.price_input.setDecimals(2)

        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(999999)

        form.addRow("Name:", self.name_input)
        form.addRow("SKU:", self.sku_input)
        form.addRow("Price:", self.price_input)
        form.addRow("Stock:", self.stock_input)

        self.btn_add = QPushButton("Add")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_clear = QPushButton("Clear")

        self.btn_add.clicked.connect(self.add_product)
        self.btn_update.clicked.connect(self.update_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_clear.clicked.connect(self.clear_form)

        right.addWidget(form_title)
        right.addLayout(form)
        right.addSpacing(20)
        right.addWidget(self.btn_add)
        right.addWidget(self.btn_update)
        right.addWidget(self.btn_delete)
        right.addWidget(self.btn_clear)
        right.addStretch()

        root.addLayout(left, 3)
        root.addWidget(panel, 1)

        self.setStyleSheet("""
            QWidget {
                background:#121212;
                color:white;
                font-size:14px;
            }

            QLineEdit, QSpinBox, QDoubleSpinBox {
                background:#1e1e1e;
                border:1px solid #333;
                padding:8px;
                border-radius:6px;
                color:white;
            }

            QPushButton {
                background:#2563eb;
                border:none;
                padding:10px;
                border-radius:8px;
                font-weight:bold;
            }

            QPushButton:hover {
                background:#1d4ed8;
            }

            QTableWidget {
                background:#1a1a1a;
                border:none;
                gridline-color:#2a2a2a;
            }

            QHeaderView::section {
                background:#222;
                padding:8px;
                border:none;
                font-weight:bold;
            }

            QFrame {
                background:#1b1b1b;
                border-radius:12px;
            }
        """)

    # -------------------------------------------------

    def load_products(self):
        
        products = self.controller.get_all_products()

        self.table.setRowCount(0)

        for row, p in enumerate(products):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setItem(row, 2, QTableWidgetItem(p.sku))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.price)))
            self.table.setItem(row, 4, QTableWidgetItem(str(p.stock_qty)))

    # -------------------------------------------------

    def search_products(self):
        
        text = self.search_input.text().strip()

        if not text:
            self.load_products()
            return

        products = self.controller.search_products(text)

        self.table.setRowCount(0)

        for row, p in enumerate(products):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            self.table.setItem(row, 2, QTableWidgetItem(p.sku))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.price)))
            self.table.setItem(row, 4, QTableWidgetItem(str(p.stock_qty)))

    # -------------------------------------------------

    def select_row(self, row, _):
        
        self.selected_id = int(self.table.item(row, 0).text())

        self.name_input.setText(self.table.item(row, 1).text())
        self.sku_input.setText(self.table.item(row, 2).text())
        self.price_input.setValue(float(self.table.item(row, 3).text()))
        self.stock_input.setValue(int(self.table.item(row, 4).text()))

    # -------------------------------------------------

    def add_product(self):
        
        try:
            self.controller.add_product(
                self.name_input.text().strip(),
                self.sku_input.text().strip(),
                self.price_input.value(),
                self.stock_input.value()
            )

            self.load_products()
            self.clear_form()

            QMessageBox.information(self, "Success", "Product added.")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------------------------------

    def update_product(self):
        
        if not self.selected_id:
            return

        try:
            self.controller.update_product(
                self.selected_id,
                self.name_input.text().strip(),
                self.sku_input.text().strip(),
                self.price_input.value(),
                self.stock_input.value()
            )

            self.load_products()
            self.clear_form()

            QMessageBox.information(self, "Success", "Product updated.")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------------------------------

    def delete_product(self):
        
        if not self.selected_id:
            return

        confirm = QMessageBox.question(
            self,
            "Delete",
            "Delete selected product?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.delete_product(self.selected_id)

            self.load_products()
            self.clear_form()

            QMessageBox.information(self, "Success", "Product deleted.")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------------------------------

    def clear_form(self):
        
        self.selected_id = None
        self.name_input.clear()
        self.sku_input.clear()
        self.price_input.setValue(0)
        self.stock_input.setValue(0)