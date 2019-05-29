# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config
from lang import ru
from bot_utilites import get_users


bot = telebot.TeleBot(config.token)


def appdate():
    txt = 'Мы обновили бота, теперь в вашем меню есть три основных раздела:\n1. Опросы - там вы можете найти активные опросы, на которые вы ещё не ответили\n2. Обсуждения - там вы можете обсуждать актуальные темы\n3. Профиль - там вы можете просмотреть и изменить информацию о вашей учетной записи' 
    users = get_users()
    for user in users:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton(ru.get('polls_user_menu_btn')),
            types.KeyboardButton(ru.get('chats_user_menu_btn')))
        keyboard.add(
            types.KeyboardButton(ru.get('settings')))
        print(user[0])
        bot.send_message(
            user[0],
            txt,
            parse_mode='html',
            reply_markup=keyboard)


appdate()
