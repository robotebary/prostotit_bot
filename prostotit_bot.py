import telebot
from telebot import types
import pandas as pd
import openpyxl

bot = telebot.TeleBot('5579090888:AAGMUTxFCVRXm0UcVWnoy3UkePrImGasK4g')


# @bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
#                                     'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
#                                     'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
#                                     'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
#                                     'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
# def mes_inf(message):
#     bot.send_message(message.chat.id, message)

# установка эксель файла если его нет в папке с ботом
def setup_xlsx():
    try:
        open('schedule.xlsx')
    except Exception:
        wb = openpyxl.Workbook()
        wb.save('schedule.xlsx')


setup_xlsx()


@bot.message_handler(commands=['start'])
def starts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="BOT START", reply_markup=markup)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == "👋 Поздороваться")
def hello_answer(message):
    bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == "❓ Задать вопрос")
def question_answer(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Как меня зовут?")
    btn2 = types.KeyboardButton("Что я могу?")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, back)
    bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Как меня зовут?":
        bot.send_message(message.chat.id, "У меня нет имени..")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


@bot.message_handler(content_types=['photo', 'document'])
def get_user_text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Время")
    btn2 = types.KeyboardButton("Период")
    back = types.KeyboardButton("удаление")
    markup.add(btn1, btn2, back)

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info)
    file_format_in = message.document.file_name.rfind('.')
    file_format = message.document.file_name[file_format_in:]

    src = 'C:/Users/Александр/Desktop/Александр/боты/prostotit_bot/Photoo/' + message.document.file_id + file_format
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        wright_name(src)

    bot.send_message(message.chat.id, "произвести настройку", reply_markup=markup)


def wright_name(src):
    n = 1
    a = openpyxl.load_workbook('schedule.xlsx')
    ws = a.active
    while ws[f'A{n}'].value != None:
        n += 1
    ws[f'A{n}'] = src
    print(ws[f'A{n}'].value)
    a.save('schedule.xlsx')


print("bot started")
bot.infinity_polling()
