import telebot
import pandas as pd
import openpyxl


bot = telebot.TeleBot('5579090888:AAGMUTxFCVRXm0UcVWnoy3UkePrImGasK4g')

#установка эксель файла если его нет в папке с ботом
def setup_xlsx():
    try:
        open('schedule.xlsx')
    except Exception:
        wb = openpyxl.Workbook()
        wb.save('schedule.xlsx')
setup_xlsx()


@bot.message_handler(content_types=['photo', 'document'])
def get_user_text(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info)
    file_format_in = message.document.file_name.rfind('.')
    file_format = message.document.file_name[file_format_in:]

    src = 'C:/Users/Александр/Desktop/Александр/боты/prostotit_bot/Photoo/' + message.document.file_id + file_format
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        wright_name(src)


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
