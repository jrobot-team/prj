# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utilites import (Basedate, append_user_seen_cat, cat_info,
                          chek_user_seen_cat, chk_admin,
                          get_active_chats_in_cat, get_arch_chat_for_user,
                          get_chat_cats, get_chat_counts, get_chat_info,
                          get_chat_user_count, get_chats, get_chats_in_cat,
                          get_group_info, get_group_users, get_no_cats_chats,
                          get_noadmin_users, get_poll_info, pollstat_sorter,
                          remove_user_seen_cat, user_info,
                          users_seen_cat_usernames)
from lang import ru
from paginators import paginator

bot = telebot.TeleBot(config.token)


def pollmnu(pollid, c=False, message=False, mes_text=False):
    pollinfo = get_poll_info(pollid)
    if pollinfo:
        pollname = pollinfo[0]
        polltext = pollinfo[1]
        choises = pollinfo[2]
        if mes_text is False:
            doc_name = pollinfo[7]
            if doc_name:
                pass
            else:
                doc_name = ru.get('no_doc')
            mes_text = ru.get('poll_details').format(
                pollname=pollname,
                polltext=polltext,
                doc_name=doc_name)
        keyboard = types.InlineKeyboardMarkup()
        for choise in choises:
            choise_name = choise.get('var')
            choise_num = choise.get('num')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=choise_name,
                    callback_data='adminchoise_' + str(pollid) + '_' + str(choise_num)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('public_poll_btn'),
                callback_data='publicpoll_' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('edit_poll_name'),
                callback_data='editpollname&' + str(pollid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('addchoise_btn'),
                callback_data='addchoise_' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('poll_text_edit'),
                callback_data='textedit_' + str(pollid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('copy_poll'),
                callback_data='copypoll#' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('delpoll_btn'),
                callback_data='dellpoll?' + str(pollid)))
        if pollinfo[6]:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('edit_doc_btn'),
                    callback_data='добавитьдок-' + str(pollid)
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('add_doc_btn'),
                    callback_data='добавитьдок-' + str(pollid)
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('to_draft'),
                callback_data='draftpolls+1'),
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='pollmenu'))
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
    else:
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


def active_polls_mnu(c, activepolls):
    keyboard = types.InlineKeyboardMarkup()
    if activepolls:
        mes_text = ru.get('active_polls_menu_text').format(
            activepolls=len(activepolls))
        for poll in activepolls:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=poll[1],
                    callback_data='pollactiveview}' + str(poll[0])))
    else:
        mes_text = ru.get('no_active_polls_menu_text')
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


def done_mnu(message):
    done_text = ru.get('done_text')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(ru.get('users_menu_btn')),
        types.KeyboardButton(ru.get('polls')))
    bot.send_message(
        message.chat.id,
        text=done_text,
        parse_mode='html',
        reply_markup=keyboard)


