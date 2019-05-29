# -*- coding: utf-8 -*-
import logging

import cherrypy
import telebot
from telebot import types

import config
from bot_utilites import (Basedate, add_cat, add_group_and_set_admin_fn,
                          add_group_fn, add_poll_choise_fn, add_to_group,
                          append_chat_to_cat, change_activation,
                          change_group_admin, change_user_status,
                          chek_user_password, chek_user_polled, chk_admin,
                          close_poll, copy_poll, date_start_updater, del_group,
                          del_poll_choise, delete_cat, delete_open_chat,
                          delete_user, delpoll_fn, edit_cat_name, edit_choise,
                          edit_pollname, get_arch_polls,
                          get_chat_appended_to_user, get_chat_arch_messages,
                          get_chat_cats, get_chat_counts, get_chat_info,
                          get_chat_user_count, get_draft_polls, get_group_info,
                          get_group_users, get_groupid_from_admin, get_groups,
                          get_open_polls, get_poll_info, get_poll_user_choise,
                          get_tmp_choiseid, get_tmp_groupid, get_tmp_pollid,
                          get_tmp_pollid_choiseid, get_tmp_uid, get_users,
                          lastpollid, make_admin, make_chat_url, make_fio,
                          make_on_chat_user, make_password, make_poll_name_fn,
                          make_poll_text_fn, make_temp_choiseid,
                          make_tmp_change_fio, make_tmp_replay_to,
                          make_tmp_uid, new_chat_name_fn, open_chat,
                          pollstat_sorter, record_chat_story, remove_admin,
                          remove_user_from_group, rename_group, replacer,
                          reset_password, temp_del, tmp_groupid, tmp_pollid,
                          tmp_user_choised, upd_chat_count, upd_chat_status,
                          upd_poll_doc, user_info, user_on_chat,
                          user_select_choise)
from lang import ru
from menu import (chats_menu, keymenu, m_polls, m_user_chats, m_user_info,
                  m_user_settings, startmenu)
from mnu import (access_menu, access_users_mnu, active_cat_detail_menu,
                 active_chat, active_chat_detail_menu, active_polls_mnu,
                 add_admin_and_make_group_mnu, add_group_admin_mnu,
                 all_groups_mnu, arch_cat_detail_user_menu, arch_chat,
                 arch_chat_detail_menu, arch_chat_detail_user_menu,
                 arch_chat_user_menu, candidate_mnu, cat_detail_menu,
                 cat_detail_user_menu, cats_menu, chat_detail_menu,
                 chat_detail_user_menu, done_mnu, draftpolls_mnu, group_mnu,
                 group_users, no_group_users, pollactiveview_mnu, pollmnu,
                 su_admin_mnu, userprofile_mnu, users_mnu, view_access_to_cat,
                 wait_chat)
from paginators import paginator
from publicator import (admin_alert, alert_close_chat, alert_open_chat,
                        alert_reset_pwd, new_user_registered_send_to_admin)
from publicator import poll as pollsender
from publicator import (poll_sender, remove_from_admin_alert, send_direct_msg,
                        send_message_to_chat)
from statistic import (create_arch_chat_messages_file, create_stata_file,
                       create_users_file)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


# telegram bot api
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.token)

cancel = [
    ru.get('users_menu_btn'),
    ru.get('polls'),
    ru.get('settings'),
    ru.get('info_btn'),
    ru.get('chats_btn'),
    ru.get('polls_user_menu_btn'),
    ru.get('chats_user_menu_btn'),
    '/start',
    '/Start'
]

###################################################


def make_poll_name(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        poll_name = replacer(message.text)
        pollid = make_poll_name_fn(poll_name)
        mes_text = ru.get('admin_make_poll_name').format(
            pollname=poll_name)
        tmp_pollid(user_id, pollid)
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_poll_text)


