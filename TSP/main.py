import sys
import os
import webbrowser
import time
import tracemalloc

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QLabel, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Các thuật toán
from Algorithms import GBFS1, GBFS2, GBFS2Expan, GBFS3, Backtracking, GA, BTTT

class TSP_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đề tài: Bài toán TSP sử dụng Greedy Best First Search")
        self.resize(1400, 600)

        self.current_algorithm_func = None

        main_layout = QHBoxLayout(self)

        # ==== CỘT TRÁI: Nút thuật toán ====
        self.left_panel = QVBoxLayout()
        algorithms = [
            ("GBFS: Trường hợp 1", self.run_gbfs1),
            ("GBFS: Trường hợp 2", self.run_gbfs2),
            ("GBFS: Mở rộng Trường hợp 2", self.run_gbfs2ex),
            ("GBFS: Trường hợp 3", self.run_gbfs3),
            ("Backtracking", self.run_backtracking),
            ("GA", self.run_ga),
            ("Bài toán thực tế", self.run_bttt),
        ]
        for label, func in algorithms:
            btn = QPushButton(label)
            btn.setFixedWidth(200)
            btn.clicked.connect(func)
            self.left_panel.addWidget(btn)

        # ==== CỘT GIỮA: Canvas + Input ====
        self.center_panel = QVBoxLayout()

        # Vùng vẽ matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.center_panel.addWidget(self.canvas)

        # Nhập thành phố xuất phát
        self.input_start = QLineEdit()
        self.input_start.setPlaceholderText("Nhập thành phố hoặc quận bắt đầu")
        self.input_start.returnPressed.connect(self.trigger_current_algorithm)
        self.center_panel.addWidget(self.input_start)

        # Nhập danh sách quận cho BTTT
        self.input_districts = QTextEdit()
        self.input_districts.setPlaceholderText("Chỉ dành cho BTTT: Nhập danh sách quận, cách nhau bằng dấu phẩy")
        self.input_districts.setVisible(False)
        self.center_panel.addWidget(self.input_districts)

        # Nút mở HTML cho BTTT
        self.open_html_button = QPushButton("Mở bản đồ HTML")
        self.open_html_button.setVisible(False)
        self.open_html_button.clicked.connect(self.open_html)
        self.center_panel.addWidget(self.open_html_button)

        # Nút xóa canvas
        self.clear_btn = QPushButton("Xóa đồ thị hiện tại") 
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.center_panel.addWidget(self.clear_btn)

        # ==== CỘT PHẢI: Log Panel ====
        self.right_panel = QVBoxLayout()
        self.right_panel.addWidget(QLabel("Lịch sử chạy"))
        self.log_panel = QTextEdit()
        self.log_panel.setFixedWidth(300)
        self.log_panel.setReadOnly(True)
        self.right_panel.addWidget(self.log_panel)

        # ==== THÊM 3 CỘT VÀO layout CHÍNH ====
        main_layout.addLayout(self.left_panel, 1)   # Cột trái
        main_layout.addLayout(self.center_panel, 3) # Cột giữa
        main_layout.addLayout(self.right_panel, 2)  # Cột phải


    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()
        self.input_districts.setVisible(False)
        self.open_html_button.setVisible(False)

    def trigger_current_algorithm(self):
        if self.current_algorithm_func:
            self.current_algorithm_func()

    def run_backtracking(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_backtracking

        city = self.input_start.text().strip().upper()
        if city in Backtracking.graph:
            tracemalloc.start()
            start_time = time.time()

            Backtracking.best_path = None
            Backtracking.best_cost = float('inf')
            Backtracking.backtrack_tsp(city, {city}, [city], 0, city)

            elapsed = time.time() - start_time

            if Backtracking.best_path:
                Backtracking.draw_path(Backtracking.graph, Backtracking.best_path, ax=self.figure.gca())
                self.canvas.draw()
                self.log_result("Backtracking", Backtracking.best_cost, Backtracking.best_path, elapsed)
            else:
                self.log_result("Backtracking", None, path=None, elapsed_time=elapsed)

            tracemalloc.stop()


    def run_ga(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_ga

        city = self.input_start.text().strip().upper()
        if city in GA.graph:
            tracemalloc.start()
            start_time = time.time()

            path, cost = GA.genetic_algorithm(city)

            elapsed = time.time() - start_time
            GA.draw_path(GA.graph, path, ax=self.figure.gca())
            self.canvas.draw()
            self.log_result("Genetic Algorithm", cost, path, elapsed)

            tracemalloc.stop() 

    def run_gbfs1(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_gbfs1

        city = self.input_start.text().strip().upper()
        if city in GBFS1.graph:
            tracemalloc.start()
            start_time = time.time()

            path, cost = GBFS1.greedy_best_first_search(GBFS1.graph, city)
            elapsed = time.time() - start_time

            GBFS1.draw_graph(GBFS1.graph, path, ax=self.figure.gca())
            self.canvas.draw()
            self.log_result("GBFS1", cost if path else None, path, elapsed)

            tracemalloc.stop()

    def run_gbfs2(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_gbfs2

        city = self.input_start.text().strip().upper()
        if city in GBFS2.graph:
            tracemalloc.start()
            start_time = time.time()

            path, cost = GBFS2.greedy_best_first_search(GBFS2.graph, city)
            elapsed = time.time() - start_time

            GBFS2.draw_graph(GBFS2.graph, path, ax=self.figure.gca())
            self.canvas.draw()
            self.log_result("GBFS2", cost if path else None, path, elapsed)

            tracemalloc.stop()

    def run_gbfs2ex(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_gbfs2ex

        city = self.input_start.text().strip().upper()
        if city in GBFS2Expan.graph:
            tracemalloc.start()
            start_time = time.time()

            path, cost = GBFS2Expan.greedy_best_first_search_Ex(GBFS2Expan.graph, city)
            elapsed = time.time() - start_time

            if path:
                GBFS2Expan.draw_graph(GBFS2Expan.graph, path, ax=self.figure.gca())
                self.canvas.draw()

            self.log_result("GBFS2 with Backtrack", cost if path else None, path, elapsed)

            tracemalloc.stop()

    def run_gbfs3(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_gbfs3

        city = self.input_start.text().strip().upper()
        if city in GBFS3.graph:
            tracemalloc.start()
            start_time = time.time()

            path, cost = GBFS3.greedy_best_first_search(GBFS3.graph, city)
            elapsed = time.time() - start_time

            GBFS3.draw_graph(GBFS3.graph, path, ax=self.figure.gca())
            self.canvas.draw()
            self.log_result("GBFS3", cost if path else None, path, elapsed)

            tracemalloc.stop()       

    def run_bttt(self):
        self.clear_canvas()
        self.current_algorithm_func = self.run_bttt

        self.input_districts.setVisible(True)
        self.open_html_button.setVisible(False)

        raw = self.input_districts.toPlainText()
        selected = [x.strip().title() for x in raw.split(",") if x.strip().title() in BTTT.positions]
        start = self.input_start.text().strip().title()

        if len(selected) >= 2 and start in selected:
            tracemalloc.start()
            start_time = time.time()

            graph = BTTT.create_graph(selected)
            path, cost = BTTT.greedy_best_first_search(graph, start)

            elapsed = time.time() - start_time

            if path:
                BTTT.draw_map(path, selected, start)
                self.open_html_button.setVisible(True)

            self.log_result("Bài toán thực tế", cost if path else None, path, elapsed)

            tracemalloc.stop()
        else:
            print("Vui lòng nhập đúng các quận và quận xuất phát.")


    def open_html(self):
        file_path = "Algorithms/tsp_tp_hcm.html"
        if os.path.exists(file_path):
            webbrowser.open(f"file://{os.path.abspath(file_path)}")
        else:
            print("File HTML chưa tồn tại.")
        
    def log_result(self, algorithm_name, cost, path=None, elapsed_time=None):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        mem_current, mem_peak = tracemalloc.get_traced_memory()

        if path:
            path_str = " → ".join(path)
        else:
            path_str = "Không có đường đi"

        log_entry = (
            f"[{current_time}] Thuật toán: {algorithm_name}\n"
            f"  - Thời gian chạy: {elapsed_time:.20f} giây\n"
            f"  - Đường đi: {path_str}\n"
            f"  - Tổng chi phí: {cost if path else '---'}\n"
            f"  - Bộ nhớ sử dụng: {mem_current / 1024:.2f} KB (tối đa {mem_peak / 1024:.2f} KB)\n"
            f"{'-'*60}\n"
        )
        self.log_panel.append(log_entry)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TSP_GUI()
    window.show()
    sys.exit(app.exec())
