# -!- coding: utf-8 -!-
import telebot
from telebot import types

import config
from lang import ru
from paginators import paginator
from user_utils import get_users_by_role

# telegram bot api
bot = telebot.TeleBot(config.token)


def users_menu(message=None, c=None, role='manager', page=1):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    users = get_users_by_role(role=role)
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        if users:
            if role == 'manager':
                mes_text = ru.get('managers_mnu_text').format(
                    count=len(users)
                )
            else:
                mes_text = ru.get('agents_mnu_text').format(
                    count=len(users)
                )
            userspage = paginator(users, page)
            for user in userspage:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=user.get('name'),
                        callback_data='userprofile=' + str(user.get('id'))
                    )
                )
            if len(users) <= config.pagelimit:
                pass
            else:
                chek_next_btn = len(paginator(users, page + 1))
                if chek_next_btn > 0:
                    if page == 1:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('next'),
                                callback_data='users!' + str(page + 1) + '!' + role
                            )
                        )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('back'),
                                callback_data='users!' + str(page - 1) + '!' + role
                            ),
                            types.InlineKeyboardButton(
                                text=ru.get('next'),
                                callback_data='users!' + str(page + 1) + '!' + role
                            )
                        )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back'),
                            callback_data='users!' + str(page - 1) + '!' + role
                        )
                    )
        else:
            if role == 'manager':
                mes_text = ru.get('no_managers_mnu_text')
            else:
                mes_text = ru.get('no_agents_mnu_text')
        if role == 'manager':
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('add_manager_mnu_btn'),
                    callback_data='createmanager'
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('add_agent_mnu_btn'),
                    callback_data='createagent'
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('to_menu_btn'),
                callback_data='usersmenu'
            )
        )
    else:
        mes_text = ru.get('access_close')
        # надо добавить кнопку назад
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def choose_role_users_menu(message=None, c=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    users = get_users_by_role(role='all')
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        mes_text = ru.get('choose_users_menu_text').format(
            count=len(users)
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('managers_mnu_btn'),
                callback_data='users!1!manager'
            ),
            types.InlineKeyboardButton(
                text=ru.get('agents_mnu_btn'),
                callback_data='users!1!agent'
            )
        )
    else:
        mes_text = ru.get('access_close')
        # добавить кнопку назад
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
