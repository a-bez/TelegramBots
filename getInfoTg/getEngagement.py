import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Установка соединения с базой данных
conn = sqlite3.connect('telegram_stats.db')
cursor = conn.cursor()

# Создание таблицы для хранения статистических данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS engagement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_id INTEGER,
        chat_id INTEGER,
        engagement_level INTEGER
    )
''')
conn.commit()

# Функция обработки входящих сообщений
def handle_message(update, context):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    text = update.message.text

    # Вычисление уровня вовлеченности (в данном примере просто длина сообщения)
    engagement_level = len(text)

    # Сохранение статистических данных в базе данных
    cursor.execute('''
        INSERT INTO engagement (user_id, message_id, chat_id, engagement_level)
        VALUES (?, ?, ?, ?)
    ''', (user_id, message_id, chat_id, engagement_level))
    conn.commit()

# Функция обработки команды /stats
def get_stats(update, context):
    chat_id = update.message.chat_id

    # Получение статистических данных по уровню вовлеченности
    cursor.execute('''
        SELECT AVG(engagement_level)
        FROM engagement
        WHERE chat_id = ?
    ''', (chat_id,))
    result = cursor.fetchone()
    avg_engagement = result[0] if result else 0

    # Отправка ответного сообщения
    message = f"Средний уровень вовлеченности: {avg_engagement}"
    context.bot.send_message(chat_id=chat_id, text=message)

# Создание объекта Updater и добавление обработчиков
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CommandHandler('stats', get_stats))

# Запуск бота
updater.start_polling()
