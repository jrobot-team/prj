# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utilites import (chek_cat_accessing, chek_user_polled,
                          chek_user_seen_cat, chk_admin, get_chat_cats,
                          get_chats, get_closed_polls, get_group_info,
                          get_open_polls, reg_user, unset_chats, user_counts,
                          user_info)
from lang import ru
from mnu import su_admin_mnu

# telegram bot api
bot = telebot.TeleBot(config.token)


def startmenu(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    active_polls = len(get_open_polls())
    closed_polls = len(get_closed_polls())
    users_counts = user_counts()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in config.admin or chk_admin(user_id):
        mes_text = ru.get('hiadmin').format(
            active_polls=active_polls,
            closed_polls=closed_polls,
            users_counts=users_counts)
        keyboard.add(
            types.KeyboardButton(ru.get('users_menu_btn')),
            types.KeyboardButton(ru.get('polls')))
        keyboard.add(
            types.KeyboardButton(ru.get('chats_btn'))
        )
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        user = user_info(user_id)
        mes_text = ru.get('hi_user')
        if user:
            if user[8]:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(
                    types.KeyboardButton(ru.get('polls_user_menu_btn')),
                    types.KeyboardButton(ru.get('chats_user_menu_btn')))
                keyboard.add(
                    types.KeyboardButton(ru.get('settings')))
                bot.send_message(
                    message.chat.id,
                    text='DNT Obrabpros',
                    parse_mode='html',
                    reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('register'),
                        callback_data='register'))
                mes_text = ru.get('reg_message').format(
                    name=username)
        else:
            reg_user(user_id, username)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('register'),
                    callback_data='register'))
            mes_text = ru.get('reg_message').format(
                name=username)
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def m_admin(message):
    user_id = message.from_user.id
    if user_id in config.admin or chk_admin(user_id):
        su_admin_mnu(message=message)
    else:
        mes_text = ru.get('error')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')


def m_polls(message=False, c=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    if user_id in config.admin or chk_admin(user_id):
        mes_text = ru.get('admin_menu_polls')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('make_poll'),
                callback_data='makepollname'),
            types.InlineKeyboardButton(
                text=ru.get('draft_polls'),
                callback_data='draftpolls+1'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('active_polls'),
                callback_data='activepolls'),
            types.InlineKeyboardButton(
                text=ru.get('arch'),
                callback_data='pollarch<1'))
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
    else:
        mes_text = ru.get('error')
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


def m_user_settings(message=False, c=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    if user_id in config.admin or chk_admin(user_id):
        keymenu(message)
    else:
        mes_text = ru.get('usersettings_menu')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('change_fio'),
                callback_data='change_fio_by_user'),
            types.InlineKeyboardButton(
                text=ru.get('change_pwd'),
                callback_data='change_pwd_by_user'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('info_btn'),
                callback_data='информация'
            )
        )
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


def m_user_info(message=False, c=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    user = user_info(user_id)
    fio = user[1]
    role = user[2]
    if user[5]:
        interviewed = ru.get('sm_yes')
    else:
        interviewed = ru.get('sm_no')
    groupid = user[7]
    if groupid:
        groupname = get_group_info(groupid)[2]
    else:
        groupname = ru.get('user_nogroup')
    if user[6]:
        pwd = ru.get('userpwd_on')
    else:
        pwd = ru.get('userpwd_off')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('to_settings'),
            callback_data='настройки'
        )
    )
    mes_text = ru.get('himessage').format(
        user_id=user_id,
        fio=fio,
        pwd=pwd,
        groupname=groupname,
        role=ru.get(role),
        interviewed=interviewed)
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


def chats_menu(message=False, c=False):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('new_chat'),
            callback_data='новое_обсуждение'
        ),
        types.InlineKeyboardButton(
            text=ru.get('active_chat'),
            callback_data='активные_обсуждения'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('category_btn'),
            callback_data='категории_обсуждений'
        ),
        types.InlineKeyboardButton(
            text=ru.get('arch_chat'),
            callback_data='архивные_обсуждения'
        )
    )
    mes_text = ru.get('chat_menu_text').format(
        active_chats=len(get_chats(status='active')),
        arch_chats=len(get_chats(status='arch'))
    )
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


def m_user_polls(message):
    user_id = message.from_user.id
    open_polls = get_open_polls()
    noactive_polls_for_user = False
    chek = True
    if user_info(user_id)[4]:
        if len(open_polls) > 0:
            for poll in open_polls:
                if chek_user_polled(user_id, poll[0]):
                    noactive_polls_for_user = True
                else:
                    mes_text = ru.get('active_poll_short_text').format(
                        poll_name=poll[1],
                        pub_date=poll[5]
                    )
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('user_open_poll_btn'),
                            callback_data='опрос-' + str(poll[0])
                        )
                    )
                    bot.send_message(
                        message.chat.id,
                        mes_text,
                        parse_mode='html',
                        reply_markup=keyboard)
                    chek = False
        else:
            mes_text = ru.get('no_active_polls')
            bot.send_message(
                message.chat.id,
                mes_text,
                parse_mode='html')
        if noactive_polls_for_user and chek:
            mes_text = ru.get('no_active_polls')
            bot.send_message(
                message.chat.id,
                mes_text,
                parse_mode='html')
    else:
        mes_text = ru.get('no_active_polls')
        bot.send_message(
            message.chat.id,
            mes_text,
            parse_mode='html')


def m_user_chats(message=False, c=False):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    cats = get_chat_cats()
    if user_info(user_id)[4]:
        if cats:
            keyboard = types.InlineKeyboardMarkup()
            mes_text = ru.get('user_view_cats')
            for cat in cats:
                if chek_cat_accessing(cat.get('id')):
                    if chek_user_seen_cat(user_id, cat.get('id')):
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=cat.get('catname'),
                                callback_data='катюз-' + str(cat.get('id'))
                            )
                        )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=cat.get('catname'),
                            callback_data='катюз-' + str(cat.get('id'))
                        )
                    )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('arch_btn_for_user'),
                    callback_data='archchatuser'
                )
            )
            if message:
                bot.send_message(
                    message.chat.id,
                    mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
            else:
                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
        else:
            mes_text = ru.get('no_cats')
            if message:
                bot.send_message(
                    message.chat.id,
                    mes_text,
                    parse_mode='html')
            else:
                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=mes_text,
                    parse_mode='html')
    else:
        mes_text = ru.get('no_cats')
        if message:
            bot.send_message(
                message.chat.id,
                mes_text,
                parse_mode='html')
        else:
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html')


def keymenu(message):
    user_id = message.from_user.id
    unset_chats(user_id)
    if message.text == '/start':
        startmenu(message)
    if user_id in config.admin or chk_admin(user_id):
        if message.text == ru.get('users_menu_btn'):
            m_admin(message)
        if message.text == ru.get('polls'):
            m_polls(message=message)
        if message.text == ru.get('chats_btn'):
            chats_menu(message=message)
    else:
        if message.text == ru.get('polls_user_menu_btn'):
            m_user_polls(message)
        if message.text == ru.get('chats_user_menu_btn'):
            m_user_chats(message=message)
        if message.text == ru.get('settings'):
            m_user_settings(message=message)
        if message.text == ru.get('info_btn'):
            m_user_info(message=message)