def candidate_mnu(c, users, page):
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('candidate_menu_text')
        for user in userspage:
            if user[2]:
                username = user[2]
            else:
                username = user[1]
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('userprofile_btn').format(
                        uid=user[0],
                        username=username),
                    callback_data='userprofile$' + str(user[0])))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='candidate*' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='candidate*' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='candidate*' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='candidate*' + str(page - 1)))
    else:
        mes_text = ru.get('nocandidate_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='usersadmin'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def users_mnu(c, users, page):
    user_id = c.from_user.id
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('users_menu_text')
        for user in userspage:
            if user[0] != user_id:
                if user[2]:
                    username = user[2]
                else:
                    username = user[1]
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('userprofile_btn').format(
                            uid=user[0],
                            username=username),
                        callback_data='userprofile$' + str(user[0])))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='users^' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='users^' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='users^' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='users^' + str(page - 1)
                    )
                )
    else:
        mes_text = ru.get('nousers_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('export_btn'),
            callback_data='экспортировать'
        ),
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='usersadmin'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def userprofile_mnu(uid, message=False, c=False):
    userinfo = user_info(uid)
    username = userinfo[0]
    fio = userinfo[1]
    role = userinfo[2]
    if userinfo[5]:
        interviewed = ru.get('sm_yes')
    else:
        interviewed = ru.get('sm_no')
    pollcount = userinfo[3]
    if userinfo[6]:
        userpwd = ru.get('userpwd_on')
    else:
        userpwd = ru.get('userpwd_off')
    keyboard = types.InlineKeyboardMarkup()
    if userinfo[4]:
        groupid = userinfo[7]
        if groupid:
            groupname = get_group_info(groupid)[2]
        else:
            groupname = ru.get('user_nogroup')
        mes_text = ru.get('user_detailmenu_text').format(
            uid=uid,
            username=username,
            fio=fio,
            role=ru.get(role),
            groupname=groupname,
            interviewed=interviewed,
            pollcount=pollcount,
            userpwd=userpwd)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('role_mnu_btn'),
                callback_data='role:' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('deactivate_user'),
                callback_data='change_activation]0]' + str(uid)),
            types.InlineKeyboardButton(
                text=ru.get('reset_pwd'),
                callback_data='resetuserpwd]' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('change_fio'),
                callback_data='changefio]' + str(uid)),
            types.InlineKeyboardButton(
                text=ru.get('send_message'),
                callback_data='usermsgsend]' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_to_users'),
                callback_data='users^1'),
            types.InlineKeyboardButton(
                text=ru.get('choise_del'),
                callback_data='ак_удалитьп_ля-' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='usersadmin'))
    else:
        mes_text = ru.get('candidate_detailmenu_text').format(
            uid=uid,
            username=username,
            fio=fio,
            userpwd=userpwd)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('activate_candidate'),
                callback_data='change_activation]1]' + str(uid)),
            types.InlineKeyboardButton(
                text=ru.get('reset_pwd'),
                callback_data='resetuserpwd]' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('change_fio'),
                callback_data='changefio]' + str(uid)),
            types.InlineKeyboardButton(
                text=ru.get('send_message'),
                callback_data='usermsgsend]' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_to_users'),
                callback_data='candidate*1'),
            types.InlineKeyboardButton(
                text=ru.get('choise_del'),
                callback_data='удалитьканд_та-' + str(uid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='usersadmin'))
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


def draftpolls_mnu(c, draftpolls, page):
    pollspage = paginator(draftpolls, page)
    keyboard = types.InlineKeyboardMarkup()
    if len(draftpolls) > 0:
        mes_text = ru.get('admin_drafts_menu')
        for poll in pollspage:
            pollid = poll[0]
            pollname = poll[1]
            keyboard.add(
                types.InlineKeyboardButton(
                    text=pollname,
                    callback_data='poll-' + str(pollid)))
        if len(draftpolls) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(draftpolls, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='draftpolls+' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='draftpolls+' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='draftpolls+' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='draftpolls+' + str(page - 1)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='pollmenu'))
    else:
        mes_text = ru.get('admin_drafts_menu_no_drafts')
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


def group_mnu(groupid, message=False, c=False):
    groupinfo = get_group_info(groupid)
    user_count = len(get_group_users(groupid))
    uid = groupinfo[1]
    groupname = groupinfo[2]
    if uid:
        admin_name = user_info(uid)
        if admin_name[1]:
            admin_name = admin_name[1]
        else:
            admin_name = admin_name[0]
        mes_text = ru.get('group_detail_menu_text').format(
            groupname=groupname,
            user_count=user_count,
            uid=uid,
            admin_name=admin_name)
    else:
        mes_text = ru.get('group_added_text').format(
            groupname=groupname,
            user_count=user_count)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('change_group_admin_btn'),
            callback_data='change_group_admin;' + str(groupid) + str(';1')),
        types.InlineKeyboardButton(
            text=ru.get('edit_poll_name'),
            callback_data='rename_group&' + str(groupid)))
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('in_group_user_view'),
            callback_data='users_ingroup_+1+' + str(groupid)),
        types.InlineKeyboardButton(
            text=ru.get('choise_del'),
            callback_data='del_group!@' + str(groupid)))
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='usersadmin'),
        types.InlineKeyboardButton(
            text=ru.get('back_to_groups'),
            callback_data='usergproups.1'))
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


