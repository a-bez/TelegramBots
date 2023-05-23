import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Установка соединения с базой данных
conn = sqlite3.connect('telegram_stats.db')
cursor = conn.cursor()

# Создание таблицы для хранения статистических данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        chat_id INTEGER,
        feedback_text TEXT
    )
''')
conn.commit()

# Функция обработки входящих сообщений
def handle_message(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    text = update.message.text

    # Сохранение обратной связи и отзыва пользователя в базе данных
    cursor.execute('''
        INSERT INTO feedback_reviews (user_id, chat_id, feedback_text)
        VALUES (?, ?, ?)
    ''', (user_id, chat_id, text))
    conn.commit()

# Функция обработки команды /reviews
def get_reviews(update, context):
    chat_id = update.message.chat_id

    # Получение всех обратных связей и отзывов пользователя
    cursor.execute('''
        SELECT feedback_text
        FROM feedback_reviews
        WHERE chat_id = ?
    ''', (chat_id,))
    results = cursor.fetchall()

    # Формирование сообщения с обратной связью и отзывами пользователей
    message = "Обратная связь и отзывы пользователей:\n\n"
    for result in results:
        message += f"- {result[0]}\n"
    context.bot.send_message(chat_id=chat_id, text=message)

# Создание объекта Updater и добавление обработчиков
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CommandHandler('reviews', get_reviews))

# Запуск бота
updater.start_polling()
