import telebot
import pandas as pd
import openpyxl
from openpyxl import load_workbook


bot = telebot.TeleBot('5579090888:AAGMUTxFCVRXm0UcVWnoy3UkePrImGasK4g')


def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id,'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age
    try:
             age = int(message.text)
             if age > 18:
                bot.send_message(message.from_user.id,
                              'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?')
             else:
                 bot.send_message(message.from_user.id, 'Ты пиздюк иди нахуй!')
                 bot.register_next_step_handler(message, get_age)

    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)





print("bot started")
bot.infinity_polling()
