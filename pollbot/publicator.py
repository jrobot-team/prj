# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utilites import (Basedate, chek_cat_accessing, chek_user_seen_cat,
                          chk_admin, do_public_poll, get_chat_counts,
                          get_chat_info, get_on_chat_users, get_poll_info,
                          get_poll_users, get_users, getadmins_ids,
                          pollstat_sorter, user_info)
from lang import ru

bot = telebot.TeleBot(config.token)


def send_message_to_chat(chatid, user_id, msg, file_id=None, mtype=None):
    username = user_info(user_id)
    if user_id in config.admin:
        username = 'Администратор'
    else:
        if username[1]:
            username = username[1]
        else:
            username = username[0]
    users = get_on_chat_users(chatid)
    mes_text = ru.get('msg').format(
        name=username,
        message=msg
    )
    for user in users:
        if user.get('user_id') != user_id:
            try:
                if file_id:
                    if mtype == 'doc':
                        bot.send_document(user.get('user_id'), file_id)
                    else:
                        bot.send_photo(user.get('user_id'), photo=file_id, caption=username)
                else:
                    bot.send_message(
                        user.get('user_id'),
                        mes_text,
                        parse_mode='html')
            except:
                pass


def alert_open_chat(chatid, sender):
    users = get_users()
    chatinfo = get_chat_info(chatid)
    catid = chatinfo.get('catid')
    if users:
        for user in users:
            user_id = user[0]
            if chatinfo.get('chat_url') == 'no_url':
                mes_text = ru.get('chat_menu_text_detail').format(
                    date_create=chatinfo.get('date_create'),
                    chat_name=chatinfo.get('chat_name')
                )
            else:
                mes_text = ru.get('chat_menu_text_with_url_detail').format(
                    date_create=chatinfo.get('date_create'),
                    chat_name=chatinfo.get('chat_name'),
                    chat_url=chatinfo.get('chat_url')
                )
            try:
                if chek_cat_accessing(catid):
                    if chek_user_seen_cat(user_id, catid):
                        if user_id != sender:
                            keyboard = types.InlineKeyboardMarkup()
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=ru.get('append_to_chat').format(
                                        count=get_chat_counts(chatid, user_id)
                                    ),
                                    callback_data='присоединиться-' + str(chatid)
                                )
                            )
                            bot.send_message(
                                user_id,
                                mes_text,
                                parse_mode='html',
                                reply_markup=keyboard)
                        else:
                            if sender not in config.admin or chk_admin(sender) is not True:
                                admins = getadmins_ids()
                                for suadm in config.admin:
                                    admins.append(suadm)
                                for admin in admins:
                                    keyboard = types.InlineKeyboardMarkup()
                                    keyboard.add(
                                        types.InlineKeyboardButton(
                                            text=ru.get('append_to_chat').format(
                                                count=get_chat_counts(chatid, admin)
                                            ),
                                            callback_data='присоединиться-' + str(chatid)
                                        )
                                    )
                                    bot.send_message(
                                        admin,
                                        mes_text,
                                        parse_mode='html',
                                        reply_markup=keyboard)
                else:
                    if user_id != sender:
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('append_to_chat').format(
                                    count=get_chat_counts(chatid, user_id)
                                ),
                                callback_data='присоединиться-' + str(chatid)
                            )
                        )
                        bot.send_message(
                            user_id,
                            mes_text,
                            parse_mode='html',
                            reply_markup=keyboard)
                    else:
                        if sender not in config.admin or chk_admin(sender) is not True:
                            admins = getadmins_ids()
                            for suadm in config.admin:
                                admins.append(suadm)
                            for admin in admins:
                                keyboard = types.InlineKeyboardMarkup()
                                keyboard.add(
                                    types.InlineKeyboardButton(
                                        text=ru.get('append_to_chat').format(
                                            count=get_chat_counts(chatid, admin)
                                        ),
                                        callback_data='присоединиться-' + str(chatid)
                                    )
                                )
                                bot.send_message(
                                    admin,
                                    mes_text,
                                    parse_mode='html',
                                    reply_markup=keyboard)
            except:
                pass


