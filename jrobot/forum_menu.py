# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utils import date_revers
from forum_utils import (append_user_to_forum, get_forum_info,
                         get_forum_users, get_forums_by_user_id_and_status,
                         remove_user_from_forum, user_on_forum)
from lng_fn import lng
from paginators import paginator
from users_utils import get_all_group_users_by_group_id, get_user_info
from calendar_helper import create_calendar

# telegram bot api
bot = telebot.TeleBot(config.token)


def forum_menu(c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    forums = get_forums_by_user_id_and_status(user_id, status=1)
    keyboard = types.InlineKeyboardMarkup()
    if forums:
        mes_text = lng(user_id).get('forums_menu_text')
        for forum in forums:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=forum.get('forum_name'),
                    callback_data='forum%' + str(forum.get('forum_id')) + '%main'
                )
            )
    else:
        mes_text = lng(user_id).get('forums_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('create_forum_mnu_btn'),
            callback_data='запланировать_собрание'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('end_forum_mnu_btn'),
            callback_data='завершенные_собрания'
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


def forums_by_status_menu(c=None, message=None, status=0):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    forums = get_forums_by_user_id_and_status(user_id, status=status)
    if forums:
        if status == 0:
            mes_text = lng(user_id).get('closed_forums_menu_text').format(
                count=len(forums)
            )
            where_come = '%closed'
        if status == 1:
            mes_text = lng(user_id).get('active_forums_menu_text').format(
                count=len(forums)
            )
            where_come = '%active'
        for forum in forums:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=forum.get('forum_name'),
                    callback_data='forum%' + str(forum.get('forum_id')) + where_come
                )
            )
    else:
        if status == 0:
            mes_text = lng(user_id).get('noclosed_forums_menu_text')
        if status == 1:
            mes_text = lng(user_id).get('noactive_forums_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='собрания'
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


def forum_detail_menu(forum_id, c=None, message=None, where_from='main', uid=0, send=0, head=0):
    if c:
        user_id = c.from_user.id
    if message:
        user_id = message.from_user.id
    if uid:
        user_id = uid
    foruminfo = get_forum_info(forum_id)
    status = foruminfo.get('status')
    username = get_user_info(foruminfo.get('creator_id')).get('name')
    users = ''
    forum_users = get_forum_users(forum_id)
    for user in forum_users:
        users += user.get('name') + '\n'
    if send:
        mes_text = lng(user_id).get('forum_details_text_alert_15_min').format(
            forum_name=foruminfo.get('forum_name'),
            username=username,
            date_create=date_revers(foruminfo.get('date_create')),
            date_start=date_revers(foruminfo.get('date_start')),
            time_delta=foruminfo.get('info').get('delta'),
            forum_theme=foruminfo.get('forum_theme'),
            users=users
        )
    else:
        if foruminfo.get('info').get('comment'):
            comment = 'Итоги собрания:\n' + foruminfo.get('info').get('comment')
        else:
            comment = ''
        if head:
            head = lng(user_id).get('forum_ended_head')
        else:
            head = ''
        mes_text = head + lng(user_id).get('forum_details_text').format(
            forum_name=foruminfo.get('forum_name'),
            username=username,
            date_create=date_revers(foruminfo.get('date_create')),
            date_start=date_revers(foruminfo.get('date_start')),
            time_delta=foruminfo.get('info').get('delta'),
            forum_theme=foruminfo.get('forum_theme'),
            users=users,
            comment=comment
        )
    keyboard = types.InlineKeyboardMarkup()
    if foruminfo.get('creator_id') == user_id:
        if status:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('cancel_mnu_btn'),
                    callback_data='отменить_собрание.' + str(forum_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('end_mnu_btn'),
                    callback_data='завершить_собрание!' + str(forum_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_name'),
                    callback_data='собрание-изменить-имя=' + str(forum_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_date'),
                    callback_data='собраниедата=' + str(forum_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_theme'),
                    callback_data='собраниеповестка=' + str(forum_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_users'),
                    callback_data='собраниеучастники=' + str(forum_id)
                )
            )
        else:
            if foruminfo.get('info').get('comment'):
                pass
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('add_forum_comment'),
                        callback_data='итогис!' + str(forum_id)
                    )
                )
    if where_from == 'main':
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='собрания'
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='завершенные_собрания'
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


def forum_calendar_menu(forum_id, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('forum_create_get_date').format(
        forum_name=get_forum_info(forum_id).get('forum_name')
    )
    cb = 'forum+' + str(forum_id)
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


def forum_time_menu(forum_id, date_start, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('forum_create_time_text').format(
        forum_name=get_forum_info(forum_id).get('forum_name')
    )
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
        callback_data='deltas>' + str(forum_id) + '>' + date_start + '>' + time) for time in timeslst])
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_date'),
            callback_data='deltas>' + str(forum_id) + '>' + date_start + '>manual'
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


def forum_delta_menu(forum_id, date_start, time, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('forum_create_delta_time').format(
        forum_name=get_forum_info(forum_id).get('forum_name')
    )
    deltas = ['00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00']
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(
        text=dt,
        callback_data=';фв>' + str(forum_id) + '>' + date_start + '>' + time + '>' + dt + '>1>0') for dt in deltas])
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


def forum_users_menu(c, forum_id, date_start, time, delta, page, uid, edit=0):
    user_id = c.from_user.id
    if edit:
        cc = 'ФУ>'
    else:
        cc = ';фв>'
    if uid:
        if user_on_forum(forum_id, uid):
            remove_user_from_forum(forum_id, uid)
        else:
            append_user_to_forum(forum_id, uid)
    group_id = get_forum_info(forum_id).get('group_id')
    users = get_all_group_users_by_group_id(group_id)
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = lng(user_id).get('forum_add_users').format(
            forum_name=get_forum_info(forum_id).get('forum_name')
        )
        onboard = '✅'
        kiked = ''
        for user in userspage:
            uid = user.get('user_id')
            if user_on_forum(forum_id, uid):
                mark = onboard
            else:
                mark = kiked
            cdata = cc + str(forum_id) + '>' + str(date_start) + '>' + str(time) + '>' + delta + '>' + str(page) + '>' + str(uid)
            keyboard.add(
                types.InlineKeyboardButton(
                    text=get_user_info(uid).get('name') + ' ' + mark,
                    callback_data=cdata
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
                            text=lng(user_id).get('next'),
                            callback_data=cc + str(forum_id) + '>' + str(date_start) + '>' + str(time) + '>' + delta + '>' + str(page + 1) + '>0'
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('back_p'),
                            callback_data=cc + str(forum_id) + '>' + str(date_start) + '>' + str(time) + '>' + delta + '>' + str(page - 1) + '>0'
                        ),
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('next'),
                            callback_data=cc + str(forum_id) + '>' + str(date_start) + '>' + str(time) + '>' + delta + '>' + str(page + 1) + '>0'
                        )
                    )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data=cc + str(forum_id) + '>' + str(date_start) + '>' + str(time) + '>' + delta + '>' + str(page - 1) + '>0'
                    )
                )
    else:
        mes_text = lng(user_id).get('forum_add_users_nousers')
    if edit:
        create_btn_call = 'ЗУФ<'
        text = lng(user_id).get('edit_forum_users_end')
    else:
        create_btn_call = 'зсф<'
        text = lng(user_id).get('create_forum_end_btn')
    keyboard.add(
        types.InlineKeyboardButton(
            text=text,
            callback_data=create_btn_call + str(forum_id) + '<' + str(date_start) + '<' + str(time) + '<' + delta
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
