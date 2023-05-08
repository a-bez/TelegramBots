import sqlite3

# подключение к базе данных
conn = sqlite3.connect('users.db')

# создание таблицы
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
             chat_id INTEGER NOT NULL,
             name TEXT NOT NULL,
             state TEXT);''')

# закрытие соединения
conn.close()
