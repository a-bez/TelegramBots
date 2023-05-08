import sqlite3
import telebot
from threading import Thread

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

bot = telebot.TeleBot('TOKEN')

# Подключение к базе данных SQLite
conn = sqlite3.connect('tg_users.db', check_same_thread=False)
cursor = conn.cursor()

# Получение списка всех пользователей из базы данных
def get_users():
    users = []
    cursor.execute('SELECT user_id FROM users')
    rows = cursor.fetchall()
    for row in rows:
        users.append(row[0])
    return users

# Отправка сообщения всем пользователям
def send_message_to_all_users(text):
    users = get_users()
    for user in users:
        try:
            bot.send_message(user, text)
        except Exception as e:
            print(f'Error sending message to user {user}: {e}')

# Обработка команды /send
@bot.message_handler(commands=['send'])
def handle_send_command(message):
    if message.chat.id == 675884947:
        text = 'THE TEXT OF MESSAGE'
        send_message_to_all_users(text)
        bot.reply_to(message, 'Message sent to all users.')
    else:
        bot.reply_to(message, 'You are not authorized to use this command.')

import sqlite3

# Функция обработки callback query
def callback_handler(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    # Помечаем пользователя как активного в базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET status = "активен" WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    # Отправляем пользователю сообщение об успешной обработке callback query
    query.answer(text="Спасибо за ответ!")


def check_user_state(message):
    chat_id = message.chat.id
    # проверка, есть ли пользователь в базе
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    if result is None:
        # добавление нового пользователя в базу со статусом "не активен"
        cursor.execute("INSERT INTO users (chat_id, state) VALUES (?, ?)", (chat_id, "non_active"))
        conn.commit()
    else:
        # обновление состояния пользователя в базе
        cursor.execute("UPDATE users_state SET state=? WHERE chat_id=?", ("active", chat_id))
        conn.commit()

# обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # отправка сообщения
    bot.send_message(message.chat.id)

    # запуск функции проверки состояния пользователя в отдельном потоке
    t = Thread(target=check_user_state, args=(message,))
    t.start()

        
bot.polling()
