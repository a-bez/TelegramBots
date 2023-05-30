import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout


class AutoRegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Автоматична реєстрація користувачів')

        # Создание подписей и полей ввода
        self.phone_label = QLabel('Номер телефону:')
        self.phone_edit = QLineEdit()
        self.name_label = QLabel('Ім\'я користувача:')
        self.name_edit = QLineEdit()
        self.lastName_label = QLabel('Прізвище Користувача:')
        self.lastName_edit = QLineEdit()
        self.password_label = QLabel('Введіть пароль:')
        self.password_edit = QLineEdit()
        self.code_label = QLabel('Код підтверждення:')
        self.code_edit = QLineEdit()

        # Создание кнопки "Зарегистрировать"
        self.register_button = QPushButton('Зареєструвати')
        self.send_code_button = QPushButton('Відправити данні та отримати код на номер')

        # Создание вертикального макета и добавление элементов
        layout = QVBoxLayout()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_edit)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.lastName_label)
        layout.addWidget(self.lastName_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.send_code_button)
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_edit)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        # Подключение обработчика события нажатия кнопки
        self.register_button.clicked.connect(self.register)

    def register(self):
        # Получение введенных данных
        phone = self.phone_edit.text()
        name = self.name_edit.text()
        lastName = self.lastName_edit.text()
        password = self.password_edit.text()
        code = self.code_edit.text()

        # Вызов функции регистрации с полученными данными
        from manualSignUpCls import register_account, save_phone_number
        registration_handler.register(phone, name, lastName, password, code)


class RegistrationHandler:
    def register(self, phone, code):
        print('Регистрация:')
        print('Номер телефона:', phone)
        print('Код подтверждения:', code)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создание экземпляра класса RegistrationHandler
    registration_handler = RegistrationHandler()

    # Создание экземпляра класса RegistrationDialog
    dialog = AutoRegistrationDialog()
    dialog.exec_()
