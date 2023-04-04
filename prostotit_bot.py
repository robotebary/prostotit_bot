import datetime

import telebot
import openpyxl
import os
import schedule
import message_handler
import time

from dateutil.relativedelta import relativedelta

from tooken import token
from datetime import datetime, timedelta

from utils import wright_name, wright_time, wright_date, wright_month, wright_week, wright_days, ret_urn_day, \
    wright_last_days

bot = telebot.TeleBot(token())
n = 1
# Создание папки с фото
if not os.path.isdir("Photoo"):
    os.mkdir("Photoo")

os.chdir("Photoo")
ph = os.getcwd()
print(ph)


# команда старт
@bot.message_handler(commands=['start'])
def starts(message):
    message_handler.message_1(message, bot)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Вернуться в главное меню")
def menu(message):
    message_handler.message_2(message, bot)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Создать пост")
def hello_answer(message):
    bot.send_message(message.chat.id, text="Пришли фото в формате 'без сжатия'")


@bot.message_handler(content_types=['photo', 'document'])
def get_user_text(message):
    global n
    global ph
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_format_in = message.document.file_name.rfind('.')
    file_format = message.document.file_name[file_format_in:]
    print(downloaded_file)
    src = f"{ph}/" + message.document.file_id + file_format

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        n = wright_name(src, n)

    message_handler.message_3(message, bot, n)


#
# @bot.message_handler(commands=['photo'])
# def get_user_text(message):
#     src = "photo"
#     n = wright_name(src)
#     message_handler.message_3(message, bot, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("but1"))
def handle(call):
    n = call.data.replace('but1', '')
    bot.send_message(call.message.chat.id, 'введите время (12:00)'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup, n)


def setup(message, n):
    try:
        user_time = datetime.strptime(message.text, '%H:%M').time()
    except ValueError:
        bot.send_message(message.chat.id, "Введено некорректное время!")
        bot.register_next_step_handler(message, setup, n)
    else:
        bot.send_message(message.chat.id, f"установленное время {user_time.strftime('%H:%M')}")
        wright_time(user_time, n)
        message_handler.message_3(message, bot, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("but2"))
