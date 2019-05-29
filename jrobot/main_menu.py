# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from forum_menu import forum_menu
from lng_fn import lng
from poll_menu import polls_menu
from tasks_menu import user_tasks_menu
from tester_menu import tester_menu, user_tester_menu
from user_menu import start_user_menu, user_group_menu, users_view
from users_utils import (get_group_info_by_id, get_user_info, get_user_status,
                         is_user_in_group, isuser, reg_user,
                         user_on_group_chek, username_getter)

# telegram bot api
bot = telebot.TeleBot(config.token)


def startmenu(message):
    user_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in config.admin:
        mes_text = lng(user_id).get('hiadmin')
        keyboard.add(
            types.KeyboardButton(
                lng(user_id).get('learn_mnu_btn')
            ),
            types.KeyboardButton(
                lng(user_id).get('tasks_mnu_btn')
            )
        )
        keyboard.add(
            types.KeyboardButton(
                lng(user_id).get('users_mnu_btn')
            )
        )
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        try:
            refer_id = int(message.text.split('/start ')[1])
        except:
            refer_id = None
        start_user_menu(message=message, refer_id=refer_id)


def keymenu(message, cncl=False):
    user_id = message.from_user.id
    if message.text == '/start':
        startmenu(message)
    if user_id in config.admin:
        if message.text == lng(user_id).get('learn_mnu_btn'):
            tester_menu(message=message)
        if message.text == lng(user_id).get('tasks_mnu_btn'):
            pass
        if message.text == lng(user_id).get('users_mnu_btn'):
            users_view(message=message)
    else:
        if isuser(user_id):
            if cncl:
                start_user_menu(message=message)
            else:
                if get_user_status(user_id):
                    if message.text == lng(user_id).get('learn_mnu_btn'):
                        user_tester_menu(message=message)
                    if message.text == lng(user_id).get('tasks_mnu_btn'):
                        if user_on_group_chek(user_id):
                            user_tasks_menu(message=message)
                        else:
                            mes_text = lng(user_id).get('nogroup_user')
                            bot.send_message(
                                message.chat.id,
                                text=mes_text,
                                parse_mode='html')
                    if message.text == lng(user_id).get('polls_mnu_btn'):
                        if user_on_group_chek(user_id):
                            polls_menu(message=message)
                        else:
                            mes_text = lng(user_id).get('nogroup_user')
                            bot.send_message(
                                message.chat.id,
                                text=mes_text,
                                parse_mode='html')
                    if message.text == lng(user_id).get('meet_mnu_btn'):
                        if user_on_group_chek(user_id):
                            forum_menu(message=message)
                        else:
                            mes_text = lng(user_id).get('nogroup_user')
                            bot.send_message(
                                message.chat.id,
                                text=mes_text,
                                parse_mode='html')
                    if message.text == lng(user_id).get('user_group_mnu_btn'):
                        user_group_menu(message=message)
                else:
                    group_id = is_user_in_group(user_id)
                    refer_id = get_group_info_by_id(group_id).get('owner_id')
                    group_name = get_group_info_by_id(group_id).get('name')
                    refer = get_user_info(refer_id)
                    mes_text = lng(user_id).get('hireferaluser_message_text_no_aprowed_acc').format(
                        refer_username=refer.get('name'),
                        group_name=group_name
                    )
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('get_learn_mnu_btn'),
                            callback_data='обучение'
                        )
                    )
                    bot.send_message(
                        message.chat.id,
                        text=mes_text,
                        parse_mode='html',
                        reply_markup=keyboard)
        else:
            try:
                refer_id = int(message.text.split('/start ')[1])
            except:
                refer_id = None
            username = username_getter(message=message)
            reg_user(user_id, username, refer_id=refer_id)
            start_user_menu(message=message)