def all_groups_mnu(c, groups, page):
    grouppage = paginator(groups, page)
    keyboard = types.InlineKeyboardMarkup()
    if len(groups) > 0:
        mes_text = ru.get('groups_menu_text')
        for group in grouppage:
            admin_true = get_group_info(group[0])[1]
            if admin_true:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=group[2],
                        callback_data='group-' + str(group[0])))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='* ' + group[2],
                        callback_data='group-' + str(group[0])))
        if len(groups) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(groups, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='usergproups.' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='usergproups.' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='usergproups.' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='usergproups.' + str(page - 1)))
    else:
        mes_text = ru.get('nogroups_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('add_group_btn'),
            callback_data='add_group+1'),
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='usersadmin'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def add_group_admin_mnu(c, groupid, page):
    users = get_noadmin_users()
    user_count = len(get_group_users(groupid))
    groupname = get_group_info(groupid)[2]
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('group_add_admin_to_group_text').format(
            groupname=groupname,
            user_count=user_count)
        for user in userspage:
            if user[1]:
                username = user[1]
            else:
                username = user[0]
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('userprofile_btn').format(
                        uid=user[7],
                        username=username),
                    callback_data='group_set_admin~' + str(user[7]) + '~' + str(groupid)))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='change_group_admin;' + str(groupid) + ';' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='change_group_admin;' + str(groupid) + ';' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='change_group_admin;' + str(groupid) + ';' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='change_group_admin;' + str(groupid) + ';' + str(page - 1)))
    else:
        mes_text = ru.get('nousers_group_add_admin_to_group_text').format(
            groupname=groupname,
            user_count=user_count)
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_to_group'),
            callback_data='group-' + str(groupid)))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def add_admin_and_make_group_mnu(c, page):
    users = get_noadmin_users()
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('new_group_add_admin_to_group_text')
        for user in userspage:
            if user[1]:
                username = user[1]
            else:
                username = user[0]
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('userprofile_btn').format(
                        uid=user[7],
                        username=username),
                    callback_data='add_group_and_set_admin*' + str(user[7])))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='add_group+' + str(page + 1)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='add_group+' + str(page - 1)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='add_group+' + str(page + 1)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='add_group+' + str(page - 1)))
    else:
        mes_text = ru.get('nousers_new_group_add_admin_to_group_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_to_groups'),
            callback_data='usergproups.1'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def group_users(groupid, page, c=False, message=False):
    users = get_group_users(groupid)
    user_count = len(users)
    groupname = get_group_info(groupid)[2]
    groupadmin = get_group_info(groupid)[1]
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('group_users_text').format(
            groupname=groupname,
            user_count=user_count)
        for user in userspage:
            uid = user[7]
            if user[1]:
                username = user[1]
            else:
                username = user[0]
            if uid == groupadmin:
                uid = ru.get('admin_user')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('userprofile_btn').format(
                        uid=uid,
                        username=username),
                    callback_data='remove_from_group*' + str(user[7]) + '*' + str(groupid)))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='users_ingroup_+' + str(page + 1) + '+' + str(groupid)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='users_ingroup_+' + str(page - 1) + '+' + str(groupid)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='users_ingroup_+' + str(page + 1) + '+' + str(groupid)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='users_ingroup_+' + str(page - 1) + '+' + str(groupid)))
    else:
        mes_text = ru.get('group_nousers_text').format(
            groupname=groupname,
            user_count=user_count)
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('user_add_to_group_btn'),
            callback_data='add_user_to_group=1' + '+' + str(groupid)),
        types.InlineKeyboardButton(
            text=ru.get('back_to_group'),
            callback_data='group-' + str(groupid)))
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


def no_group_users(groupid, page, c=False, message=False):
    users = get_group_users(0)
    user_count = len(get_group_users(groupid))
    groupname = get_group_info(groupid)[2]
    groupadmin = get_group_info(groupid)[1]
    admin_name = user_info(groupadmin)
    if admin_name:
        if admin_name[1]:
            admin_name = admin_name[1]
        else:
            admin_name = admin_name[0]
    else:
        admin_name = ru.get('noadmin')
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        mes_text = ru.get('group_add_user_text').format(
            groupname=groupname,
            user_count=user_count,
            uid=groupadmin,
            admin_name=admin_name)
        for user in userspage:
            uid = user[7]
            if user[1]:
                username = user[1]
            else:
                username = user[0]
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('userprofile_btn').format(
                        uid=uid,
                        username=username),
                    callback_data='group_useradd>*' + str(user[7]) + '>*' + str(groupid)))
        if len(users) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(users, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='add_user_to_group=' + str(page + 1) + '+' + str(groupid)))
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='add_user_to_group=' + str(page - 1) + '+' + str(groupid)),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='add_user_to_group=' + str(page + 1) + '+' + str(groupid)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='add_user_to_group=' + str(page - 1) + '+' + str(groupid)))
    else:
        mes_text = ru.get('group_add_nousers_text').format(
            groupname=groupname,
            user_count=user_count,
            uid=groupadmin,
            admin_name=admin_name)
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_to_group'),
            callback_data='group-' + str(groupid)))
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


