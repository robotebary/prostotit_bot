import datetime

import telebot
import openpyxl
import os
from telebot import types

import message_handler

bot = telebot.TeleBot('5579090888:AAGMUTxFCVRXm0UcVWnoy3UkePrImGasK4g')

# Создание папки с фото
if not os.path.isdir("Photoo"):
    os.mkdir("Photoo")

os.chdir("Photoo")
ph = os.getcwd()
print(ph)


@bot.message_handler(commands=['start'])
def starts(message):
    message_handler.message_1(message, bot)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "Вернуться в главное меню")
def func(message):
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

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Время", callback_data=f'but1{n}')
    btn2 = types.InlineKeyboardButton("Период", callback_data='but2')
    btn3 = types.InlineKeyboardButton("удаление", callback_data='but3')
    back = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='but4')
    markup.add(btn1, btn2, btn3, back)

    bot.send_message(message.chat.id, "произвести настройку", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("but1"))
def handle(call):
    n = call.data.replace('but1', '')
    bot.send_message(call.message.chat.id, 'введите время ( 11:44)'.format(str(call.data)))
    bot.answer_callback_query(call.id)
    bot.register_next_step_handler(call.message, setup, n)


def setup(message, n):
    try:
        user_time = datetime.datetime.strptime(message.text, '%H:%M').time()
    except ValueError:
        print("Введено некорректное время!")
    else:
        print("Введенное время: ", user_time)
    bot.send_message(message.chat.id, f"установленное время {user_time}")
    wright_date(user_time, n)
# if message.text == "Период":
    #     bot.send_message(message.chat.id, text="Поздороваться с читателями")
    #
    # elif message.text == "удаление":
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     button1 = types.KeyboardButton("👋 Поздороваться")
    #     button2 = types.KeyboardButton("❓ Задать вопрос")
    #     markup.add(button1, button2)
    #     bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    # elif message.text == "Вернуться в главное меню":
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     button1 = types.KeyboardButton("👋 Поздороваться")
    #     button2 = types.KeyboardButton("❓ Задать вопрос")
    #     markup.add(button1, button2)
    #     bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    # # доделать удаление названия еслы выходишь в главное меню без настройка(а лучше применить стандпртные настройки)
    # else:
    #     bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал!!!..")


def wright_name(src):
    n = 1
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    while ws[f'A{n}'].value is not None:
        n += 1
    ws[f'A{n}'] = src
    print(ws[f'A{n}'].value)
    a.save('schedule.xlsx')
    return n


def wright_date(src, n):
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    ws[f'B{n}'] = src
    print(ws[f'B{n}'].value)
    a.save('schedule.xlsx')
    return n

# Проверка типа файла

# @bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
#                                     'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
#                                     'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
#                                     'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
#                                     'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
# def mes_inf(message):
#     bot.send_message(message.chat.id, message)


# установка эксель файла если его нет в папке с ботом
#
def setup_xlsx():
    try:
        open('schedule.xlsx')
    except Exception:
        wb = openpyxl.Workbook()
        wb.save('schedule.xlsx')


setup_xlsx()







print("bot started")
bot.infinity_polling()
