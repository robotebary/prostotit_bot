from telebot import types


def message_1(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="BOT START", reply_markup=markup)


def message_2(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton(f"👋 выложить пост")
    button2 = types.KeyboardButton(f"❓ Количество постов")
    button3 = types.KeyboardButton(f"Создать пост")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)


def message_3(message, bot, n):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Время✅", callback_data=f'but1{n}')
    btn2 = types.InlineKeyboardButton("Период", callback_data=f'but2{n}')
    btn3 = types.InlineKeyboardButton("удаление", callback_data=f'but3{n}')
    btn6 = types.InlineKeyboardButton("Чат", callback_data=f'but6{n}')
    markup.add(btn1, btn2, btn3, btn6)
    settings = types.InlineKeyboardButton("Проверить настройки поста", callback_data=f'but5')
    markup.add(settings)
    back = types.InlineKeyboardButton("Вернуться в главное меню", callback_data=f'but4{n}')
    markup.add(back)

    bot.send_message(message.chat.id, "произвести настройку", reply_markup=markup)


def message_4(message, bot, n):
    markup = types.InlineKeyboardMarkup()
    button0 = types.InlineKeyboardButton("Когда выложить первый пост", callback_data=f'buton0{n}')
    markup.add(button0)
    button1 = types.InlineKeyboardButton("месяц", callback_data=f'buton1{n}')
    button2 = types.InlineKeyboardButton("неделя", callback_data=f'buton2{n}')
    button3 = types.InlineKeyboardButton("день", callback_data=f'buton3{n}')
    markup.add(button1, button2, button3)
    back = types.InlineKeyboardButton("Вернуться назад", callback_data=f'buton4{n}')
    markup.add(back)
    bot.send_message(message.chat.id, text="выберите что поменять", reply_markup=markup)


