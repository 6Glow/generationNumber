import sys
import re
import csv

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox,QProgressBar, QHBoxLayout, QMessageBox

from PyQt6.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import random


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Загрузка")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.loading_label = QLabel("Загрузка...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setContentsMargins(0, 10, 0, 0)  # Установка отступа сверху
        self.loading_label.setStyleSheet("QLabel { color: white; }")  # Установка цвета текста
        # self.loading_label.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))  # Установка шрифта и размера

        # font_id = QFontDatabase.addApplicationFont("../FONTS/With_cerilitsa/Anaktoria/Anaktoria.ttf")
        # # # font_id = QFontDatabase.addApplicationFont("../FONTS/Without_cerilitsa/Merriweather/Merriweather-Light.ttf")
        # font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # font = QFont(font_family, 16, QFont.Weight.Light)
        # self.loading_label.setFont(font)

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

        # Открытие первого экрана
        self.firstScreen = FirstScreen()
        self.firstScreen.show()

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
            self.msleep(20)


class FirstScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приложение")
        self.setFixedSize(600, 400)

        self.label = QLabel("Вставьте ссылку:")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.linkLineEdit = QLineEdit()
        self.linkLineEdit.setToolTip("Введите ссылку в это поле")

        self.generateButton = QPushButton("Продолжить")
        self.generateButton.setToolTip("Нажмите, чтобы перейти к следующему экрану")

        self.darkModeCheckBox = QCheckBox("Включить / Выключить темный режим")

        # Размещение виджетов на вертикальной компоновке
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.linkLineEdit)
        vbox.addWidget(self.generateButton)
        vbox.addWidget(self.darkModeCheckBox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.generateButton.clicked.connect(self.showSecondScreen)

        self.darkModeCheckBox.stateChanged.connect(self.toggleDarkMode)

        self.darkModeCheckBox.setChecked(True)

    def showSecondScreen(self):
        link = self.linkLineEdit.text()

        if "http://" not in link and "https://" not in link:
            link = "http://" + link

        if "www" not in link:
            link = link.replace("://", "://www.")

        if "www" not in link:
            link = "www." + link

        if ".org" not in link and ".com" not in link and ".net" not in link:
            self.statusBar().showMessage("Ошибка! Введите корректную ссылку.")
            return

        self.secScreen = SecondScreen(link, self.darkModeCheckBox.isChecked())
        self.secScreen.show()
        self.close()

    def toggleDarkMode(self, state):

        palette = self.palette()

        if state == 2:  # Если чекбокс отмечен, включить темный режим
            palette.setColor(QPalette.ColorRole.Window, QColor("black"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))

        else:  # Иначе выключить темный режим
            palette.setColor(QPalette.ColorRole.Window, QColor("white"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        self.setPalette(palette)


class SecondScreen(QWidget):
    def __init__(self, link, darkMode):
        super().__init__()
        self.link = link
        self.darkMode = darkMode
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приложение")
        self.setFixedSize(600, 400)

        self.nameLabel = QLabel("Имя:")
        self.nameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setToolTip("Введите ваше имя")

        self.linkLabel = QLabel("Ссылка:")
        self.linkLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.linkLineEdit = QLineEdit(self.link)
        self.linkLineEdit.setReadOnly(True)

        self.phoneLabel = QLabel("Номер телефона:")
        self.phoneLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.phoneLineEdit = QLineEdit()
        self.phoneLineEdit.setReadOnly(True)

        self.generateButton = QPushButton("Генерация номера мобильного телефона")
        self.generateButton.setToolTip("Нажмите, чтобы сгенерировать номер телефона")

        self.confirmButton = QPushButton("Подтвердить")
        self.confirmButton.setToolTip("Нажмите, чтобы вернуться на первый экран")

        self.saveButton = QPushButton("Сохранить")
        self.saveButton.setToolTip("Нажмите, чтобы сохранить информацию")

        hbox = QHBoxLayout()
        hbox.addWidget(self.generateButton)
        hbox.addWidget(self.confirmButton)
        hbox.addWidget(self.saveButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.nameLineEdit)
        vbox.addWidget(self.linkLabel)
        vbox.addWidget(self.linkLineEdit)
        vbox.addWidget(self.phoneLabel)
        vbox.addWidget(self.phoneLineEdit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.generateButton.clicked.connect(self.generatePhone)
        self.confirmButton.clicked.connect(self.showFirstScreen)
        self.saveButton.clicked.connect(self.save_info)

        if self.darkMode:  # Если включен темный режим, применить соответствующую палитру
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor("black"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))

            self.generateButton.setStyleSheet('background-color: white; color: black;')

            self.setPalette(palette)

        self.setGeometry(0, 0, 800, 600)

    def generatePhone(self):
        generatedPhone = generate_phone_number()
        self.phoneLineEdit.setText(generatedPhone)

    def showFirstScreen(self):
        name = self.nameLineEdit.text()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите имя.")
            return
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', self.nameLineEdit.text()):
            QMessageBox.warning(self, "Ошибка", "Допускается только имя на латинице или на кириллице")
            return
        self.firstScreen = FirstScreen()
        self.firstScreen.show()
        self.close()

    def save_info(self):
        name = self.nameLineEdit.text()
        phone = self.phoneLineEdit.text()

        with open('generated_info.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone])


def generate_phone_number():
    operators = ["29", "25", "33", "44"]
    operator_code = random.choice(operators)
    region_code = random.randint(1, 9)
    unique_number = random.randint(100000, 999999)

    phone_number = f"+375 {operator_code} {region_code}{unique_number}"
    return phone_number


number = generate_phone_number()
# print(number)


if __name__ == '__main__':
    app = QApplication([])
    splashScreen = SplashScreen()
    splashScreen.start_loading_animation()
    splashScreen.show()
    sys.exit(app.exec())
