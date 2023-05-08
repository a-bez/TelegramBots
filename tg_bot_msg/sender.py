import telebot
import sqlite3

bot = telebot.TeleBot('5891886347:AAEHei8Lge377MUAnQaFT0eiPDSxuxb2aUk')

@bot.message_handler(commanrds=['start'])
def star(message):
    print(message.chat.id)

@bot.message_handler(commands=['send'])
def send(message):
    con = sqlite3.connect('tg_users.db')
    cur = con.execute('''SELECT user_id FROM users''')
    if message.chat.id == 675884947:
        for i in cur:
            # chat_id = i[1]
            # bot.send_message(message=chat_id, text='Какой-то текст')
            print(i)

bot.polling()