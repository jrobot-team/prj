# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from lng_fn import lng
from poll_utils import (get_poll_info, get_polls_by_user_id,
                        get_user_choose_var_name, is_user_polled,
                        poll_stata_formatter, rec_user_choosed)
from calendar_helper import create_calendar

# telegram bot api
bot = telebot.TeleBot(config.token)


def polls_menu(c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    active_polls = get_polls_by_user_id(user_id, status=1)
    keyboard = types.InlineKeyboardMarkup()
    if active_polls:
        mes_text = lng(user_id).get('user_polls_menu_text')
        for poll in active_polls:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=poll.get('name'),
                    callback_data='poll-' + str(poll.get('id'))
                )
            )
    else:
        mes_text = lng(user_id).get('user_nopolls_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_poll_mnu_btn'),
            callback_data='создать_опрос'
        ),
        types.InlineKeyboardButton(
            text=lng(user_id).get('arch_polls'),
            callback_data='архив_опросов'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('to_menu_btn'),
            callback_data='MENU'
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


def arch_polls_menu(c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    arch_polls = get_polls_by_user_id(user_id, status=0)
    keyboard = types.InlineKeyboardMarkup()
    if arch_polls:
        mes_text = lng(user_id).get('user_arch_polls_menu_text')
        for poll in arch_polls:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=poll.get('name'),
                    callback_data='poll-' + str(poll.get('id'))
                )
            )
    else:
        mes_text = lng(user_id).get('user_arch_nopolls_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='опросы'
        ),
        types.InlineKeyboardButton(
            text=lng(user_id).get('to_menu_btn'),
            callback_data='MENU'
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


def poll_detail_menu(poll_id, c=None, message=None, uid=None):
    if c:
        user_id = c.from_user.id
    if message:
        user_id = message.from_user.id
    if uid:
        user_id = uid
    keyboard = types.InlineKeyboardMarkup()
    pollinfo = get_poll_info(poll_id)
    variants = pollinfo.get('chooses')
    if pollinfo.get('status'):
        status = lng(user_id).get('active')
    else:
        status = lng(user_id).get('passive')
    if is_user_polled(user_id, poll_id):
        if status == lng(user_id).get('passive'):
            results = lng(user_id).get('poll_results').format(
                poll_results=poll_stata_formatter(poll_id)
            )
        else:
            varname = get_user_choose_var_name(user_id, poll_id)
            results = lng(user_id).get('user_polled_varname').format(
                varname=varname
            )
        mes_text = lng(user_id).get('poll_detail_text').format(
            pollname=pollinfo.get('name'),
            polltext=pollinfo.get('polltext'),
            date_create=pollinfo.get('date_create'),
            date_end=pollinfo.get('date_end'),
            status=status,
            results=results
        )
    else:
        if status == lng(user_id).get('passive'):
            results = lng(user_id).get('poll_results').format(
                poll_results=poll_stata_formatter(poll_id)
            )
        else:
            results = ''
        mes_text = lng(user_id).get('poll_detail_text').format(
            pollname=pollinfo.get('name'),
            polltext=pollinfo.get('polltext'),
            date_create=pollinfo.get('date_create'),
            date_end=pollinfo.get('date_end'),
            status=status,
            results=results
        )
        for var in variants:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=var.get('choose'),
                    callback_data='вариант@' + str(poll_id) + '@' + str(var.get('id'))
                )
            )
    if status == lng(user_id).get('passive'):
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='архив_опросов'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('to_menu_btn'),
                callback_data='MENU'
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='опросы'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('to_menu_btn'),
                callback_data='MENU'
            )
        )
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    if c:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    if uid:
        bot.send_message(
            uid,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def user_select_poll_variant(c, poll_id, var_id):
    user_id = c.from_user.id
    rec_user_choosed(user_id, poll_id, var_id)
    ans_text = lng(user_id).get('user_select_poll_variant_ans_text').format(
        var=get_user_choose_var_name(user_id, poll_id)
    )
    bot.answer_callback_query(
        c.id,
        text=ans_text,
        show_alert=True)
    poll_detail_menu(poll_id, c=c)


def poll_calendar_menu(poll_id, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('poll_create_get_date')
    cb = 'poll+' + str(poll_id)
    markup = create_calendar(cb=cb)
    if c:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=markup)
    else:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=markup)


def poll_time_menu(poll_id, date_end, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('poll_create_time_text')
    keyboard = types.InlineKeyboardMarkup()
    times = [t for t in range(8, 21)]
    timeslst = []
    for t in times:
        time = str(t) + ':00'
        if len(time) == 4:
            time = '0' + time
        timeslst.append(time)
    keyboard.add(*[types.InlineKeyboardButton(
        text=time,
        callback_data='заопрос>' + str(poll_id) + '>' + date_end + '>' + time) for time in timeslst])
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_date'),
            callback_data='заопрос>' + str(poll_id) + '>' + date_end + '>manual'
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
