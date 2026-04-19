from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame
)

from PyQt6.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure

from ui.modules.dashboard.controller import DashboardController


class DashboardView(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = DashboardController()

        self.build_ui()
        self.apply_style()
        self.load_data()

        # -----------------------------
        # LIVE AUTO REFRESH
        # -----------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(5000)  # 5 sec refresh

    # -----------------------------
    # UI
    # -----------------------------
    def build_ui(self):

        root = QVBoxLayout(self)

        # =========================
        # KPI CARDS
        # =========================
        kpi = QHBoxLayout()

        self.card_sales = QLabel()
        self.card_orders = QLabel()
        self.card_products = QLabel()
        self.card_stock = QLabel()

        for c in [self.card_sales, self.card_orders,
                  self.card_products, self.card_stock]:
            c.setMinimumHeight(80)
            kpi.addWidget(c)

        # =========================
        # CHART AREA
        # =========================
        self.chart_frame = QFrame()
        chart_layout = QVBoxLayout(self.chart_frame)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        chart_layout.addWidget(self.canvas)

        # =========================
        # BOTTOM AREA
        # =========================
        bottom = QHBoxLayout()

        self.recent_orders = QLabel()
        self.low_stock = QLabel()

        bottom.addWidget(self.recent_orders)
        bottom.addWidget(self.low_stock)

        # =========================
        # ASSEMBLE
        # =========================
        root.addLayout(kpi)
        root.addWidget(self.chart_frame)
        root.addLayout(bottom)

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    def load_data(self):

        self.load_kpis()
        self.load_chart()
        self.load_recent_orders()
        self.load_low_stock()

    # -----------------------------
    # KPI
    # -----------------------------
    def load_kpis(self):

        self.card_sales.setText(
            f"Today Sales\n${self.controller.get_today_sales():.2f}"
        )

        self.card_orders.setText(
            f"Orders\n{self.controller.get_orders_count()}"
        )

        self.card_products.setText(
            f"Products\n{self.controller.get_products_count()}"
        )

        low = self.controller.get_low_stock()

        self.card_stock.setText(
            f"Low Stock\n{len(low)}"
        )

    # -----------------------------
    # CHART
    # -----------------------------
    def load_chart(self):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        data = self.controller.get_weekly_sales()

        if not data:
            ax.text(0.5, 0.5, "No Data",
                    ha="center", va="center")
            self.canvas.draw()
            return

        x = [str(d[0]) for d in data]
        y = [d[1] for d in data]

        ax.plot(x, y, marker="o")

        ax.set_title("Weekly Sales")
        ax.set_xlabel("Date")
        ax.set_ylabel("Revenue")

        self.figure.tight_layout()
        self.canvas.draw()

    # -----------------------------
    # RECENT ORDERS
    # -----------------------------
    def load_recent_orders(self):

        orders = self.controller.get_recent_orders()

        text = "Recent Orders\n\n"

        for o in orders:
            name = o.customer.name if o.customer else "Walk-in"
            text += f"#{o.id} - {name} - ${o.total_amount}\n"

        self.recent_orders.setText(text)

    # -----------------------------
    # LOW STOCK
    # -----------------------------
    def load_low_stock(self):

        products = self.controller.get_low_stock()

        text = "Low Stock\n\n"

        for p in products:
            text += f"{p.name} ({p.stock_qty})\n"

        self.low_stock.setText(text)

    # -----------------------------
    # STYLE
    # -----------------------------
    def apply_style(self):

        self.setStyleSheet("""

        QWidget {
            background: #0f1115;
            color: white;
            font-size: 14px;
        }

        QLabel {
            background: #1a1d24;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
        }

        QFrame {
            background: #1a1d24;
            border-radius: 12px;
        }

        """)