from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox,
    QHeaderView, QFrame
)

from ui.modules.orders.controller import OrdersController


class OrdersView(QWidget):
    
    def __init__(self):
        super().__init__()

        self.controller = OrdersController()
        self.selected_order_id = None

        self.build_ui()
        self.load_orders()

    # ---------------------------------------------

    def build_ui(self):
        root = QVBoxLayout(self)

        # TOP BAR
        top = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Order ID...")

        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.load_orders)

        top.addWidget(self.search_input)
        top.addWidget(btn_refresh)

        # ORDERS TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Customer", "Total", "Status", "Date"]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.cellClicked.connect(self.select_order)

        # DETAILS AREA
        self.details = QLabel("Select an order to view details")
        self.details.setFrameStyle(QFrame.Shape.Box)
        self.details.setMinimumHeight(120)

        # ACTIONS
        self.btn_cancel = QPushButton("Cancel Order")
        self.btn_cancel.clicked.connect(self.cancel_order)

        # LAYOUT
        root.addLayout(top)
        root.addWidget(self.table)
        root.addWidget(self.details)
        root.addWidget(self.btn_cancel)

        # STYLE
        self.setStyleSheet("""
            QWidget {
                background:#121212;
                color:white;
                font-size:14px;
            }

            QLineEdit {
                padding:8px;
                background:#1e1e1e;
                border:1px solid #333;
                border-radius:6px;
            }

            QPushButton {
                background:#2563eb;
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
            }

            QLabel {
                padding:10px;
                background:#1e1e1e;
                border-radius:6px;
            }
        """)

    # ---------------------------------------------

    def load_orders(self):
        orders = self.controller.get_all_orders()
        
        self.table.setRowCount(0)

        for row, o in enumerate(orders):
            self.table.insertRow(row)

            customer_name = o.customer.name if o.customer else "Walk-in"

            self.table.setItem(row, 0, QTableWidgetItem(str(o.id)))
            self.table.setItem(row, 1, QTableWidgetItem(customer_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(o.total_amount)))
            self.table.setItem(row, 3, QTableWidgetItem(o.status))
            self.table.setItem(row, 4, QTableWidgetItem(str(o.created_at)))

    # ---------------------------------------------

    def select_order(self, row, _):
        self.selected_order_id = int(self.table.item(row, 0).text())

        order = self.controller.get_order(self.selected_order_id)

        if not order:
            return

        items_text = "Items:\n"

        for item in order.items:
            items_text += (
                f"- {item.product.name} "
                f"(x{item.quantity}) = {item.unit_price}\n"
            )

        self.details.setText(
            f"Order ID: {order.id}\n"
            f"Customer: {order.customer.name if order.customer else 'Walk-in'}\n"
            f"Total: {order.total_amount}\n"
            f"Status: {order.status}\n\n"
            f"{items_text}"
        )

    # ---------------------------------------------

    def cancel_order(self):
        if not self.selected_order_id:
            return

        confirm = QMessageBox.question(
            self,
            "Cancel Order",
            "Cancel this order and restore stock?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.cancel_order(self.selected_order_id)

            self.load_orders()
            self.details.setText("Select an order to view details")

            QMessageBox.information(
                self,
                "Success",
                "Order cancelled and stock restored."
            )

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))