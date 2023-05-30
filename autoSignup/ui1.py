import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from dialogManualReg import ManualRegistrationDialog
from dialogSemiManualReg import SemiManialRegistrationDialog
from dialogAutoReg import AutoRegistrationDialog
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Registration App')

        # Создание кнопок
        btn_auto = QPushButton('Автоматическая регистрация', self)
        btn_semi_auto = QPushButton('Полуавтоматическая регистрация', self)
        btn_manual = QPushButton('Механическая регистрация', self)

        # Создание вертикального макета и добавление кнопок
        layout = QVBoxLayout()
        layout.addWidget(btn_auto)
        layout.addWidget(btn_semi_auto)
        layout.addWidget(btn_manual)

        self.setLayout(layout)

        # Подключение обработчиков событий для кнопок
        btn_auto.clicked.connect(self.handle_auto_registration)
        btn_semi_auto.clicked.connect(self.handle_semi_auto_registration)
        btn_manual.clicked.connect(self.handle_manual_registration)

    def handle_auto_registration(self):
        # Вызов метода для автоматической регистрации из класса RegistrationHandler
        AutoRegistrationDialog().exec_()

    def handle_semi_auto_registration(self):
        # Вызов метода для полуавтоматической регистрации из класса RegistrationHandler
        SemiManialRegistrationDialog().exec_()

    def handle_manual_registration(self):
        # Вызов метода для механической регистрации из класса RegistrationHandler
        ManualRegistrationDialog().exec_()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создание экземпляра класса MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
