import telebot
import pandas as pd
import openpyxl
from openpyxl import load_workbook


bot = telebot.TeleBot('5579090888:AAGMUTxFCVRXm0UcVWnoy3UkePrImGasK4g')

#установка эксель файла если его нет в папке с ботом
def setup_xlsx():
    try:
        open('schedule.xlsx')
    except Exception:
        wb = openpyxl.Workbook()
        wb.save('schedule.xlsx')
setup_xlsx()


@bot.message_handler(content_types=['photo', 'document'] )
def get_user_text(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:/Users/Александр/Desktop/Александр/боты/prostotit_bot/Photoo/' + message.document.file_id + ".png"
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)









# def get_name(message): #получаем фамилию
#     global name;
#     name = message.text;
#     bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
#     bot.register_next_step_handler(message, get_surname);
#
# def get_surname(message):
#     global surname;
#     surname = message.text;
#     bot.send_message(message.from_user.id,'Сколько тебе лет?');
#     bot.register_next_step_handler(message, get_age);
#
# def get_age(message):
#     global age
#     try:
#              age = int(message.text)
#              if age > 18:
#                 bot.send_message(message.from_user.id,
#                               'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?')
#              else:
#                  bot.send_message(message.from_user.id, 'Ты пиздюк иди нахуй!')
#                  bot.register_next_step_handler(message, get_age)
#
#     except Exception:
#         bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
#         bot.register_next_step_handler(message, get_age)
#




print("bot started")
bot.infinity_polling()
