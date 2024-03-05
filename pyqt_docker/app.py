import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class OrderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주문 생성")

        self.label = QLabel("제품명:", self)
        self.label.move(50, 50)

        self.button = QPushButton("주문 생성", self)
        self.button.move(150, 100)
        self.button.clicked.connect(self.create_order)

    def create_order(self):
        # 주문 생성 로직 구현
        print("주문이 생성되었습니다.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderWindow()
    window.show()
    sys.exit(app.exec())