def pollactiveview_mnu(user_id, pollid, c=False, message=False):
    date = Basedate().date_hms()
    pollstats = pollstat_sorter(pollid)
    pollinfo = get_poll_info(pollid)
    pollname = pollinfo[0]
    polltext = pollinfo[1]
    publicdate = str(pollstats[1])
    polled_count = pollstats[2]
    stat_mess = pollstats[3]
    mes_text = ru.get('active_poll_details').format(
        pollname=pollname,
        publicdate=publicdate,
        polled_count=polled_count,
        polltext=polltext,
        pollstat=stat_mess,
        date=date)
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin or chk_admin(user_id):
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('admin_whant_poll'),
                callback_data='админ_голосует-' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('poll_detail_userchoise'),
                callback_data='pduserchoise>' + str(pollid) + '>a'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('close_poll'),
                callback_data='closepoll{' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('reload'),
                callback_data='pollactiveview}' + str(pollid)))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('copy_poll'),
                callback_data='copypoll#' + str(pollid)),
            types.InlineKeyboardButton(
                text=ru.get('export_poll_stata'),
                callback_data='xlsexport}' + str(pollid) + '}a'))
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
                text=ru.get('reload'),
                callback_data='pollactiveview}' + str(pollid)))
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


def su_admin_mnu(message=False, c=False):
    mes_text = ru.get('admin_menu')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('candidate_menu_btn'),
            callback_data='candidate*1'),
        types.InlineKeyboardButton(
            text=ru.get('users_menu_btn'),
            callback_data='users^1'))
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('user_groups_menu_btn'),
            callback_data='usergproups.1'))
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


