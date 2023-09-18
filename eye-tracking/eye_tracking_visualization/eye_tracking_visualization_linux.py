import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import threading
import queue


class LogReader(QThread):
    new_point = pyqtSignal(int, int)

    def __init__(self, file_path, log_queue):
        super().__init__()
        self.file_path = file_path
        self.log_queue = log_queue

    def run(self):
        with open(self.file_path, 'r') as log_file:
            log_file.seek(0, 2)
            while True:
                line = log_file.readline()
                if line:
                    components = line.strip().split(',')
                    x_coord = int(float(components[1]))
                    y_coord = int(float(components[2]))
                    self.new_point.emit(x_coord, y_coord)
                else:
                    time.sleep(0.01)


class PointVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.points = []
        self.x = 0
        self.y = 0
        self.init_ui()

        # add path to tobii logs here
        self.log_reader = LogReader('/home/mkopcz/Desktop/contextual-emotion/examination/tobi_logs/logs.txt', self.points)
        self.log_reader.new_point.connect(self.add_point)
        self.log_reader.start()

    def init_ui(self):

        self.setGeometry(0, 0, QApplication.desktop().width(),
                         QApplication.desktop().height())
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(Qt.Window | Qt.X11BypassWindowManagerHint |
                            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.quit_widget = QWidget()
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.quit)
        self.quit_window = QMainWindow()
        self.quit_window.setCentralWidget(self.quit_widget)
        self.quit_window.setWindowTitle("Quit")
        self.quit_window.setGeometry(0, 0, 100, 50)
        self.quit_window.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.quit_window.setAttribute(Qt.WA_TranslucentBackground)

        # Add Quit button to main window layout
        main_layout = QGridLayout()
        main_layout.addWidget(self.quit_button, 0, 0,
                              Qt.AlignRight | Qt.AlignTop)
        self.quit_widget.setLayout(main_layout)

        # self.show()
        self.quit_window.show()

    def add_point(self, x, y):
        self.x = x
        self.y = y
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 70))
        painter.drawEllipse(self.x, self.y, 5, 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PointVisualizer()
    ex.show()
    sys.exit(app.exec_())