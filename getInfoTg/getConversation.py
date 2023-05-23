import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Установка соединения с базой данных
conn = sqlite3.connect('telegram_stats.db')
cursor = conn.cursor()

# Создание таблицы для хранения статистических данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals_achievement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        chat_id INTEGER,
        goal_achieved INTEGER,
        goal_total INTEGER
    )
''')
conn.commit()

# Функция обработки входящих сообщений
def handle_message(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    text = update.message.text

    # Проверка достижения цели (в данном примере просто проверка наличия ключевого слова)
    goal_achieved = 1 if 'keyword' in text else 0

    # Сохранение статистических данных в базе данных
    cursor.execute('''
        INSERT INTO goals_achievement (user_id, chat_id, goal_achieved, goal_total)
        VALUES (?, ?, ?, ?)
    ''', (user_id, chat_id, goal_achieved, 1))
    conn.commit()

# Функция обработки команды /stats
def get_stats(update, context):
    chat_id = update.message.chat_id

    # Получение статистических данных по достижению целей
    cursor.execute('''
        SELECT SUM(goal_achieved), SUM(goal_total)
        FROM goals_achievement
        WHERE chat_id = ?
    ''', (chat_id,))
    result = cursor.fetchone()
    goal_achieved, goal_total = result if result else (0, 0)

    # Расчет конверсии и отправка ответного сообщения
    conversion_rate = (goal_achieved / goal_total) * 100 if goal_total > 0 else 0
    message = f"Конверсия: {conversion_rate}%"
    context.bot.send_message(chat_id=chat_id, text=message)

# Создание объекта Updater и добавление обработчиков
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CommandHandler('stats', get_stats))

# Запуск бота
updater.start_polling()
