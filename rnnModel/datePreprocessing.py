import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import telebot

# Создание экземпляра Telegram Bot API
bot_token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(bot_token)

# Загрузка данных из телеграм-канала
channel_username = 'CHANNEL_USERNAME'
message_count = 1000  # Количество сообщений для загрузки
messages = bot.get_chat_history(channel_username, limit=message_count)

# Сбор статистики сообщений по дате
dates = []
for message in messages:
    date = datetime.fromtimestamp(message.date)
    dates.append(date)

# Создание DataFrame с данными
data = pd.DataFrame({'Date': dates})

# Группировка по дате и подсчет количества сообщений
data = data.groupby('Date').size().reset_index(name='MessageCount')

# Преобразование даты в индекс
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Ресемплирование данных по дням
daily_data = data.resample('D').sum()

# Визуализация статистики
plt.figure(figsize=(12, 6))
plt.plot(daily_data.index, daily_data['MessageCount'])
plt.xlabel('Date')
plt.ylabel('Message Count')
plt.title('Telegram Channel Message Count')
plt.grid(True)
plt.show()

# Выполнение статистического анализа
mean = daily_data['MessageCount'].mean()
median = daily_data['MessageCount'].median()
std = daily_data['MessageCount'].std()
