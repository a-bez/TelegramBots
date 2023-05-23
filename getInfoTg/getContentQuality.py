import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Установка соединения с базой данных
conn = sqlite3.connect('telegram_stats.db')
cursor = conn.cursor()

# Создание таблицы для хранения статистических данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS content_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        chat_id INTEGER,
        content_quality INTEGER
    )
''')
conn.commit()

# Функция обработки входящих сообщений
def handle_message(update, context):
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    text = update.message.text

    # Вычисление оценки качества контента (в данном примере просто длина сообщения)
    content_quality = len(text)

    # Сохранение статистических данных в базе данных
    cursor.execute('''
        INSERT INTO content_quality (message_id, chat_id, content_quality)
        VALUES (?, ?, ?)
    ''', (message_id, chat_id, content_quality))
    conn.commit()

# Функция обработки команды /stats
def get_stats(update, context):
    chat_id = update.message.chat_id

    # Получение статистических данных по качеству контента
    cursor.execute('''
        SELECT AVG(content_quality)
        FROM content_quality
        WHERE chat_id = ?
    ''', (chat_id,))
    result = cursor.fetchone()
    avg_content_quality = result[0] if result else 0

    # Отправка ответного сообщения
    message = f"Среднее качество контента: {avg_content_quality}"
    context.bot.send_message(chat_id=chat_id, text=message)

# Создание объекта Updater и добавление обработчиков
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CommandHandler('stats', get_stats))

# Запуск бота
updater.start_polling()
