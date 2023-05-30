import sqlite3
from telethon.sync import TelegramClient
from telethon.tl.functions.auth import SignInRequest

class TelegramRegistration:
    def __init__(self, db_file, api_id, api_hash):
        self.db_file = db_file
        self.api_id = api_id
        self.api_hash = api_hash

    def register_accounts(self):
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Получение данных для регистрации из базы данных
        cursor.execute("SELECT phone_number, confirmation_code FROM usersForRegistration")
        rows = cursor.fetchall()

        # Инициализация клиента Telegram
        client = TelegramClient('session', self.api_id, self.api_hash)
        client.start()

        # Регистрация аккаунтов
        for row in rows:
            phone_number = row[0]
            confirmation_code = row[1]

            try:
                # Регистрация аккаунта
                client(SignInRequest(phone_number, confirmation_code))

                print(f"Аккаунт с номером {phone_number} успешно зарегистрирован!")
            except Exception as e:
                print(f"Ошибка при регистрации аккаунта с номером {phone_number}: {str(e)}")

        # Закрытие соединения с базой данных
        conn.close()

# Пример использования
db_file = './registration_data.db'  # Путь к файлу базы данных
api_id = 'YOUR_API_ID'  # Ваш API ID Telegram
api_hash = 'YOUR_API_HASH'  # Ваш API Hash Telegram

registration = TelegramRegistration(db_file, api_id, api_hash)
registration.register_accounts()
