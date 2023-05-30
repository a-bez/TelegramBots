import sqlite3
from telethon.sync import TelegramClient
from telethon import functions, types

def register_account(phone_number, confirmation_code):
    api_id = 'YOUR_API_ID'  # Замените на свой API ID
    api_hash = 'YOUR_API_HASH'  # Замените на свой API Hash

    with TelegramClient('session_name', api_id, api_hash) as client:
        # Регистрация нового аккаунта
        result = client(functions.auth.SignUpRequest(
            phone=phone_number,
            first_name='First Name',
            last_name='Last Name',
            password='password'
        ))
        
        if isinstance(result, types.auth.AuthorizationSignUpRequired):
            # Ввод кода подтверждения
            client(functions.auth.SignInRequest(
                phone=phone_number,
                phone_code_hash=result.phone_code_hash,
                phone_code=confirmation_code
            ))

            # Сохранение номера телефона в базе данных
            save_phone_number(phone_number)
            

def save_phone_number(phone_number):
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')  # Замените 'database.db' на имя вашей базы данных
    cursor = conn.cursor()
    
    # Создание таблицы, если она не существует
    cursor.execute('CREATE TABLE IF NOT EXISTS users (phone_number TEXT, registered BOOLEAN)')
    
    # Вставка номера телефона в базу данных
    cursor.execute('INSERT INTO users (phone_number, registered) VALUES (?, ?)', (phone_number, True))
    
    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()

# Пример использования функции
phone_number = input('Введите номер телефона: ')
confirmation_code = input('Введите код подтверждения: ')
register_account(phone_number, confirmation_code)
