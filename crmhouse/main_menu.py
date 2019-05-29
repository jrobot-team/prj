# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from agent_menu import agent_main_menu
from agent_utils import get_agent_consumers
from boss_utils import admininfo
from boss_menu import boss_main_menu
from consumers_menu import clients_menu, consumers_menu
from consumers_utils import get_consumers_by_role
from lang import ru
from user_utils import get_user_info
from users_menu import choose_role_users_menu

# telegram bot api
bot = telebot.TeleBot(config.token)


def startmenu(message):
    user_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if admininfo(user_id):
        boss_main_menu(message=message)
    elif get_user_info(user_id).get('role') == 'admin':
        boss_main_menu(message=message)
    else:
        userinfo = get_user_info(user_id)
        if userinfo:
            if userinfo.get('role') == 'manager':
                mes_text = ru.get('hiagent').format(
                    username=userinfo.get('name'),
                    buyers_count=len(get_consumers_by_role('buyer')),  # база покупателей
                    sellers_count=len(get_consumers_by_role('seller')),  # база продавцов
                )
                keyboard.add(
                    types.KeyboardButton(
                        ru.get('sellers_mnu_btn')
                    ),
                    types.KeyboardButton(
                        ru.get('buyers_mnu_btn')
                    )
                )
            if userinfo.get('role') == 'agent':
                mes_text = ru.get('agent_main_menu_text').format(
                    name=userinfo.get('name'),
                    tasks_count=0,
                    buyers_count=len(get_agent_consumers(user_id, role='buyer')),
                    sellers_count=len(get_agent_consumers(user_id, role='seller'))
                )
                keyboard.add(
                    types.KeyboardButton(
                        ru.get('sellers_mnu_btn')
                    ),
                    types.KeyboardButton(
                        ru.get('buyers_mnu_btn')
                    )
                )
                keyboard.add(
                    types.KeyboardButton(
                        ru.get('tasks_mnu_btn')
                    )
                )
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            mes_text = ru.get('access_close')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('reg_btn'),
                    callback_data='регистрация'
                )
            )
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        if userinfo:
            if userinfo.get('role') == 'manager':
                keyboard = types.InlineKeyboardMarkup()
                mes_text = ru.get('hiagent_footer')
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('add_seller_mnu_btn'),
                        callback_data='add_consumer%seller'
                    ),
                    types.InlineKeyboardButton(
                        text=ru.get('add_buyer_mnu_btn'),
                        callback_data='add_consumer%buyer'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('sellers_mnu_btn'),
                        callback_data='клиенты*1*seller'
                    ),
                    types.InlineKeyboardButton(
                        text=ru.get('buyers_mnu_btn'),
                        callback_data='клиенты*1*buyer'
                    )
                )
                bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
            if userinfo.get('role') == 'agent':
                keyboard = types.InlineKeyboardMarkup()
                mes_text = ru.get('hiagent_footer')
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('sellers_mnu_btn'),
                        callback_data='agentmenu*seller'
                    ),
                    types.InlineKeyboardButton(
                        text=ru.get('buyers_mnu_btn'),
                        callback_data='agentmenu*buyer'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('tasks_mnu_btn'),
                        callback_data='tasks'
                    )
                )
                bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)


def keymenu(message):
    user_id = message.from_user.id
    if message.text == '/start':
        startmenu(message)
    if user_id in config.admin:
        if message.text == ru.get('sellers_mnu_btn'):
            consumers_menu(message=message, status=1)
        if message.text == ru.get('buyers_mnu_btn'):
            consumers_menu(message=message, status=0)
        if message.text == ru.get('users_mnu_btn'):
            choose_role_users_menu(message=message)
    else:
        userinfo = get_user_info(user_id)
        if userinfo:
            if userinfo.get('role') == 'manager':
                if message.text == ru.get('sellers_mnu_btn'):
                    clients_menu('seller', message=message)
                if message.text == ru.get('buyers_mnu_btn'):
                    clients_menu('buyer', message=message)
            if userinfo.get('role') == 'agent':
                if message.text == ru.get('sellers_mnu_btn'):
                    agent_main_menu('seller', message=message)
                if message.text == ru.get('buyers_mnu_btn'):
                    agent_main_menu('buyer', message=message)
                if message.text == ru.get('tasks_mnu_btn'):
                    pass
        else:
            pass
