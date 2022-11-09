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



print("bot started")
bot.infinity_polling()
