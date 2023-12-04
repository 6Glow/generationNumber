import sys
import random
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Загрузка")
        self.resize(300, 150)


        layout = QVBoxLayout()

        self.loading_label = QLabel("Loading...>")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setContentsMargins(0, 10, 0, 0)  # Установка отступа сверху
        self.loading_label.setStyleSheet("QLabel { color: white; }")  # Установка цвета текста
        self.loading_label.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))  # Установка шрифта и размера

        font_id = QFontDatabase.addApplicationFont("../FONTS/Without_cerilitsa/Merriweather/Merriweather-Light.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16, QFont.Weight.Light)
        self.loading_label.setFont(font)


        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)

        layout.addWidget(self.loading_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)


    def start_loading_animation(self):
        self.thread = LoadingThread()
        self.thread.progress_update.connect(self.update_progress)
        self.thread.finished.connect(self.load_next_file)
        self.thread.start()

    def load_next_file(self):

        # Закрытие окна загрузки
        self.close()


    def update_progress(self, value):
        self.progress_bar.setValue(value)
        # Изменение цвета на каждые 5%
        if value % 5 == 0:
            color = self.get_random_color()
            style_sheet = f"QProgressBar::chunk{{background-color: {color};}}"
            self.progress_bar.setStyleSheet(style_sheet)

            style_sheet += f"QLabel {{ border: 2px solid {color}; }}"
            self.loading_label.setStyleSheet(style_sheet)


    def get_random_color(self):
        random_color_model = random.choice(["RGB", "HSV", "CMYK"])
        if random_color_model == "RGB":
            return self.get_random_rgb_color()
        elif random_color_model == "HSV":
            return self.get_random_hsv_color()
        elif random_color_model == "CMYK":
            return self.get_random_cmyk_color()

    def get_random_rgb_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"rgb({r}, {g}, {b})"

    def get_random_hsv_color(self):
        h = random.randint(0, 359)
        s = random.randint(0, 255)
        v = random.randint(0, 255)
        color = QColor.fromHsv(h, s, v)
        return color.name()

    def get_random_cmyk_color(self):
        c = random.randint(0, 100)
        m = random.randint(0, 100)
        y = random.randint(0, 100)
        k = random.randint(0, 100)
        color = QColor.fromCmyk(c, m, y, k)
        return color.name()


class LoadingThread(QThread):
    progress_update = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.progress_update.emit(i)
            self.msleep(100)


if __name__ == "__main__":
    app = QApplication([])
    loading_screen = LoadingScreen()
    loading_screen.start_loading_animation()
    loading_screen.show()
    sys.exit(app.exec())
