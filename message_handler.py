from telebot import types


def message_1(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="BOT START", reply_markup=markup)


def message_2(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("👋 Поздороваться")
    button2 = types.KeyboardButton("❓ Задать вопрос")
    button3 = types.KeyboardButton("Создать пост")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