def handle(call):
    n = call.data.replace('but2', '')
    message_handler.message_4(call.message, bot, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buton0"))
def time_date(call):
    n = call.data.replace('buton0', '')
    bot.send_message(call.message.chat.id, 'введите дату (Д-М)'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup0, n)


def setup0(message, n):
    try:
        user_time = datetime.strptime(message.text, '%d-%m')
    except ValueError:
        bot.send_message(message.chat.id, "Введена некорректная дата!")
        bot.register_next_step_handler(message, setup0, n)
    else:
        current_year = datetime.now().year
        full_date = datetime(current_year, user_time.month, user_time.day).strftime("%d-%m-%Y")
        bot.send_message(message.chat.id, f"установленная дата {full_date}")
        date = ret_urn_day(n, 3)
        # mons
        # weeks
        # days
        if date is not None:
            # if moons is not None
            date_new = (datetime.strptime(ret_urn_day(n, 7), '%d-%m-%Y').date() - datetime.strptime(date, '%d-%m-%Y')
                        .date()).days
            full_date_post = (datetime.strptime(full_date, '%d-%m-%Y') + timedelta(days=date_new)).strftime('%d-%m-%Y')
            wright_last_days(full_date_post, n)
        full_date = datetime.strptime(full_date, '%d-%m-%Y').strftime('%d-%m-%Y')
        wright_date(full_date, n)
        message_handler.message_4(message, bot, n)


# def setup0(message, n):
#     try:
#         user_time = datetime.strptime(message.text, '%d-%m')
#     except ValueError:
#         bot.send_message(message.chat.id, "Введена некорректная дата!")
#         bot.register_next_step_handler(message, setup0, n)
#     else:
#         current_year = datetime.now().year
#         full_date = str(datetime(current_year, user_time.month, user_time.day).date().strftime("%d-%m-%Y"))
#         bot.send_message(message.chat.id, f"установленная дата {full_date}")
#         date = ret_urn_day(n, 3)
#         if date is not None:
#             date_old = datetime.strptime(date, '%d-%m-%Y').date()
#             date_post = datetime.strptime(ret_urn_day(n, 7), '%d-%m-%Y').date()
#             date_new = int(str((date_post - date_old).days))
#             full_date = datetime.strptime(full_date, '%d-%m-%Y')
#             full_date_post = full_date + timedelta(days=date_new)
#             full_date_post_str = full_date_post.strftime('%d-%m-%Y')
#             full_date_post = datetime.strptime(full_date_post_str, '%d-%m-%Y').date()
#             full_date_post = full_date_post.strftime('%d-%m-%Y')
#             wright_last_days(full_date_post, n)
#         full_date = datetime.strptime(str(full_date), '%Y-%m-%d').date()
#         full_date = full_date.strftime('%d-%m-%Y')
#         wright_date(full_date, n)
#         message_handler.message_4(message, bot, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buton1"))
def time_date_month(call):
    n = call.data.replace('buton1', '')
    bot.send_message(call.message.chat.id, 'введите количество месяцов'.format(str(call.data)))
    bot.answer_callback_query(call.id)

    bot.register_next_step_handler(call.message, setup1, n)


def setup1(message, n):
    if message.text.isnumeric():
        month = int(message.text)
        bot.send_message(message.chat.id, f"установленное количество месяцов {month}")
        wright_month(month, n)
        date = ret_urn_day(n, 3)
        if date is None:
            date_now = datetime.now()
            full_date = date_now.strftime('%d-%m-%Y')
            wright_date(full_date, n)
            date = full_date
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        result = date_obj + relativedelta(months=month)
        wright_last_days(result.strftime("%d-%m-%Y"), n)
    else:
        bot.send_message(message.chat.id, "Введите число!")
        bot.register_next_step_handler(message, setup1, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buton2"))
def time_date_week(call):
    n = call.data.replace('buton2', '')
    bot.send_message(call.message.chat.id, 'введите количество недель'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup2, n)


def setup2(message, n):
    if message.text.isnumeric():
        week = int(message.text)
        bot.send_message(message.chat.id, f"установленное количество недель {week}")
        wright_week(week, n)
        date = ret_urn_day(n, 3)
        if date is None:
            date_now = datetime.now()
            full_date = date_now.strftime('%d-%m-%Y')
            wright_date(full_date, n)
            date = full_date
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        result = date_obj + timedelta(weeks=week)
        wright_last_days(result.strftime("%d-%m-%Y"), n)
    else:
        bot.send_message(message.chat.id, "Введите число!")
        bot.register_next_step_handler(message, setup2, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buton3"))
def time_date_days(call):
    n = call.data.replace('buton3', '')
    bot.send_message(call.message.chat.id, 'введите количество дней'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup3, n)


def setup3(message, n):
    if message.text.isnumeric():
        days = int(message.text)
        bot.send_message(message.chat.id, f"установленное количество дней {days}")
        wright_days(days, n)
        date = ret_urn_day(n, 3)
        if date is None:
            date_now = datetime.now()
            full_date = date_now.strftime('%d-%m-%Y')
            wright_date(full_date, n)
            date = full_date
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        result = date_obj + timedelta(days=days)
        wright_last_days(result.strftime("%d-%m-%Y"), n)
    else:
        bot.send_message(message.chat.id, "Введите число!")
        bot.register_next_step_handler(message, setup3, n)


# Вернуться назад
@bot.callback_query_handler(func=lambda call: call.data.startswith("buton4"))
def handle(call):
    n = call.data.replace('buton4', '')
    message_handler.message_3(call.message, bot, n)


# Проверить настройки поста
@bot.callback_query_handler(func=lambda call: call.data.startswith("but5"))
def handle(call):
    n = call.data.replace('but5', '')
    settings(call.message, n)


def settings(message, n):
    times = ret_urn_day(n, 2)
    dwy = ret_urn_day(n, 3)
    dwys = ret_urn_day(n, 7)
    photo_import = ret_urn_day(n, 1)
    # замена обратных слешей
    photo_import = photo_import.replace("\\", "/")
    with open(photo_import, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=
        f"время отправки поста {times}\n"
        f"Дата отправки первого поста {dwy}\n"
        f"Дата отправки второго поста {dwys}\n")


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "👋 выложить пост")
def send_mes(message):
    channel_id = "-1001764282774"
    global n
    try:
        print(n)
    except NameError:
        print("Сначала загрузите фото")
        bot.send_message(message.chat.id, "Сначала загрузите фото")
    else:
        bot.send_message(message.chat.id, "Пост отправлен")
        send_message(channel_id, message_text="Zig hi")


def send_message(channel_id, message_text):
    global n
    print(n)
    # bot.send_message(channel_id, message_text)
    send_time = "14:04"
    send_date = "2023-04-03"
    photo_import = ret_urn_day(n, 1)
    # замена обратных слешей
    photo_import = photo_import.replace("\\", "/")
    with open(photo_import, 'rb') as photo:
        sent_message = bot.send_photo(channel_id, photo, caption=
        f"{message_text}")

        def delete_message():
            bot.delete_message(chat_id=channel_id, message_id=sent_message.message_id)

    schedule.every(3).minutes.do(delete_message)
    # schedule.every().day.at(send_time).do(send_message, channel_id, message_text)

    while True:
        schedule.run_pending()
        time.sleep(1)


# установка эксель файла если его нет в папке с ботом


def setup_xlsx():
    try:
        open('schedule.xlsx')
    except Exception:
        wb = openpyxl.Workbook()
        wb.save('schedule.xlsx')


setup_xlsx()

print("bot started")
bot.infinity_polling()

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# Проверка типа файла
# Инфа для фото
# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#     print(10)
#     # получаем информацию о фото
#     file_info = bot.get_file(message.photo[-1].file_id)
#     file_url = f"https://api.telegram.org/file/bot{token()}/" \
#                f"{file_info.file_path}"
#     response = requests.get(file_url)
#     img = Image.open(BytesIO(response.content))
#
#     # выводим информацию о фото
#     print(f"Image format: {img.format}")
#     print(f"Image size: {img.size}")