def alert_close_chat(chatid):
    users = get_users()
    chatinfo = get_chat_info(chatid)
    if users:
        for user in users:
            user_id = user[0]
            if chatinfo.get('chat_url') == 'no_url':
                mes_text = ru.get('chat_menu_text_detail_close').format(
                    date_create=chatinfo.get('date_create'),
                    chat_name=chatinfo.get('chat_name')
                )
            else:
                mes_text = ru.get('chat_menu_text_with_url_detail_close').format(
                    date_create=chatinfo.get('date_create'),
                    chat_name=chatinfo.get('chat_name'),
                    chat_url=chatinfo.get('chat_url')
                )
            try:
                bot.send_message(
                    user_id,
                    mes_text,
                    parse_mode='html')
            except:
                pass


def poll(user_id, pollid, chat=False):
    date = Basedate().date_hms()
    pollinfo = get_poll_info(pollid)
    pollname = pollinfo[0]
    polltext = pollinfo[1]
    choises = pollinfo[2]
    poll = ru.get('poll_whith_choises').format(
        pollid=pollid,
        date=date,
        pollname=pollname,
        polltext=polltext)
    keyboard = types.InlineKeyboardMarkup()
    interviewed = user_info(user_id)[5]
    if interviewed:
        for choise in choises:
            choise_name = choise.get('var')
            choise_num = choise.get('num')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=choise_name,
                    callback_data='usrcvar!' + str(pollid) + '!' + str(choise_num)))
    else:
        date = Basedate().date_hms()
        pollstats = pollstat_sorter(pollid)
        pollinfo = get_poll_info(pollid)
        pollname = pollinfo[0]
        polltext = pollinfo[1]
        publicdate = str(pollstats[1])
        polled_count = pollstats[2]
        stat_mess = pollstats[3]
        poll = ru.get('active_poll_details').format(
            pollname=pollname,
            publicdate=publicdate,
            polled_count=polled_count,
            polltext=polltext,
            pollstat=stat_mess,
            date=date)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('reload'),
                callback_data='pollactiveview}' + str(pollid)))
    if chat:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('open_chat'),
                callback_data='useropenchat=' + str(user_id)))
    bot.send_message(
        user_id,
        poll,
        parse_mode='html',
        reply_markup=keyboard)


def poll_sender(pollid, chat=False):
    do_public_poll(pollid)
    users = get_poll_users()
    doc = get_poll_info(pollid)[6]
    for user in users:
        try:
            if doc:
                bot.send_document(user, doc)
            poll(user, pollid, chat=False)
        except:
            pass


def send_direct_msg(user_id, replay_to_id, msg):
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        userinfo = user_info(replay_to_id)
        if userinfo[1]:
            username = userinfo[1]
        else:
            username = userinfo[0]
        msg = ru.get('admin_sender_text').format(
            uid=replay_to_id,
            username=username,
            msg=msg)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('userprofile_btn').format(
                    uid=replay_to_id,
                    username=username),
                callback_data='userprofile$' + str(replay_to_id)))
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('replay_msg'),
                callback_data='replay_msg%' + str(replay_to_id)))
    bot.send_message(
        user_id,
        msg,
        parse_mode='html',
        reply_markup=keyboard)


def new_user_registered_send_to_admin(uid):
    fio = user_info(uid)[1]
    mes_text = ru.get('aler_new_user_reg').format(
        uid=uid,
        fio=fio)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('profile'),
            callback_data='userprofile$' + str(uid)))
    adminsids = getadmins_ids()
    for aid in config.admin:
        adminsids.append(aid)
    for admin in adminsids:
        bot.send_message(
            admin,
            mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def alert_reset_pwd(user_id):
    mes_text = ru.get('alert_reset_user_pwd')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('change_pwd'),
            callback_data='change_pwd_by_user'))
    bot.send_message(
        user_id,
        mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def admin_alert(user_id):
    mes_text = ru.get('admin_alert')
    bot.send_message(
        user_id,
        mes_text,
        parse_mode='html')


def remove_from_admin_alert(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(ru.get('polls_user_menu_btn')),
        types.KeyboardButton(ru.get('chats_user_menu_btn')))
    keyboard.add(
        types.KeyboardButton(ru.get('settings')))
    mes_text = ru.get('remove_admin_alert')
    bot.send_message(
        user_id,
        mes_text,
        parse_mode='html',
        reply_markup=keyboard)