def active_chat(c):
    active_chats = get_chats(status='active')
    mes_text = ru.get('active_chat_menu_text').format(
        active_chats=len(active_chats)
    )
    keyboard = types.InlineKeyboardMarkup()
    categories = get_chat_cats()
    if len(categories):
        for cat in categories:
            active_count = len(get_active_chats_in_cat(cat.get('id')))
            if active_count > 0:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('category_and_count_active_chats').format(
                            catname=cat.get('catname'),
                            active_count=active_count
                        ),
                        callback_data='active_cat-' + str(cat.get('id'))
                    )
                )
    keyboard.add(
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


def arch_chat(c):
    mes_text = ru.get('user_arch_chat_menu_text')
    cats = get_chat_cats()
    no_cats_chats = get_no_cats_chats()
    keyboard = types.InlineKeyboardMarkup()
    if cats:
        for cat in cats:
            arch_chats = get_arch_chat_for_user(cat.get('id'))
            if arch_chats:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=cat.get('catname'),
                        callback_data='archcatsee-' + str(cat.get('id'))
                    )
                )
    if no_cats_chats:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('no_cat_chats_btn'),
                callback_data='archcatsee-0'
            )
        )
    arch_chats = get_chats(status='arch')
    mes_text = ru.get('arch_chat_menu_text').format(
        arch_chats=len(arch_chats)
    )
    keyboard.add(
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


def wait_chat(c):
    wait_chats = get_chats(status='wait')
    mes_text = ru.get('wait_menu_text').format(
        wait_chats=len(wait_chats)
    )
    keyboard = types.InlineKeyboardMarkup()
    for chat in wait_chats:
        keyboard.add(
            types.InlineKeyboardButton(
                text=chat.get('chat_name'),
                callback_data='обсуждение-' + str(chat.get('chatid'))
            )
        )
    keyboard.add(
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


def chat_detail_menu(c=False, message=False, chatid=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    if chatid is False:
        chatid = int(c.data.split('-')[1])
    chatinfo = get_chat_info(chatid)
    chat_user_count = get_chat_user_count(user_id, chatid)
    if chatinfo.get('status') == 'active':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('view_active_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('active_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('append_to_chat').format(
                    count=get_chat_counts(chatid, user_id) - chat_user_count
                ),
                callback_data='присоединиться-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('stop_chat'),
                callback_data='остановить-' + str(chatid)
            )
        )
        if chatinfo.get('catid'):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                ),
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='категория-' + str(chatinfo.get('catid'))
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
    if chatinfo.get('status') == 'wait':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('wait_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('wait_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('edit_url'),
                    callback_data='редактировать_ссылку-' + str(chatid)
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('delite_chat'),
                callback_data='удалить_-' + str(chatid)
            )
        )
        if chatinfo.get('catid'):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                ),
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='категория-' + str(chatinfo.get('catid'))
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
    if chatinfo.get('status') == 'arch':
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
            )
        )
        if chatinfo.get('catid'):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                ),
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='категория-' + str(chatinfo.get('catid'))
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                )
            )
    if chatinfo.get('status') == 'new':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('view_new_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('view_new_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('edit_url'),
                    callback_data='редактировать_ссылку-' + str(chatid)
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('delite_chat'),
                callback_data='удалить_-' + str(chatid)
            )
        )
        if chatinfo.get('catid'):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
                ),
                types.InlineKeyboardButton(
                    text=ru.get('back_p'),
                    callback_data='категория-' + str(chatinfo.get('catid'))
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('back'),
                    callback_data='чаты'
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


def active_chat_detail_menu(c=False, message=False, chatid=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    if chatid is False:
        chatid = int(c.data.split('-')[1])
    chatinfo = get_chat_info(chatid)
    chat_user_count = get_chat_user_count(user_id, chatid)
    keyboard = types.InlineKeyboardMarkup()
    if chatinfo.get('chat_url') == 'no_url':
        mes_text = ru.get('view_active_chat_menu_text').format(
            date_create=chatinfo.get('date_create'),
            chat_name=chatinfo.get('chat_name'),
            date_start=chatinfo.get('date_start')
        )
    else:
        mes_text = ru.get('active_chat_menu_text_with_url').format(
            date_create=chatinfo.get('date_create'),
            chat_name=chatinfo.get('chat_name'),
            date_start=chatinfo.get('date_start'),
            chat_url=chatinfo.get('chat_url')
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('append_to_chat').format(
                count=get_chat_counts(chatid, user_id) - chat_user_count
            ),
            callback_data='присоединиться-' + str(chatid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('stop_chat'),
            callback_data='остановить-' + str(chatid)
        )
    )
    if chatinfo.get('catid'):
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='чаты'
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='active_cat-' + str(chatinfo.get('catid'))
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back'),
                callback_data='чаты'
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


def arch_chat_detail_menu(c=False, message=False, chatid=False, arch=False):
    if chatid is False:
        chatid = int(c.data.split('-')[1])
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
        ),
        types.InlineKeyboardButton(
            text=ru.get('chat_view_messages'),
            callback_data='архсообщения-' + str(chatid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('delite_chat'),
            callback_data='удалить_-' + str(chatid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='чаты'
        ),
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='архивные_обсуждения'
        )
    )
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        if arch:
            bot.send_message(
                c.message.chat.id,
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


def cats_menu(message=False, c=False):
    mes_text = ru.get('cats_menu_text')
    keyboard = types.InlineKeyboardMarkup()
    categories = get_chat_cats()
    if len(categories):
        for cat in categories:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=cat.get('catname'),
                    callback_data='категория-' + str(cat.get('id'))
                )
            )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('add_chat_cat'),
            callback_data='добавить_категорию=0'
        ),
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='чаты'
        )
    )
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


def cat_detail_menu(catid, message=False, c=False):
    chats = get_chats_in_cat(catid)
    mes_text = ru.get('view_cat_menu_text').format(
        catname=cat_info(catid).get('catname')
    )
    keyboard = types.InlineKeyboardMarkup()
    for chat in chats:
        if chat.get('status') != 'arch':
            keyboard.add(
                types.InlineKeyboardButton(
                    text=chat.get('chatname'),
                    callback_data='обсуждение-' + str(chat.get('id'))
                )
            )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('add_chat_cat_btn'),
            callback_data='новобсвк-' + str(catid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('edit_cat_name_btn'),
            callback_data='кат_изменить_название-' + str(catid)
        ),
        types.InlineKeyboardButton(
            text=ru.get('delite_chat'),
            callback_data='удалить_кат-' + str(catid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('access'),
            callback_data='доступ-' + str(catid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='чаты'
        ),
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='категории_обсуждений'
        )
    )
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


