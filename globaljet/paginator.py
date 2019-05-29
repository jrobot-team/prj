# -*- coding: utf-8 -*-
import telebot
from telebot import types

from config import PAGELIMIT, TOKEN
from lng_fn import lng

bot = telebot.TeleBot(TOKEN)


def paginator(array, page, limit=PAGELIMIT):
    """
    Принимает массив и страницу
    возвращает массив страницу обрезанную на лимит отображения
    (данная настройка или передается напрямую в функцию
    или берется из конфига)
    """
    if array:
        try:
            if page == 1:
                array = array[:limit]
            else:
                start = limit * (int(page) - 1)
                stop = limit + start
                array = array[start:stop]
        except Exception as e:
            print(e)
            print('paginator error')
            array = []
    else:
        array = []
    return array


def page_menu(
        array,
        page,
        mes_text,
        c_data,
        back_c_data,
        c=False,
        message=False):
    """
    Принимает массив (array) состоящий из списков [0-текст, 1-ID],
    страницу (page), текст сообщения (mes_text),
    коллбек на меню (c_dat), коллбек в вышестоящее меню (back_c_data)
    """
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    slice_page = paginator(array, page)
    keyboard = types.InlineKeyboardMarkup()
    for btn in slice_page:
        keyboard.add(
            types.InlineKeyboardButton(
                text=btn[0],
                callback_data=c_data + str(btn[1])))
    if len(slice_page) <= PAGELIMIT:
        pass
    else:
        chek_next_btn = len(paginator(array, page + 1))
        if chek_next_btn > 0:
            if page == 1:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('next'),
                        callback_data=c_data + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back'),
                        callback_data=c_data + str(page - 1)),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('next'),
                        callback_data=c_data + str(page + 1)))
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data=c_data + str(page - 1)))
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back'),
            callback_data=back_c_data))
    if c:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
