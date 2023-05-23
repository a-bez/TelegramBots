import sqlite3
from telegram.ext import Updater, CommandHandler
from telegram import Bot

# Установите соединение с базой данных
conn = sqlite3.connect('telegram_stats.db')
cursor = conn.cursor()

# Создайте таблицу для хранения статистических данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subscribers INTEGER,
        active_members INTEGER
    )
''')
conn.commit()



# Функция обработки команды /stats
def get_stats(update, context):
    # Получение информации о боте
    bot = Bot(token=context.bot.token)
    bot_info = bot.get_me()

    # Получение количества подписчиков и активных участников
    subscribers = bot_info['num_subscribers']
    active_members = bot.get_chat_members_count(update.effective_chat.id)

    # Вставка статистических данных в базу данных
    cursor.execute('''
        INSERT INTO stats (subscribers, active_members)
        VALUES (?, ?)
    ''', (subscribers, active_members))
    conn.commit()

    # Отправка ответного сообщения
    message = f"Количество подписчиков: {subscribers} Количество активных участников: {active_members}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Создание объекта Updater и добавление обработчика команды
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('stats', get_stats))

# Запуск бота
updater.start_polling()