def active_cat_detail_menu(catid, message=False, c=False):
    chats = get_chats_in_cat(catid, status='active')
    mes_text = ru.get('view_cat_menu_text').format(
        catname=cat_info(catid).get('catname')
    )
    keyboard = types.InlineKeyboardMarkup()
    for chat in chats:
        keyboard.add(
            types.InlineKeyboardButton(
                text=chat.get('chatname'),
                callback_data='activech-' + str(chat.get('id'))
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('add_chat_cat_btn'),
            callback_data='новобсвк-' + str(catid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('edit_cat_name_btn'),
            callback_data='кат_изменить_название-' + str(catid)
        ),
        types.InlineKeyboardButton(
            text=ru.get('delite_chat'),
            callback_data='удалить_кат-' + str(catid)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back'),
            callback_data='чаты'
        ),
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='активные_обсуждения'
        )
    )
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


def cat_detail_user_menu(catid, message=False, c=False):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    chats = get_chats_in_cat(catid)
    mes_text = ru.get('view_cat_menu_text').format(
        catname=cat_info(catid).get('catname')
    )
    keyboard = types.InlineKeyboardMarkup()
    for chat in chats:
        chat_user_count = get_chat_user_count(user_id, chat.get('id'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('chat_in_cat_btn').format(
                    chatname=chat.get('chatname'),
                    count=get_chat_counts(chat.get('id'), user_id) - chat_user_count
                ),
                callback_data='присоединиться-' + str(chat.get('id'))
            )
        )
    if user_info(user_id)[5]:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('add_chat_cat_btn'),
                callback_data='новобсвк-' + str(catid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('view_users_access'),
                callback_data='accessview=' + str(catid)
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='п_обсуждения'
        )
    )
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


def chat_detail_user_menu(c=False, message=False, chatid=False):
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    if chatid is False:
        chatid = int(c.data.split('-')[1])
    chatinfo = get_chat_info(chatid)
    chat_user_count = get_chat_user_count(user_id, chatid)
    if chatinfo.get('status') == 'active':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('view_active_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('active_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('append_to_chat').format(
                    count=get_chat_counts(chatid, user_id) - chat_user_count
                ),
                callback_data='присоединиться-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='катюз-' + str(chatinfo.get('catid'))
            )
        )
    if chatinfo.get('status') == 'wait':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('wait_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('wait_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='катюз-' + str(chatinfo.get('catid'))
            )
        )
    if chatinfo.get('status') == 'arch':
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
                text=ru.get('back_p'),
                callback_data='катюз-' + str(chatinfo.get('catid'))
            )
        )
    if chatinfo.get('status') == 'new':
        keyboard = types.InlineKeyboardMarkup()
        if chatinfo.get('chat_url') == 'no_url':
            mes_text = ru.get('view_new_chat_menu_text').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start')
            )
        else:
            mes_text = ru.get('view_new_chat_menu_text_with_url').format(
                date_create=chatinfo.get('date_create'),
                chat_name=chatinfo.get('chat_name'),
                date_start=chatinfo.get('date_start'),
                chat_url=chatinfo.get('chat_url')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('edit_url'),
                    callback_data='редактировать_ссылку-' + str(chatid)
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('start_chat'),
                callback_data='стартовать_-' + str(chatid)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='катюз-' + str(chatinfo.get('catid'))
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


def arch_chat_user_menu(c):
    mes_text = ru.get('user_arch_chat_menu_text')
    cats = get_chat_cats()
    no_cats_chats = get_no_cats_chats()
    keyboard = types.InlineKeyboardMarkup()
    if cats:
        for cat in cats:
            arch_chats = get_arch_chat_for_user(cat.get('id'))
            if arch_chats:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=cat.get('catname'),
                        callback_data='archcatsee-' + str(cat.get('id'))
                    )
                )
    if no_cats_chats:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('no_cat_chats_btn'),
                callback_data='archcatsee-0'
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='п_обсуждения'
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def arch_cat_detail_user_menu(catid, message=False, c=False):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    chats = get_arch_chat_for_user(catid)
    catname = cat_info(catid).get('catname')
    if catname == 'Архив':
        catname = 'Без категории'
    mes_text = ru.get('view_arch_cat_menu_text').format(
        catname=catname
    )
    keyboard = types.InlineKeyboardMarkup()
    if catname == 'Без категории':
        chats = get_no_cats_chats()
    for chat in chats:
        keyboard.add(
            types.InlineKeyboardButton(
                text=chat.get('chat_name'),
                callback_data='архсообщенияюз-' + str(chat.get('id'))
            )
        )
    if user_id in config.admin or chk_admin(user_id):
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='архивные_обсуждения'
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='archchatuser'
            )
        )
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


