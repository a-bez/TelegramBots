import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QLineEdit
import sqlite3

class ManualRegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        #  название диалогового окна
        self.setWindowTitle("Ручная регистрация в ТГ")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.phone_label = QLabel("Номер телефона:")
        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_input)

        self.code_label = QLabel("Код подтверждения:")
        self.code_input = QLineEdit()
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_input)

        self.confirm_button = QPushButton("Зарегистрировать")
        self.layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.register_user)

    def register_user(self):
        phone_number = self.phone_input.text()
        verification_code = self.code_input.text()

        self.save_registration_data(phone_number)

        # Здесь можно добавить код для регистрации пользователя в Телеграме
        # с использованием номера телефона и кода подтверждения

        self.accept()

    def save_registration_data(self, phone_number):
        # Пример сохранения номера телефона в базу данных
        connection = sqlite3.connect("./registration_data.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rented_numbers (phone_number, registered) VALUES (?, ?)",
                       (phone_number, False))
        connection.commit()
        connection.close()

class SemiAutomaticRegistrationDialog(QDialog):
    def __init__(self, phone_number):
        super().__init__()
        self.setWindowTitle("Полуавтоматическая регистрация в ТГ")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.phone_label = QLabel("Номер телефона:")
        self.phone_input = QLineEdit()
        self.phone_input.setText(phone_number)  # Установка значения из БД
        self.phone_input.setReadOnly(True)  # Запрет редактирования
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_input)

        self.code_label = QLabel("Код подтверждения:")
        self.code_input = QLineEdit()
        self.layout.addWidget(self.code_label)
        self.layout.addWidget(self.code_input)

        self.confirm_button = QPushButton("Зарегистрировать")
        self.layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.register_user)

    def register_user(self):
        phone_number = self.phone_input.text()
        verification_code = self.code_input.text()

        self.save_registration_data(phone_number)

        # Здесь можно добавить код для регистрации пользователя в Телеграме
        # с использованием номера телефона и кода подтверждения

        self.accept()

    def save_registration_data(self, phone_number):
        # сохранения номера телефона в базу данных
        connection = sqlite3.connect("./registration_data.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rented_numbers (phone_number, registered) VALUES (?, ?)",
                       (phone_number, False))
        connection.commit()
        connection.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Телеграм Регистрация")
        self.setGeometry(200, 200, 300, 200)

        self.manual_registration_button = QPushButton("Ручная регистрация в ТГ", self)
        self.manual_registration_button.setGeometry(50, 50, 200, 30)
        self.manual_registration_button.clicked.connect(self.show_manual_registration_dialog)

        self.semi_automatic_registration_button = QPushButton("Полуавтоматическая регистрация в ТГ", self)
        self.semi_automatic_registration_button.setGeometry(50, 100, 250, 30)
        self.semi_automatic_registration_button.clicked.connect(self.show_semi_automatic_registration_dialog)

    def show_manual_registration_dialog(self):
        dialog = ManualRegistrationDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.mark_as_registered(dialog.phone_input.text())

    def show_semi_automatic_registration_dialog(self):
        phone_number = self.get_phone_number_from_database()  # Получение номера из БД
        dialog = SemiAutomaticRegistrationDialog(phone_number)
        if dialog.exec_() == QDialog.Accepted:
            self.mark_as_registered(dialog.phone_input.text())

    def get_phone_number_from_database(self):
        # Пример получения номера из базы данных
        connection = sqlite3.connect("./registration_data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT phone_number FROM rented_numbers WHERE registered = ?", (False,))
        result = cursor.fetchone()
        connection.close()

        if result:
            return result[0]
        else:
            return ""

    def mark_as_registered(self, phone_number):
        # Обновление статуса регистрации в БД
        connection = sqlite3.connect("./registration_data.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE rented_numbers SET registered = ? WHERE phone_number = ?",
                       (True, phone_number))
        connection.commit()
        connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
