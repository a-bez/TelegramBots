import sqlite3
import telebot
import threading
import time

# Подключение к базе данных
conn = sqlite3.connect('users2.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('CREATE TABLE IF NOT EXISTS users2 (id INTEGER PRIMARY KEY, chat_id INTEGER, is_active INTEGER)')

# Получение списка всех активных пользователей
def get_active_users():
    cursor.execute('SELECT chat_id FROM users2 WHERE is_active=1')
    return [row[0] for row in cursor.fetchall()]

# Установка статуса пользователя в "неактивный"
def set_user_inactive(chat_id):
    cursor.execute('UPDATE users2 SET is_active=0 WHERE chat_id=?', (chat_id,))
    conn.commit()

# Инициализация бота
bot = telebot.TeleBot('5891886347:AAEHei8Lge377MUAnQaFT0eiPDSxuxb2aUk')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Добавление пользователя в базу данных
    chat_id = message.chat.id
    cursor.execute('INSERT INTO users (chat_id, is_active) VALUES (?, 1)', (chat_id,))
    conn.commit()

    # Отправка сообщения приветствия
    bot.send_message(chat_id, 'Привет! Я бот для рассылки сообщений.')

# Обработчик команды /send_all
@bot.message_handler(commands=['send_all'])
def handle_send_all(message):
    # Проверка, что отправитель является администратором бота
    if message.from_user.id == 675884947:
        # Получение текста сообщения
        text = message.text.replace('/send_all ', '')

        # Получение списка активных пользователей
        users = get_active_users()

        # Рассылка сообщений
        for user in users:
            sent = bot.send_message(user, text)
            # Ожидание ответа от пользователя в течение 60 секунд
            bot.polling(none_stop=True)
            bot.skip_pending = True
            bot.message_handlers.unregister(handle_response)
            timer = threading.Timer(60, set_user_inactive, [user])
            timer.start()
            # Ожидание ответа от пользователя
            while True:
                time.sleep(1)
                if sent is not None and sent.chat.id == user:
                    break
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором бота.')

# Обработчик ответа от пользователя
@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.reply_to_message is not None)
def handle_response(message):
    # Пометка пользователя как неактивного, если он не ответил в течение 60 секунд
    set_user_inactive(message.chat.id)

bot.polling()
