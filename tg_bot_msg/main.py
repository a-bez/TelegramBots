import sqlite3
import requests


def send_mesage():
    TOKEN = "5891886347:AAEHei8Lge377MUAnQaFT0eiPDSxuxb2aUk"
    con = sqlite3.connect('tg_users.db')
    cur = con.execute('''SELECT name, user_id FROM users''')

    for el in cur:
        name = el[0]
        chat_id = el[1]
        message =f'Hello diar, {name}! Now I testing my new sender bot.'
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url).json()

    con.close()

send_mesage()

import schedule
import time

# определение времени выполнения задачи
# schedule.every().day.at("16:13").do(send_mesage)

# бесконечный цикл для запуска планировщика задач
# while True:
#     schedule.run_pending()
#     time.sleep(1)
