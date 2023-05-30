from twilio.rest import Client
import sqlite3

class TwilioManager:
    def __init__(self, account_sid, auth_token, db_file):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.db_file = db_file

    def rent_phone_number(self):
        client = Client(self.account_sid, self.auth_token)

        # Замените 'your_twilio_phone_number' на ваш номер телефона Twilio
        number = client.available_phone_numbers('US').fetch()

        # Аренда номера телефона
        rented_number = client.incoming_phone_numbers.create(
            phone_number=number.phone_number
        )

        # Сохранение номера в базу данных
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rented_numbers (phone_number) VALUES (?)", (rented_number.phone_number,))
        conn.commit()
        conn.close()

        return rented_number.phone_number

    def get_sms_text(self, phone_number):
        client = Client(self.account_sid, self.auth_token)

        # Получение сообщений с помощью фильтра по отправителю
        messages = client.messages.list(from_=phone_number)

        if messages:
            latest_message = messages[0]
            sms_text = latest_message.body

            # Сохранение текста сообщения в базу данных
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sms_messages (message_text) VALUES (?)", (sms_text,))
            conn.commit()
            conn.close()

            return sms_text
        else:
            return None
