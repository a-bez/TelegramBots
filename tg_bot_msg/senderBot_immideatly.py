import requests
import sqlite3
import time

# подключение к базе данных
connection = sqlite3.connect('tg_users.db')
# создание таблицы
connection.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
             chat_id INTEGER NOT NULL,
             name TEXT NOT NULL);''')
# сейчас таблица пуста, но на тестовых данных работает отлично.

def sender():
    # подключение к базе данных
    connection = sqlite3.connect('tg_users.db')
    # извлечение значений таблицы
    cursor = connection.execute('''SELECT name, user_id FROM USERS''')

    TOKEN = "5891886347:AAEHei8Lge377MUAnQaFT0eiPDSxuxb2aUk"
    logs=[]
    for i in cursor:
        name=i[0]
        chat_id=i[1]
        message = f'Hello diar, {name}! Now I testing my new sender bot.'
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        logs.append(requests.get(url).json()) # отправка сообщений и сохранение логов
        time.sleep(1)
        connection.close()


sender()



