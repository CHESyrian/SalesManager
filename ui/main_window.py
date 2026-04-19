from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QListWidget,  QStackedWidget
)

from ui.modules.customers.view import CustomersView
from ui.modules.products.view import ProductsView
from ui.modules.sales.view import SalesView
from ui.modules.orders.view import OrdersView


class MainWindow(QMainWindow):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.setWindowTitle(f"Sales Manager - {user.username}")
        self.showMaximized()

        self.menu = QListWidget()
        self.menu.setFixedWidth(200)
        self.menu.addItems([
            "Dashboard", 
            "Customers", 
            "Products", 
            "Orders", 
            "POS System"
        ])

        self.stack = QStackedWidget()
        
        self.customers = CustomersView()
        self.products  = ProductsView()
        self.orders    = OrdersView()
        self.sales     = SalesView()

        self.stack.addWidget(QWidget())  # dashboard placeholder
        self.stack.addWidget(self.customers)
        self.stack.addWidget(self.products)
        self.stack.addWidget(self.orders)
        self.stack.addWidget(self.sales)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        layout = QHBoxLayout()
        layout.addWidget(self.menu)
        layout.addWidget(self.stack, 1)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