def arch_chat_detail_user_menu(c=False, message=False, chatid=False, arch=False):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    if chatid is False:
        chatid = int(c.data.split('-')[1])
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
    if user_id in config.admin or chk_admin(user_id):
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('chat_view_messages'),
                callback_data='архсообщенияюз-' + str(chatid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('get_message_arch_btn'),
                callback_data='выгрузить-' + str(chatid)
            ),
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='archcatsee-' + str(chatinfo.get('catid'))
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='archcatsee-' + str(chatinfo.get('catid'))
            )
        )
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        if arch:
            bot.send_message(
                c.message.chat.id,
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


def access_menu(c, catid):
    user_id = c.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin or chk_admin(user_id):
        mes_text = ru.get('access_menu_text_admin').format(
            catname=cat_info(catid).get('catname')
        )
        call = str(catid) + '=1=0=0=0'
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('add_users_access'),
                callback_data='accessaddusr=' + call
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('view_users_access'),
                callback_data='accessview=' + str(catid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='категория-' + str(catid)
            )
        )
    else:
        mes_text = ru.get('access_menu_text_admin')
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('view_users_access'),
                callback_data='accessview=' + str(catid)
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='катюз-' + str(catid)
            )
        )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def view_access_to_cat(c, catid):
    user_id = c.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    mes_text = ru.get('view_access_text').format(
        catname=cat_info(catid).get('catname'),
        users=users_seen_cat_usernames(catid)
    )
    if user_id in config.admin or chk_admin(user_id):
        call = str(catid) + '=1=0=0=0'
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('add_users_access'),
                callback_data='accessaddusr=' + call
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='доступ-' + str(catid)
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='катюз-' + str(catid)
            )
        )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def access_users_mnu(c, catid, users, page, uid, state, chk):
    if chk:
        chk = '0'
    else:
        chk = '1'
    if uid:
        if int(state):
            append_user_seen_cat(uid, catid)
        else:
            remove_user_seen_cat(uid, catid)
    user_id = c.from_user.id
    userspage = paginator(users, page)
    keyboard = types.InlineKeyboardMarkup()
    if users:
        for user in userspage:
            if user[0] != user_id:
                if user[2]:
                    username = user[2]
                else:
                    username = user[1]
                ustate = chek_user_seen_cat(user[0], catid)
                if ustate:
                    call = str(catid) + '=' + str(page) + '=' + str(user[0]) + '=0=' + str(chk)
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('userprofile_btn_appended').format(
                                username=username),
                            callback_data='accessaddusr=' + call
                        )
                    )
                else:
                    call = str(catid) + '=' + str(page) + '=' + str(user[0]) + '=1=' + str(chk)
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('userprofile_btn_notappended').format(
                                username=username),
                            callback_data='accessaddusr=' + call
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
                            callback_data='accessaddusr=' + str(catid) + '=' + str(page + 1) + '=0=0=' + str(chk)
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back_p'),
                            callback_data='accessaddusr=' + str(catid) + '=' + str(page - 1) + '=0=0=' + str(chk)
                        ),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='accessaddusr=' + str(catid) + '=' + str(page + 1) + '=0=0=' + str(chk)
                        )
                    )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back_p'),
                        callback_data='accessaddusr=' + str(catid) + '=' + str(page - 1) + '=0=0=' + str(chk)
                    )
                )
        if chk:
            mes_text = ru.get('user_access_add_remove_menu_chk').format(
                catname=cat_info(catid).get('catname')
            )
        else:
            mes_text = ru.get('user_access_add_remove_menu').format(
                catname=cat_info(catid).get('catname')
            )
    else:
        mes_text = ru.get('nousers_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_to_cat'),
            callback_data='доступ-' + str(catid)))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
