import datetime
import telebot
import openpyxl
import os

from tooken import token

import message_handler
from utils import wright_name, wright_time, wright_date

bot = telebot.TeleBot(token())

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
    bot.send_message(message.chat.id, text="Пришли фото")


@bot.message_handler(content_types=['photo', 'document'])
def get_user_text(message):
    global ph
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_format_in = message.document.file_name.rfind('.')
    file_format = message.document.file_name[file_format_in:]

    src = f"{ph}/" + message.document.file_id + file_format

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        n = wright_name(src)

    message_handler.message_3(message, bot, n)


@bot.callback_query_handler(func=lambda call: call.data.startswith("but1"))
def handle(call):
    n = call.data.replace('but1', '')
    bot.send_message(call.message.chat.id, 'введите время (12:00)'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup, n)


def setup(message, n):
    try:
        user_time = datetime.datetime.strptime(message.text, '%H:%M').time()
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
    bot.send_message(call.message.chat.id, 'введите дату ( М:Д)'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup1, n)


def setup1(message, n):
    try:
        user_time = datetime.datetime.strptime(message.text, '%m-%d')
    except ValueError:
        bot.send_message(message.chat.id, "Введена некорректная дата!")
        bot.register_next_step_handler(message, setup1, n)
    else:
        current_year = datetime.datetime.now().year
        full_date = datetime.datetime(current_year, user_time.month, user_time.day).date().strftime("%Y-%m-%d")
        bot.send_message(message.chat.id, f"установленная дата {full_date}")
        wright_date(full_date, n)
        message_handler.message_4(message, bot, n)


# Проверка типа файла
# @bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
#                                     'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
#                                     'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
#                                     'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
#                                     'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
# def mes_inf(message):
#     bot.send_message(message.chat.id, message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("buton4"))
def handle(call):
    n = call.data.replace('buton4', '')
    message_handler.message_3(call.message, bot, n)
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