def edit_poll_name(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        poll_name = replacer(message.text)
        pollid = get_tmp_pollid(user_id)
        if pollid:
            edit_pollname(pollid, poll_name)
            done_mnu(message)
            pollmnu(pollid, message=message)


def make_poll_text(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        polltext = message.text
        pollid = get_tmp_pollid(user_id)
        temp_del(user_id)
        if pollid:
            pollname = get_poll_info(pollid)[0]
            make_poll_text_fn(pollid, polltext)
            mes_text = ru.get('polltext_added').format(
                pollid=pollid,
                pollname=pollname,
                polltext=polltext)
            tmp_pollid(user_id, pollid)
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, make_poll_choises)


def edit_poll_text(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        polltext = message.text
        pollid = get_tmp_pollid(user_id)
        if pollid:
            done_mnu(message)
            pollname = get_poll_info(pollid)[0]
            make_poll_text_fn(pollid, polltext)
            mes_text = ru.get('polltext_edited').format(
                pollid=pollid,
                pollname=pollname,
                polltext=polltext)
            pollmnu(pollid, message=message, mes_text=mes_text)


def make_poll_choises(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        pollchoises = message.text
        pollid = get_tmp_pollid(user_id)
        if pollid:
            add_poll_choise_fn(pollid, pollchoises)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            polltext = pollinfo[1]
            pollchoises = pollinfo[2]
            mes_text = ru.get('pollchoise_added').format(
                pollid=pollid,
                pollname=pollname,
                polltext=polltext)
            pollmnu(pollid, message=message, mes_text=mes_text)


def edit_poll_choise(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        pollchoise = message.text
        getids = get_tmp_choiseid(user_id)
        if getids:
            pollid = getids[0]
            choiseid = getids[1]
            old_choise = edit_choise(pollid, choiseid, pollchoise)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            polltext = pollinfo[1]
            done_mnu(message)
            mes_text = ru.get('pollchoise_edited').format(
                pollid=pollid,
                pollname=pollname,
                polltext=polltext,
                old_choise=old_choise,
                new_choise=pollchoise)
            pollmnu(pollid, message=message, mes_text=mes_text)


def edit_user_fio_by_admin(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        fio = replacer(message.text)
        uid = get_tmp_uid(user_id)
        make_fio(uid, fio)
        userprofile_mnu(uid, message=message)


def send_direct_message(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        uid = get_tmp_uid(user_id)
        direct_msg = replacer(message.text)
        send_direct_msg(uid, user_id, direct_msg)
        mes_text = ru.get('msg_is_send')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        userprofile_mnu(uid, message=message)


def user_send_direct_message(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        uid = get_tmp_uid(user_id)
        direct_msg = replacer(message.text)
        send_direct_msg(uid, user_id, direct_msg)
        mes_text = ru.get('msg_is_send')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')


def add_group_and_make_admin(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        uid = get_tmp_uid(user_id)
        groupname = replacer(message.text)
        groupid = add_group_and_set_admin_fn(groupname, uid)
        change_user_status(uid, config.statuses[2])
        add_to_group(groupid, uid)
        no_group_users(groupid, 1, message=message)


def add_group(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        groupname = replacer(message.text)
        groupid = add_group_fn(groupname)
        mes_text = ru.get('group_added_text').format(
            groupname=groupname,
            user_count=len(get_group_users(groupid)))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('change_group_admin_btn'),
                callback_data='change_group_admin;' + str(groupid) + str(';1')))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_poll_name'),
                callback_data='rename_group&' + str(groupid)),
            types.InlineKeyboardButton(
                text=ru.get('choise_del'),
                callback_data='del_group!@'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('in_group_user_view'),
                callback_data='no'),
            types.InlineKeyboardButton(
                text=ru.get('back_to_groups'),
                callback_data='usergproups.1'))
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def edit_group_name(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        groupname = replacer(message.text)
        groupid = get_tmp_groupid(user_id)
        rename_group(groupid, groupname)
        group_mnu(groupid, message=message)


def register_fio(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        fio = replacer(message.text)
        make_fio(user_id, fio)
        mes_text = ru.get('register_pwd').format(
            fio=fio)
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, register_pwd)


def change_user_fio(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        fio = replacer(message.text)
        make_fio(user_id, fio)
        mes_text = ru.get('user_fio_is_changed')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        m_user_info(message)


def register_pwd(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        pwd = message.text
        make_password(user_id, pwd)
        new_user_registered_send_to_admin(user_id)
        userinfo = user_info(user_id)
        fio = userinfo[1]
        pwd = ru.get('userpwd_on')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton(ru.get('polls_user_menu_btn')),
            types.KeyboardButton(ru.get('chats_user_menu_btn')))
        keyboard.add(
            types.KeyboardButton(ru.get('settings')))
        mes_text = ru.get('usermenu_text_status_off').format(
            user_id=user_id,
            fio=fio,
            pwd=pwd)
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def change_user_pwd(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        pwd = message.text
        make_password(user_id, pwd)
        mes_text = ru.get('user_pwd_is_changed')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        m_user_info(message)


def chek_password(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
        temp_del(user_id)
    else:
        pwd = message.text
        chekpwd = chek_user_password(user_id, pwd)
        pollids = get_tmp_pollid_choiseid(user_id)
        pollid = pollids[0]
        choiseid = pollids[1]
        pollinfo = get_poll_info(pollid)
        if pollinfo:
            if pollinfo[3]:
                if chek_user_polled(user_id, pollid):
                    mes_text = ru.get('poll_is_polled_by_user')
                else:
                    variant = ru.get('nofind')
                    for var in pollinfo[2]:
                        if var.get('num') == choiseid:
                            variant = var.get('var')
                    if chekpwd:
                        if chek_user_polled(user_id, pollid):
                            pass
                        else:
                            user_select_choise(user_id, pollid, choiseid)
                        mes_text = ru.get('user_poll_done').format(
                            variant=variant)
                    else:
                        mes_text = ru.get('user_password_error').format(
                            variant=variant)
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('back_to_poll'),
                                callback_data='pollactiveview}' + str(pollid)),
                            types.InlineKeyboardButton(
                                text=ru.get('password_send_again'),
                                callback_data='usrcvar!' + str(pollid) + '!' + str(choiseid)))
                        bot.send_message(
                            message.chat.id,
                            text=mes_text,
                            parse_mode='html',
                            reply_markup=keyboard)
            else:
                mes_text = ru.get('poll_is_dead')
        else:
            mes_text = ru.get('poll_is_dead')
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        if pollinfo:
            if chekpwd:
                pollactiveview_mnu(user_id, pollid, message=message)


def new_chat_name(message, catid=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
    else:
        chat_name = replacer(message.text)
        chatid = new_chat_name_fn(chat_name)
        if catid:
            append_chat_to_cat(catid, chatid)
        mes_text = ru.get('enter_chat_url_text').format(
            chat_name=chat_name,
            date_create=get_chat_info(chatid).get('date_create')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('chat_url_append_btn'),
                callback_data='доб_ссылку_на_тр-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            )
        )
        if user_id in config.admin or chk_admin(user_id):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='п_обсуждения'
                )
            )
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def new_chat_url(message, chatid=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
    else:
        chat_url = message.text
        make_chat_url(chatid, chat_url)
        chatinfo = get_chat_info(chatid)
        mes_text = ru.get('chat_menu_text_with_url_detail').format(
            chat_name=chatinfo.get('chat_name'),
            date_create=chatinfo.get('date_create'),
            chat_url=chatinfo.get('chat_url')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            )
        )
        if user_id in config.admin or chk_admin(user_id):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='п_обсуждения'
                )
            )
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def edit_chat_url(message, chatid=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
    else:
        chat_url = message.text
        make_chat_url(chatid, chat_url)
        if user_id in config.admin or chk_admin(user_id):
            chat_detail_menu(message=message, chatid=chatid)
        else:
            chat_detail_user_menu(message=message, chatid=chatid)


def new_chat_date_start(message, chatid=0):
    if message.text in cancel:
        keymenu(message)
    else:
        date_start = date_start_updater(message.text, chatid)
        if date_start:
            chatinfo = get_chat_info(chatid)
            if chatinfo.get('chat_url') == 'no_url':
                mes_text = ru.get('new_chat_make_done').format(
                    chat_name=chatinfo.get('chat_name'),
                    date_create=chatinfo.get('date_create'),
                    date_start=chatinfo.get('date_start')
                )
            else:
                mes_text = ru.get('new_chat_make_done_with_url').format(
                    chat_name=chatinfo.get('chat_name'),
                    date_create=chatinfo.get('date_create'),
                    date_start=chatinfo.get('date_start'),
                    chat_url=chatinfo.get('chat_url')
                )
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('start_chat'),
                    callback_data='стартовать_-' + str(chatid)
                ),
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            mes_text = ru.get('new_chat_date_error')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, new_chat_date_start, chatid=chatid)


def first_message_on_chat(message, chatid=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
    else:
        msg = message.text
        if message.document:
            file_id = message.document.file_id
            mtype = 'doc'
            msg = message.document.file_name
        elif message.photo:
            file_id = message.photo[0].file_id
            mtype = 'photo'
        else:
            file_id = None
            mtype = None
        open_chatid = get_chat_appended_to_user(user_id)
        if open_chatid == chatid:
            send_message_to_chat(chatid, user_id, msg, file_id=file_id, mtype=mtype)
            if file_id:
                record_chat_story(user_id, chatid, file_id, mtype)
            else:
                record_chat_story(user_id, chatid, msg, 'txt')
        else:
            mes_text = ru.get('chat_close')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')


def add_doc_to_poll(message, pollid=0):
    if message.text in cancel:
        keymenu(message)
    else:
        file_id = message.document.file_id
        file_name = message.document.file_name
        upd_poll_doc(pollid, file_id, file_name)
        pollmnu(pollid, message=message)


def new_category_name(message, frommenu=0):
    if message.text in cancel:
        keymenu(message)
    else:
        catname = replacer(message.text)
        catid = add_cat(catname)
        if frommenu:
            mes_text = ru.get('new_chat_menu_text')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, new_chat_name, catid=catid)
        else:
            cats_menu(message=message)


def edit_category_name(message, catid=0):
    if message.text in cancel:
        keymenu(message)
    else:
        catname = replacer(message.text)
        edit_cat_name(catid, catname)
        cat_detail_menu(catid, message=message)


# Регистрация
@bot.message_handler(commands=['start', 'Start'])
def start(message):
    startmenu(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'document', 'photo'])
def menu(message):
    if message.text in cancel:
        keymenu(message)
    else:
        user_id = message.from_user.id
        msg = message.text
        if message.document:
            file_id = message.document.file_id
            mtype = 'doc'
            msg = message.document.file_name
        elif message.photo:
            file_id = message.photo[0].file_id
            mtype = 'photo'
        else:
            file_id = None
            mtype = None
        chatid = get_chat_appended_to_user(user_id)
        if chatid:
            if user_on_chat(user_id, chatid):
                send_message_to_chat(chatid, user_id, msg, file_id=file_id, mtype=mtype)
                if file_id:
                    record_chat_story(user_id, chatid, file_id, mtype)
                else:
                    record_chat_story(user_id, chatid, msg, 'txt')
        else:
            mes_text = ru.get('chat_close')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if 'accessaddusr=' in c.data:
        call = c.data.split('=')
        catid = int(call[1])
        users = get_users()
        page = int(call[2])
        uid = int(call[3])
        state = int(call[4])
        chk = int(call[5])
        access_users_mnu(c, catid, users, page, uid, state, chk)

    if 'accessview=' in c.data:
        catid = int(c.data.split('=')[1])
        view_access_to_cat(c, catid)

    if 'доступ-' in c.data:
        catid = int(c.data.split('-')[1])
        access_menu(c, catid)

    if 'смархч-' in c.data:
        chatid = int(c.data.split('-')[1])
        arch_chat_detail_user_menu(c=c, chatid=chatid)

    if 'archcatsee-' in c.data:
        catid = int(c.data.split('-')[1])
        arch_cat_detail_user_menu(catid, c=c)

    if c.data == 'archchatuser':
        arch_chat_user_menu(c)

    if 'архсообщения-' in c.data:
        chatid = int(c.data.split('-')[1])
        msgs_arch = get_chat_arch_messages(chatid)
        if len(msgs_arch) > 0:
            for msg_arch in msgs_arch:
                username = user_info(msg_arch.get('user_id'))
                if username:
                    if user_info(msg_arch.get('user_id')) in config.admin:
                        username = 'Администратор'
                    else:
                        if username[1]:
                            username = username[1]
                        else:
                            username = username[0]
                else:
                    username = 'Администратор'
                if msg_arch.get('type') == 'text':
                    chat_text = ru.get('msg').format(
                        name=username,
                        message=msg_arch.get('message')
                    )
                    bot.send_message(
                        c.message.chat.id,
                        text=chat_text,
                        parse_mode='html')
                elif msg_arch.get('type') == 'photo':
                    bot.send_photo(
                        c.message.chat.id,
                        msg_arch.get('message')
                    )
                else:
                    bot.send_document(
                        c.message.chat.id,
                        msg_arch.get('message')
                    )
        else:
            mes_text = ru.get('nomsgs')
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html')
        arch_chat_detail_menu(c=c, arch=True)

    if 'архсообщенияюз-' in c.data:
        chatid = int(c.data.split('-')[1])
        msgs_arch = get_chat_arch_messages(chatid)
        if len(msgs_arch) > 0:
            for msg_arch in msgs_arch:
                username = user_info(msg_arch.get('user_id'))
                if username:
                    if user_info(msg_arch.get('user_id')) in config.admin:
                        username = 'Администратор'
                    else:
                        if username[1]:
                            username = username[1]
                        else:
                            username = username[0]
                else:
                    username = 'Администратор'
                if msg_arch.get('type') == 'text':
                    chat_text = ru.get('msg').format(
                        name=username,
                        message=msg_arch.get('message')
                    )
                    bot.send_message(
                        c.message.chat.id,
                        text=chat_text,
                        parse_mode='html')
                elif msg_arch.get('type') == 'photo':
                    bot.send_photo(
                        c.message.chat.id,
                        msg_arch.get('message')
                    )
                else:
                    bot.send_document(
                        c.message.chat.id,
                        msg_arch.get('message')
                    )
        else:
            mes_text = ru.get('nomsgs')
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html')
        arch_chat_detail_user_menu(chatid=chatid, c=c, arch=True)

    if 'опрос-' in c.data:
        user_id = c.from_user.id
        pollid = int(c.data.split('-')[1])
        doc = get_poll_info(pollid)[6]
        if doc:
            bot.send_document(user_id, doc)
        pollsender(user_id, pollid)

    if 'добавитьдок-' in c.data:
        pollid = int(c.data.split('-')[1])
        mes_text = ru.get('add_doc_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, add_doc_to_poll, pollid=pollid)

    if c.data == 'экспортировать':
        date = create_users_file()
        users_file = open('export_users/' + str(date) + '_users.xlsx', 'rb')
        bot.send_document(c.message.chat.id, users_file)
        mes_text = ru.get('export_done_text')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('users_menu_btn'),
                callback_data='users^1'
            )
        )
        bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'ак_удалитьп_ля-' in c.data:
        user_id = int(c.data.split('-')[1])
        delete_user(user_id)
        users = get_users()
        users_mnu(c, users, 1)

    if 'удалитьканд_та-' in c.data:
        user_id = int(c.data.split('-')[1])
        delete_user(user_id)
        users = get_users(reg=0)
        candidate_mnu(c, users, 1)

    if c.data == 'чаты':
        chats_menu(c=c)

    if 'обсуждение-' in c.data:
        chatid = int(c.data.split('-')[1])
        chat_detail_menu(c=c, chatid=chatid)

    if 'обсуждение_арх-' in c.data:
        chatid = int(c.data.split('-')[1])
        arch_chat_detail_menu(c=c, chatid=chatid)

    if 'activech-' in c.data:
        chatid = int(c.data.split('-')[1])
        active_chat_detail_menu(c=c, chatid=chatid)

    if 'стартовать_-' in c.data:
        user_id = c.from_user.id
        chatid = int(c.data.split('-')[1])
        chat_user_count = get_chat_user_count(user_id, chatid)
        upd_chat_status(chatid, 'active')
        ans_text = ru.get('chat_started_alert_text')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True
        )
        open_chat(chatid)
        alert_open_chat(chatid, sender=user_id)
        chatinfo = get_chat_info(chatid)
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
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('append_to_chat').format(
                    count=get_chat_counts(chatid, user_id) - chat_user_count
                ),
                callback_data='присоединиться-' + str(chatid)
            )
        )
        bot.send_message(
            c.message.chat.id,
            mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'остановить-' in c.data:
        chatid = int(c.data.split('-')[1])
        upd_chat_status(chatid, 'arch')
        ans_text = ru.get('chat_stoped_alert_text')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True
        )
        delete_open_chat(chatid)
        alert_close_chat(chatid)
        chats_menu(c=c)

    if 'присоединиться-' in c.data:
        user_id = c.from_user.id
        chatid = int(c.data.split('-')[1])
        chat_counts = get_chat_counts(chatid, user_id)
        upd_chat_count(user_id, chatid, chat_counts)
        make_on_chat_user(user_id, chatid)
        mes_text = ru.get('user_appended_on_chat')
        msgs_arch = get_chat_arch_messages(chatid)
        for msg_arch in msgs_arch:
            username = user_info(msg_arch.get('user_id'))
            if username:
                if user_info(msg_arch.get('user_id')) in config.admin:
                    username = 'Администратор'
                else:
                    if username[1]:
                        username = username[1]
                    else:
                        username = username[0]
            else:
                username = 'Администратор'
            if msg_arch.get('type') == 'text':
                chat_text = ru.get('msg').format(
                    name=username,
                    message=msg_arch.get('message')
                )
                bot.send_message(
                    c.message.chat.id,
                    text=chat_text,
                    parse_mode='html')
            elif msg_arch.get('type') == 'photo':
                bot.send_photo(
                    c.message.chat.id,
                    msg_arch.get('message')
                )
            else:
                bot.send_document(
                    c.message.chat.id,
                    msg_arch.get('message')
                )
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, first_message_on_chat, chatid=chatid)

    if 'удалить_-' in c.data:
        chatid = int(c.data.split('-')[1])
        upd_chat_status(chatid, 'del')
        ans_text = ru.get('chat_delited_alert_text')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True
        )
        arch_chat(c)

    if 'выгрузить-' in c.data:
        chatid = int(c.data.split('-')[1])
        create_arch_chat_messages_file(chatid)
        chat_arch_messages = open('chat_msgs/' + str(chatid) + '_msgs.xlsx', 'rb')
        bot.send_document(c.message.chat.id, chat_arch_messages)
        chatinfo = get_chat_info(chatid)
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('view_arch_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('view_arch_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('get_message_arch_btn'),
                callback_data='выгрузить-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('delite_chat'),
                callback_data='удалить_-' + str(chatid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='чаты'
            )
        )
        bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'редактировать_ссылку-' in c.data:
        chatid = int(c.data.split('-')[1])
        mes_text = ru.get('edit_chat_url_menu_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, edit_chat_url)

    if c.data == 'категории_обсуждений':
        cats_menu(c=c)

    if 'новобсвк-' in c.data:
        catid = int(c.data.split('-')[1])
        mes_text = ru.get('new_chat_menu_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, new_chat_name, catid=catid)

    if c.data == 'новое_обсуждение':
        mes_text = ru.get('choose_cat')
        keyboard = types.InlineKeyboardMarkup()
        categories = get_chat_cats()
        if len(categories):
            for cat in categories:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=cat.get('catname'),
                        callback_data='новобсвк-' + str(cat.get('id'))
                    )
                )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('add_chat_cat'),
                callback_data='добавить_категорию=1'
            ),
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='чаты'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'добавить_категорию=' in c.data:
        frommenu = int(c.data.split('=')[1])
        mes_text = ru.get('add_cat_menu_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, new_category_name, frommenu=frommenu)

    if 'категория-' in c.data:
        catid = int(c.data.split('-')[1])
        cat_detail_menu(catid, c=c)

    if 'active_cat-' in c.data:
        catid = int(c.data.split('-')[1])
        active_cat_detail_menu(catid, c=c)

    if 'катюз-' in c.data:
        catid = int(c.data.split('-')[1])
        cat_detail_user_menu(catid, c=c)

    if 'полобсужд-' in c.data:
        chatid = int(c.data.split('-')[1])
        chat_detail_user_menu(c=c, chatid=chatid)

    if c.data == 'п_обсуждения':
        m_user_chats(c=c)

    if 'кат_изменить_название-' in c.data:
        catid = int(c.data.split('-')[1])
        mes_text = ru.get('edit_cat_name_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, edit_category_name, catid=catid)

    if 'удалить_кат-' in c.data:
        catid = int(c.data.split('-')[1])
        delete_cat(catid)
        ans_text = ru.get('cat_is_del')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True)
        cats_menu(c=c)

    if 'доб_ссылку_на_тр-' in c.data:
        chatid = int(c.data.split('-')[1])
        chatinfo = get_chat_info(chatid)
        mes_text = ru.get('new_chat_append_url_text').format(
            date_create=chatinfo.get('date_create'),
            chat_name=chatinfo.get('chat_name')
        )
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, new_chat_url, chatid=chatid)

    if 'время_старта_об_я-' in c.data:
        chatid = int(c.data.split('-')[1])
        chatinfo = get_chat_info(chatid)
        mes_text = ru.get('new_chat_make_date_text').format(
            date_create=chatinfo.get('date_create'),
            chat_name=chatinfo.get('chat_name')
        )
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, new_chat_date_start, chatid=chatid)

    if c.data == 'активные_обсуждения':
        active_chat(c)

    if c.data == 'архивные_обсуждения':
        arch_chat(c)

    if c.data == 'ожидающие_обсуждения':
        wait_chat(c)

    if c.data == 'change_fio_by_user':
        mes_text = ru.get('change_user_fio')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, change_user_fio)

    if c.data == 'change_pwd_by_user':
        mes_text = ru.get('change_user_pwd')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, change_user_pwd)

    if c.data == 'register':
        user_id = c.from_user.id
        fio = user_info(user_id)[1]
        if fio:
            mes_text = ru.get('register_pwd').format(
                fio=fio)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, register_pwd)
        else:
            mes_text = ru.get('register_fio')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, register_fio)

    if c.data == 'usersadmin':
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            su_admin_mnu(c=c)

    if 'add_group+' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('+')[1])
            add_admin_and_make_group_mnu(c, page)

    if 'admin_set_to_group^' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('^')[1])
            make_tmp_uid(user_id, uid)
            mes_text = ru.get('add_group_name_text')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, add_group_and_make_admin)

    if c.data == 'pollmenu':
        user_id = c.from_user.id
        temp_del(user_id)
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
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            mes_text = ru.get('error')
            bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')

    if c.data == 'makepollname':
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            temp_del(user_id)
            pollid = lastpollid() + 1
            mes_text = ru.get('admin_make_poll_started')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, make_poll_name)

    if c.data == 'activepolls':
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            activepolls = get_open_polls()
            active_polls_mnu(c, activepolls)

    if 'users^' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('^')[1])
            users = get_users()
            users_mnu(c, users, page)

    if 'candidate*' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('*')[1])
            users = get_users(reg=0)
            candidate_mnu(c, users, page)

    if 'userprofile$' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('$')[1])
            userprofile_mnu(uid, c=c)

    if 'change_activation]' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            activation = int(c.data.split(']')[1])
            user_id = int(c.data.split(']')[2])
            if activation:
                change_activation(user_id, activ=1)
                userinfo = user_info(user_id)
                if userinfo[1]:
                    username = userinfo[1]
                else:
                    username = userinfo[0]
                ans_text = ru.get('usr_activate').format(
                    uid=user_id,
                    username=username)
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                users = get_users(reg=0)
                candidate_mnu(c, users, 1)
            else:
                change_activation(user_id, activ=0)
                userinfo = user_info(user_id)
                if userinfo[1]:
                    username = userinfo[1]
                else:
                    username = userinfo[0]
                if chk_admin(user_id):
                    remove_admin(user_id)
                    remove_from_admin_alert(user_id)
                    ans_text = ru.get('user_deactivate_and_remove_admin').format(
                        user_id=user_id,
                        username=username)
                else:
                    ans_text = ru.get('usr_deactivate').format(
                        uid=user_id,
                        username=username)
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                users = get_users()
                users_mnu(c, users, 1)

    if 'resetuserpwd]' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            user_id = int(c.data.split(']')[1])
            reset_password(user_id)
            alert_reset_pwd(user_id)
            ans_text = ru.get('reset_password_text')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            userprofile_mnu(user_id, c=c)

    if 'changefio]' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split(']')[1])
            make_tmp_change_fio(user_id, uid)
            mes_text = ru.get('admin_change_fio').format(
                uid=uid)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, edit_user_fio_by_admin)

    if 'draftpolls+' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('+')[1])
            draftpolls = get_draft_polls()
            draftpolls_mnu(c, draftpolls, page)

    if 'addchoise_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            tmp_pollid(user_id, pollid)
            pollinfo = get_poll_info(pollid)
            if pollinfo:
                pollname = pollinfo[0]
            else:
                pollname = ru.get('error_poll_not_found')
            mes_text = ru.get('admin_adding_poll_choise').format(
                pollid=pollid,
                pollname=pollname)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, make_poll_choises)

    if 'poll-' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            temp_del(user_id)
            pollid = int(c.data.split('-')[1])
            pollmnu(pollid, c)

    if 'textedit_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            temp_del(user_id)
            tmp_pollid(user_id, pollid)
            pollinfo = get_poll_info(pollid)
            if pollinfo:
                pollname = pollinfo[0]
                polltext = pollinfo[1]
            else:
                pollname = ru.get('error_poll_not_found')
            mes_text = ru.get('admin_edit_poll_text').format(
                pollid=pollid,
                pollname=pollname,
                polltext=polltext)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, edit_poll_text)

    if 'adminchoise_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            poll_choiseid = int(c.data.split('_')[2])
            pollchoises = get_poll_info(pollid)[2]
            for choise in pollchoises:
                if choise.get('num') == poll_choiseid:
                    choise_text = choise.get('var')
            mes_text = ru.get('admin_edit_choise').format(
                choise_text=choise_text)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('choise_edit'),
                    callback_data='choiseedit@_' + str(pollid) + '_' + str(poll_choiseid)),
                types.InlineKeyboardButton(
                    text=ru.get('choise_del'),
                    callback_data='choisedel!_' + str(pollid) + '_' + str(poll_choiseid)))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_to_poll'),
                    callback_data='poll-' + str(pollid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'choiseedit@_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            choiseid = int(c.data.split('_')[2])
            poll_choises = get_poll_info(pollid)[2]
            for row in poll_choises:
                if row.get('num') == choiseid:
                    choise = row.get('var')
            make_temp_choiseid(user_id, pollid, choiseid)
            mes_text = ru.get('admin_edit_poll_choise').format(
                choise=choise)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, edit_poll_choise)

    if 'choisedel!_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            poll_choiseid = int(c.data.split('_')[2])
            del_poll_choise(pollid, poll_choiseid)
            ans_text = ru.get('pollchoise_del_text')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            pollmnu(pollid, c)

    if 'editpollname&' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('&')[1])
            pollname = get_poll_info(pollid)[0]
            tmp_pollid(user_id, pollid)
            mes_text = ru.get('edit_pollname_text').format(
                pollname=pollname)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, edit_poll_name)

    if 'copypoll#' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('#')[1])
            pollid = copy_poll(pollid)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            polltext = pollinfo[1]
            mes_text = ru.get('copy_poll_text').format(
                pollname=pollname,
                polltext=polltext)
            pollmnu(pollid, c=c, mes_text=mes_text)

    if 'dellpoll?' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('?')[1])
            pollname = get_poll_info(pollid)[0]
            mes_text = ru.get('del_poll_text').format(
                pollname=pollname)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('yes'),
                    callback_data='delyes?' + str(pollid)),
                types.InlineKeyboardButton(
                    text=ru.get('no'),
                    callback_data='poll-' + str(pollid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'delyes?' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('?')[1])
            pollname = get_poll_info(pollid)[0]
            delpoll_fn(pollid)
            ans_text = ru.get('del_poll_text_done').format(
                pollname=pollname)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            draftpolls = get_draft_polls()
            draftpolls_mnu(c, draftpolls, 1)

    if 'publicpoll_' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('_')[1])
            pollname = get_poll_info(pollid)[0]
            mes_text = ru.get('ask_before_public').format(
                pollname=pollname)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('yes'),
                    callback_data='pub(' + str(pollid)),
                types.InlineKeyboardButton(
                    text=ru.get('no'),
                    callback_data='poll-' + str(pollid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'pub(' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('(')[1])
            poll_sender(pollid)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            polltext = pollinfo[1]
            pollstatus = 'Опубликован, активен'
            mes_text = ru.get('public_poll_details').format(
                pollname=pollname,
                polltext=polltext,
                pollstatus=pollstatus)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('to_draft'),
                    callback_data='draftpolls+1'),
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='pollmenu'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'pollactiveview}' in c.data:
        user_id = c.from_user.id
        pollid = int(c.data.split('}')[1])
        pollactiveview_mnu(user_id, pollid, c=c)

    if 'closepoll{' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('{')[1])
            pollname = get_poll_info(pollid)[0]
            mes_text = ru.get('closepoll_question_text').format(
                pollname=pollname)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('yes'),
                    callback_data='yclose{' + str(pollid)),
                types.InlineKeyboardButton(
                    text=ru.get('no'),
                    callback_data='pollactiveview}' + str(pollid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'yclose{' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('{')[1])
            pollname = get_poll_info(pollid)[0]
            close_poll(pollid)
            ans_text = ru.get('close_poll_done_text').format(
                pollid=pollid,
                pollname=pollname)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            activepolls = get_open_polls()
            if len(activepolls) > 0:
                active_polls_mnu(c, activepolls)
            else:
                m_polls(c=c)

    if 'xlsexport}' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('}')[1])
            wherefrom = c.data.split('}')[2]
            pollname = get_poll_info(pollid)[0]
            create_stata_file(pollid)
            report = open('stata/' + str(pollid) + '_poll.xlsx', 'rb')
            mes_text = ru.get('export_poll_stata_text').format(
                pollid=pollid,
                pollname=pollname)
            keyboard = types.InlineKeyboardMarkup()
            if wherefrom == 'a':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_to_poll'),
                        callback_data='pollactiveview}' + str(pollid)))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_active'),
                        callback_data='activepolls'),
                    types.InlineKeyboardButton(
                        text=ru.get('back'),
                        callback_data='pollmenu'))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_to_poll'),
                        callback_data='archpoll|' + str(pollid)))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_arch'),
                        callback_data='pollarch<1'),
                    types.InlineKeyboardButton(
                        text=ru.get('back'),
                        callback_data='pollmenu'))
            bot.send_document(c.message.chat.id, report)
            bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'pollarch<' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('<')[1])
            archpoll = get_arch_polls()
            archpollspage = paginator(archpoll, page)
            keyboard = types.InlineKeyboardMarkup()
            archivepolls = len(archpoll)
            if archivepolls:
                mes_text = ru.get('arch_polls_menu_text').format(
                    archivepolls=archivepolls)
                for poll in archpollspage:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=poll[1],
                            callback_data='archpoll|' + str(poll[0])))
                if len(archpoll) <= config.pagelimit:
                    pass
                else:
                    chek_next_btn = len(paginator(archpoll, page + 1))
                    if chek_next_btn > 0:
                        if page == 1:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=ru.get('next'),
                                    callback_data='pollarch<' + str(page + 1)))
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=ru.get('back_p'),
                                    callback_data='pollarch<' + str(page - 1)),
                                types.InlineKeyboardButton(
                                    text=ru.get('next'),
                                    callback_data='pollarch<' + str(page + 1)))
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('back_p'),
                                callback_data='pollarch<' + str(page - 1)))
            else:
                mes_text = ru.get('noarch_polls_menu_text')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='pollmenu'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'archpoll|' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('|')[1])
            pollstats = pollstat_sorter(pollid)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            polltext = pollinfo[1]
            publicdate = str(pollstats[1])
            polled_count = pollstats[2]
            stat_mess = pollstats[3]
            mes_text = ru.get('arch_poll_details').format(
                pollname=pollname,
                publicdate=publicdate,
                polled_count=polled_count,
                polltext=polltext,
                pollstat=stat_mess)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('poll_detail_userchoise'),
                    callback_data='pduserchoise>' + str(pollid) + '>h'))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('copy_poll'),
                    callback_data='copypoll#' + str(pollid)),
                types.InlineKeyboardButton(
                    text=ru.get('export_poll_stata'),
                    callback_data='xlsexport}' + str(pollid) + '}h'))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_arch'),
                    callback_data='pollarch<1'),
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='pollmenu'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'pduserchoise>' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('>')[1])
            wherefrom = c.data.split('>')[2]
            pollstats = pollstat_sorter(pollid)
            pollinfo = get_poll_info(pollid)
            pollname = pollinfo[0]
            publicdate = str(pollstats[1])
            polled_count = pollstats[2]
            polldetailtxt = get_poll_user_choise(pollid)
            mes_text = ru.get('polldetail_userchoise_text').format(
                pollname=pollname,
                publicdate=publicdate,
                polled_count=polled_count,
                pollstat=polldetailtxt)
            keyboard = types.InlineKeyboardMarkup()
            if wherefrom == 'a':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_to_poll'),
                        callback_data='pollactiveview}' + str(pollid)),
                    types.InlineKeyboardButton(
                        text=ru.get('back_active'),
                        callback_data='pollarch<1'))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_to_poll'),
                        callback_data='archpoll|' + str(pollid)),
                    types.InlineKeyboardButton(
                        text=ru.get('back_arch'),
                        callback_data='pollarch<1'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'usrcvar!' in c.data:
        user_id = c.from_user.id
        pollid = int(c.data.split('!')[1])
        choise = int(c.data.split('!')[2])
        interviewed = user_info(user_id)[5]
        if chek_user_polled(user_id, pollid):
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
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('reload'),
                    callback_data='pollactiveview}' + str(pollid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            if interviewed:
                tmp_user_choised(user_id, pollid, choise)
                mes_text = ru.get('user_whant_to_poll_but_password')
                msg = bot.send_message(
                    c.message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(msg, chek_password)
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
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('reload'),
                        callback_data='pollactiveview}' + str(pollid)))
                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)

    if 'usermsgsend]' in c.data:
        user_id = c.from_user.id
        uid = int(c.data.split(']')[1])
        make_tmp_replay_to(user_id, uid)
        userinfo = user_info(uid)
        if userinfo[1]:
            username = userinfo[1]
        else:
            username = userinfo[0]
        mes_text = ru.get('send_direct_msg_to_user').format(
            uid=uid,
            username=username)
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, send_direct_message)

    if 'replay_msg%' in c.data:
        uid = c.from_user.id
        replay_to_id = int(c.data.split('%')[1])
        make_tmp_replay_to(uid, replay_to_id)
        mes_text = ru.get('replay_user_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, user_send_direct_message)

    if 'role:' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split(':')[1])
            role = user_info(uid)[2]
            statuses = config.statuses
            groupid = user_info(uid)[7]
            if groupid:
                groupname = get_group_info(groupid)[2]
            else:
                groupname = ru.get('user_nogroup')
            mes_text = ru.get('role_menu_text').format(
                role=ru.get(role),
                groupname=groupname)
            keyboard = types.InlineKeyboardMarkup()
            for status in statuses:
                if status == statuses[2]:
                    pass
                else:
                    if role == status:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('role_btn').format(
                                    status=ru.get('role_status_on'),
                                    role=ru.get(status)),
                                callback_data='role_ch:' + str(uid) + ':0'))
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('role_btn').format(
                                    status=ru.get('role_status_off'),
                                    role=ru.get(status)),
                                callback_data='role_ch:' + str(uid) + ':' + status))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_to_profile'),
                    callback_data='userprofile$' + str(uid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'role_ch:' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split(':')[1])
            role = c.data.split(':')[2]
            keyboard = types.InlineKeyboardMarkup()
            old_user_role = user_info(uid)[2]
            username = user_info(uid)
            if username[1]:
                username = username[1]
            else:
                username = username[0]
            statuses = config.statuses
            if role == '0':
                role = user_info(uid)[2]
                mes_text = ru.get('role_menu_text_edit').format(
                    role=ru.get(role))
            else:
                if role == statuses[0]:
                    if old_user_role == statuses[1]:
                        remove_user_from_group(uid)
                    if old_user_role == statuses[2]:
                        groupid = get_groupid_from_admin(uid)
                        del_group(groupid)
                    if old_user_role == statuses[3]:
                        remove_admin(uid)
                        remove_from_admin_alert(uid)
                        ans_text = ru.get('usr_remove_bot_admin').format(
                            uid=uid,
                            username=username)
                        bot.answer_callback_query(
                            c.id,
                            text=ans_text,
                            show_alert=True)
                    role = change_user_status(uid, role)
                if role == statuses[1]:
                    if old_user_role == statuses[2]:
                        groupid = get_groupid_from_admin(uid)
                        del_group(groupid)
                    if old_user_role == statuses[3]:
                        remove_admin(uid)
                        remove_from_admin_alert(uid)
                        ans_text = ru.get('usr_remove_bot_admin').format(
                            uid=uid,
                            username=username)
                        bot.answer_callback_query(
                            c.id,
                            text=ans_text,
                            show_alert=True)
                    role = change_user_status(uid, role)
                if role == statuses[3]:
                    make_admin(uid)
                    admin_alert(uid)
                    ans_text = ru.get('usr_bot_admin').format(
                        uid=uid,
                        username=username)
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    role = change_user_status(uid, role)
            for status in statuses:
                if status == statuses[2]:
                    pass
                else:
                    if role == status:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('role_btn').format(
                                    status=ru.get('role_status_on'),
                                    role=ru.get(status)),
                                callback_data='role_ch:' + str(uid) + ':0'))
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('role_btn').format(
                                    status=ru.get('role_status_off'),
                                    role=ru.get(status)),
                                callback_data='role_ch:' + str(uid) + ':' + status))
            mes_text = ru.get('role_menu_text_edit').format(
                role=ru.get(role))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back_to_profile'),
                    callback_data='userprofile$' + str(uid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'add_group_and_set_admin*' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('*')[1])
            make_tmp_uid(user_id, uid)
            mes_text = ru.get('add_group_name_text')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, add_group_and_make_admin)

    if 'group_set_admin~' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('~')[1])
            groupid = int(c.data.split('~')[2])
            change_group_admin(uid, groupid)
            change_user_status(uid, config.statuses[2])
            add_to_group(groupid, uid)
            groupname = get_group_info(groupid)[2]
            ans_text = ru.get('admin_added_to_group_alert').format(
                groupname=groupname)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            group_mnu(groupid, c=c)

    if 'usergproups.' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            page = int(c.data.split('.')[1])
            groups = get_groups(admin=2)
            all_groups_mnu(c, groups, page)

    if 'group-' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split('-')[1])
            group_mnu(groupid, c=c)

    if 'change_group_admin;' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split(';')[1])
            page = int(c.data.split(';')[2])
            add_group_admin_mnu(c, groupid, page)

    if 'users_ingroup_+1' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split('+')[2])
            page = int(c.data.split('+')[1])
            group_users(groupid, page, c=c)

    if 'remove_from_group*' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('*')[1])
            groupid = int(c.data.split('*')[2])
            userisadmin = user_info(uid)[2]
            if userisadmin != config.statuses[2]:
                remove_user_from_group(uid)
                ans_text = ru.get('user_is_removed_from_group')
            else:
                ans_text = ru.get('user_is_admin')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            group_users(groupid, 1, c=c)

    if 'add_user_to_group=' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            cdata = c.data.split('=')[1]
            page = int(cdata.split('+')[0])
            groupid = int(cdata.split('+')[1])
            no_group_users(groupid, page, c=c)

    if 'group_useradd>*' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            uid = int(c.data.split('>*')[1])
            groupid = int(c.data.split('>*')[2])
            groupname = get_group_info(groupid)[2]
            ans_text = ru.get('user_is_adde_to_group').format(
                groupname=groupname)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            add_to_group(groupid, uid)
            no_group_users(groupid, 1, c=c)

    if 'del_group!@' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split('!@')[1])
            groupname = get_group_info(groupid)[2]
            mes_text = ru.get('ask_for_del_group_text').format(
                groupname=groupname)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('yes'),
                    callback_data='group_del|<' + str(groupid)),
                types.InlineKeyboardButton(
                    text=ru.get('no'),
                    callback_data='group-' + str(groupid)))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)

    if 'group_del|<' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split('|<')[1])
            groupname = get_group_info(groupid)[2]
            del_group(groupid)
            ans_text = ru.get('yes_del_group_text').format(
                groupname=groupname)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            groups = get_groups(admin=2)
            all_groups_mnu(c, groups, 1)

    if 'rename_group&' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            groupid = int(c.data.split('&')[1])
            tmp_groupid(user_id, groupid)
            mes_text = ru.get('add_group_name_text')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, edit_group_name)

    if 'админ_голосует-' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            keyboard = types.InlineKeyboardMarkup()
            pollid = int(c.data.split('-')[1])
            if chek_user_polled(user_id, pollid):
                ans_text = ru.get('poll_is_polled_by_user')
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                pollactiveview_mnu(user_id, pollid, c=c)
            else:
                date = Basedate().date_hms()
                pollinfo = get_poll_info(pollid)
                pollname = pollinfo[0]
                polltext = pollinfo[1]
                choises = pollinfo[2]
                mes_text = ru.get('poll_whith_choises').format(
                    pollid=pollid,
                    date=date,
                    pollname=pollname,
                    polltext=polltext)
                for choise in choises:
                    choise_name = choise.get('var')
                    choise_num = choise.get('num')
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=choise_name,
                            callback_data='вариантадмина!' + str(pollid) + '!' + str(choise_num)))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_to_poll'),
                        callback_data='pollactiveview}' + str(pollid)))
                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)

    if 'вариантадмина!' in c.data:
        user_id = c.from_user.id
        if user_id in config.admin or chk_admin(user_id):
            pollid = int(c.data.split('!')[1])
            choise = int(c.data.split('!')[2])
            user_select_choise(user_id, pollid, choise)
            choises = get_poll_info(pollid)[2]
            variant = ru.get('nofind')
            for var in choises:
                if var.get('num') == choise:
                    variant = var.get('var')
            ans_text = ru.get('admin_polled_in_poll').format(
                variant=variant)
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            pollactiveview_mnu(user_id, pollid, c=c)

    if c.data == 'настройки':
        m_user_settings(c=c)

    if c.data == 'информация':
        m_user_info(c=c)


###################################################

bot.remove_webhook()

bot.set_webhook(
    url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
