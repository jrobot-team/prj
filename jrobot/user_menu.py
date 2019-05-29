# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utils import date_revers, btn
from lng_fn import lng
from paginators import paginator
from users_utils import (get_all_groups, get_all_users, get_group_info_by_id,
                         get_group_info_by_owner, get_owner_group_users,
                         get_refer_users, get_user_info, get_user_status,
                         is_user_in_group, is_user_owner, isuser,
                         put_user_to_group, reg_user, remove_user_from_group,
                         update_user_status, username_getter)

# telegram bot api
bot = telebot.TeleBot(config.token)


def users_view(message=None, c=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        users = get_all_users()
        groups = get_all_groups()
        mes_text = lng(user_id).get('admin_users_view_text').format(
            count=len(users),
            groups=len(groups)
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('users_mnu_btn'),
                callback_data='viewallusers+1'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('groups_view_btn'),
                callback_data='viewallgroups'
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('add_user_to_refer'),
                callback_data='adduserrefer'
            )
        )
    else:
        users = get_refer_users(user_id)
        group = get_owner_group_users(user_id)
        mes_text = lng(user_id).get('owner_users_view_text').format(
            count=len(users),
            groups=len(group)
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('users_mnu_btn'),
                callback_data='viewallrefer'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('add_user_to_refer'),
                callback_data='adduserrefer'
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('group_owner_view_btn'),
                callback_data='ownergroupview'
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


def view_users(c, page=1):
    user_id = c.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        users = get_all_users()
    else:
        users = get_refer_users(user_id)
    if users:
        userspage = paginator(users, page)
        mes_text = lng(user_id).get('users_view_menu_text').format(
            count=len(users)
        )
        for user in userspage:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=user.get('name'),
                    callback_data='uprofile-' + str(user.get('user_id'))
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
                            callback_data='viewallusers+' + str(page + 1)
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('back_p'),
                            callback_data='viewallusers+' + str(page - 1)
                        ),
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('next'),
                            callback_data='viewallusers+' + str(page + 1)
                        )
                    )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='viewallusers+' + str(page - 1)
                    )
                )
    else:
        referlink = 'https://t.me/jrobot_demo_bot?start=' + str(user_id)
        mes_text = lng(user_id).get('nousers_view_menu_text').format(
            referlink=referlink
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='usersview'
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def start_user_menu(message=None, c=None, refer_id=None):
    if c:
        user_id = c.from_user.id
        username = username_getter(c=c)
    else:
        user_id = message.from_user.id
        username = username_getter(message=message)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if isuser(user_id):
        userinfo = get_user_info(user_id)
        if userinfo.get('refer_id'):
            refer_name = get_user_info(userinfo.get('refer_id'))
            if refer_name:
                refer_name = refer_name.get('name')
            else:
                refer_name = 'Неопределено'
            group_name = get_group_info_by_owner(userinfo.get('refer_id'))
            if group_name:
                group_name = group_name.get('name')
            else:
                group_name = 'Неопределено'
            if get_user_status(user_id):
                mes_text = lng(user_id).get('hireferaluser_message_text').format(
                    refer_username=refer_name,
                    group_name=group_name
                )
                keyboard.add(
                    btn(lng(user_id).get('learn_mnu_btn'), 'LEARN'),
                    btn(lng(user_id).get('tasks_mnu_btn'), 'TASKS'),
                    btn(lng(user_id).get('polls_mnu_btn'), 'POLLS'),
                    btn(lng(user_id).get('meet_mnu_btn'), 'MEET'),
                    btn(lng(user_id).get('user_group_mnu_btn'), 'GROUP'),
                    btn(lng(user_id).get('settings'), 'SETTINGS'),
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
            else:
                mes_text = lng(user_id).get('hireferaluser_message_text_no_aprowed_acc').format(
                    refer_username=refer_name,
                    group_name=group_name
                )
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('get_learn_mnu_btn'),
                        callback_data='обучение'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('settings'),
                        callback_data='SETTINGS'
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
        else:
            if is_user_owner(user_id):
                mes_text = lng(user_id).get('hiuser_message_text')
                keyboard.add(
                    btn(lng(user_id).get('learn_mnu_btn'), 'LEARN'),
                    btn(lng(user_id).get('tasks_mnu_btn'), 'TASKS'),
                    btn(lng(user_id).get('polls_mnu_btn'), 'POLLS'),
                    btn(lng(user_id).get('meet_mnu_btn'), 'MEET'),
                    btn(lng(user_id).get('user_group_mnu_btn'), 'GROUP'),
                    btn(lng(user_id).get('settings'), 'SETTINGS'),
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
            else:
                mes_text = lng(user_id).get('hiuser_message_text')
                mes_text = mes_text + '\n' + lng(user_id).get('choose_mnu_text')
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('create_group_mnu_btn'),
                        callback_data='группа-1'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('get_learn_mnu_btn'),
                        callback_data='обучение'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('settings'),
                        callback_data='SETTINGS'
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
    else:
        reg_user(user_id, username, refer_id=refer_id)
        if refer_id:
            refer_name = get_user_info(refer_id)
            if refer_name:
                refer_name = refer_name.get('name')
            else:
                refer_name = 'Неопределено'
            group_name = get_group_info_by_owner(refer_id)
            if group_name:
                group_name = group_name.get('name')
            else:
                group_name = 'Неопределено'
            if get_user_status(user_id):
                mes_text = lng(user_id).get('hireferaluser_message_text').format(
                    refer_username=refer_name,
                    group_name=group_name
                )
                mes_text = mes_text + '\n' + lng(user_id).get('choose_mnu_text')
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('get_learn_mnu_btn'),
                        callback_data='обучение'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('settings'),
                        callback_data='SETTINGS'
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
            else:
                mes_text = lng(user_id).get('hireferaluser_message_text_no_aprowed_acc').format(
                    refer_username=refer_name,
                    group_name=group_name
                )
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('get_learn_mnu_btn'),
                        callback_data='обучение'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('settings'),
                        callback_data='SETTINGS'
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
        else:
            mes_text = lng(user_id).get('hiuser_message_text')
            mes_text = mes_text + '\n' + lng(user_id).get('choose_mnu_text')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('create_group_mnu_btn'),
                    callback_data='группа-1'
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('get_learn_mnu_btn'),
                    callback_data='обучение'
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('settings'),
                    callback_data='SETTINGS'
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


def user_group_menu(message=None, c=None, page=1, fr=False):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    group_created = False
    userinfo = get_user_info(user_id)
    keyboard = types.InlineKeyboardMarkup()
    if isuser(user_id):
        if is_user_owner(user_id):
            group_created = True
            refer_link = 'https://t.me/jrobot_demo_bot?start=' + str(user_id)
            groupinfo = get_group_info_by_owner(user_id)
            group_users = get_owner_group_users(user_id)
            ownerinfo = get_user_info(user_id)
            group_users.append(
                {
                    'id': ownerinfo.get('id'),
                    'group_id': groupinfo.get('id'),
                    'user_id': user_id
                }
            )
            if group_users:
                mes_text = lng(user_id).get('user_view_group').format(
                    groupname=groupinfo.get('name'),
                    users_count=len(group_users),
                    refer_link=refer_link
                )
                userspage = paginator(group_users, page)
                for user in userspage:
                    username = get_user_info(user.get('user_id')).get('name')
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=username,
                            callback_data='uprofile-' + str(user.get('user_id'))
                        )
                    )
                if len(group_users) <= config.pagelimit:
                    pass
                else:
                    chek_next_btn = len(paginator(group_users, page + 1))
                    if chek_next_btn > 0:
                        if page == 1:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='группа-' + str(page + 1)
                                )
                            )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='группа-' + str(page - 1)
                                ),
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='группа-' + str(page + 1)
                                )
                            )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('back_p'),
                                callback_data='группа-' + str(page - 1)
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
            else:
                mes_text = lng(user_id).get('user_view_group_no_users').format(
                    groupname=groupinfo.get('name'),
                    refer_link=refer_link
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
        else:
            if is_user_in_group(user_id):
                group_created = True
                group_id = is_user_in_group(user_id)
                groupinfo = get_group_info_by_id(group_id)
                group_users = get_owner_group_users(groupinfo.get('owner_id'))
                ownerinfo = get_user_info(groupinfo.get('owner_id'))
                group_users.append(
                    {
                        'id': ownerinfo.get('id'),
                        'group_id': groupinfo.get('id'),
                        'user_id': ownerinfo.get('user_id')
                    }
                )
                refer_link = 'https://t.me/jrobot_demo_bot?start=' + str(groupinfo.get('owner_id'))
                mes_text = lng(user_id).get('in_group_user_see_group_menu_text').format(
                    groupname=groupinfo.get('name'),
                    users_count=len(group_users),
                    refer_link=refer_link
                )
                userspage = paginator(group_users, page)
                for user in userspage:
                    username = get_user_info(user.get('user_id')).get('name')
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=username,
                            callback_data='uprofile-' + str(user.get('user_id'))
                        )
                    )
                if len(group_users) <= config.pagelimit:
                    pass
                else:
                    chek_next_btn = len(paginator(group_users, page + 1))
                    if chek_next_btn > 0:
                        if page == 1:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='группа-' + str(page + 1)
                                )
                            )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='группа-' + str(page - 1)
                                ),
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='группа-' + str(page + 1)
                                )
                            )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('back_p'),
                                callback_data='группа-' + str(page - 1)
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
            else:
                if userinfo.get('refer_id'):
                    group_created = True
                    groupinfo = get_group_info_by_owner(userinfo.get('refer_id'))
                    put_user_to_group(groupinfo.get('id'), user_id)
                    group_users = get_owner_group_users(groupinfo.get('owner_id'))
                    ownerinfo = get_user_info(groupinfo.get('owner_id'))
                    group_users.append(
                        {
                            'id': ownerinfo.get('id'),
                            'group_id': groupinfo.get('id'),
                            'user_id': ownerinfo.get('user_id')
                        }
                    )
                    refer_link = 'https://t.me/jrobot_demo_bot?start=' + str(groupinfo.get('owner_id'))
                    mes_text = lng(user_id).get('in_group_user_see_group_menu_text').format(
                        groupname=groupinfo.get('name'),
                        users_count=len(group_users),
                        refer_link=refer_link
                    )
                    userspage = paginator(group_users, page)
                    for user in userspage:
                        username = get_user_info(user.get('user_id')).get('name')
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=username,
                                callback_data='uprofile-' + str(user.get('user_id'))
                            )
                        )
                    if len(group_users) <= config.pagelimit:
                        pass
                    else:
                        chek_next_btn = len(paginator(group_users, page + 1))
                        if chek_next_btn > 0:
                            if page == 1:
                                keyboard.add(
                                    types.InlineKeyboardButton(
                                        text=lng(user_id).get('next'),
                                        callback_data='группа-' + str(page + 1)
                                    )
                                )
                            else:
                                keyboard.add(
                                    types.InlineKeyboardButton(
                                        text=lng(user_id).get('back_p'),
                                        callback_data='группа-' + str(page - 1)
                                    ),
                                    types.InlineKeyboardButton(
                                        text=lng(user_id).get('next'),
                                        callback_data='группа-' + str(page + 1)
                                    )
                                )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='группа-' + str(page - 1)
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
                else:
                    if fr:
                        mes_text = lng(user_id).get('acc_not_created')
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('create_acc'),
                                callback_data='группа-1'
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
                    else:
                        group_created = False
        return group_created
    else:
        if message:
            start_user_menu(message=message)
        else:
            start_user_menu(c=c)


def user_profile(c, profile_id):
    user_id = c.from_user.id
    userinfo = get_user_info(profile_id)
    mes_text = lng(user_id).get('user_profile_menu_text').format(
        username=userinfo.get('name'),
        datereg=date_revers(userinfo.get('info').get('date_reg'))
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='группа-1'
        ),
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_task_to_user'),
            callback_data='task_to_user!' + str(profile_id)
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def user_aprowed_start_menu(user_id):
    userinfo = get_user_info(user_id)
    refer_id = userinfo.get('refer_id')
    refer_name = get_user_info(refer_id)
    refer_name = refer_name.get('name')
    group_name = get_group_info_by_owner(refer_id)
    group_name = group_name.get('name')
    mes_text = lng(user_id).get('message_send_aprowed_user_text').format(
        refer_username=refer_name,
        group_name=group_name
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        btn(lng(user_id).get('learn_mnu_btn'), 'LEARN'),
        btn(lng(user_id).get('tasks_mnu_btn'), 'TASKS'),
        btn(lng(user_id).get('polls_mnu_btn'), 'POLLS'),
        btn(lng(user_id).get('meet_mnu_btn'), 'MEET'),
        btn(lng(user_id).get('user_group_mnu_btn'), 'GROUP'),
        btn(lng(user_id).get('settings'), 'SETTINGS'),
    )
    bot.send_message(
        user_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def refer_aprowed_user(c, status=1):
    user_id = c.from_user.id
    if status:
        ans_text = lng(user_id).get('refer_aprowed_user_text')
    else:
        ans_text = lng(user_id).get('refer_cancel_user_text')
    bot.answer_callback_query(
        c.id,
        text=ans_text,
        show_alert=False)
    start_user_menu(c=c)


def user_cancel_start_menu(user_id):
    userinfo = get_user_info(user_id)
    refer_id = userinfo.get('refer_id')
    refer_name = get_user_info(refer_id)
    refer_name = refer_name.get('name')
    group_name = get_group_info_by_owner(refer_id)
    group_name = group_name.get('name')
    update_user_status(user_id, 1)
    remove_user_from_group(user_id)
    mes_text = lng(user_id).get('message_send_cancel_user_text').format(
        refer_username=refer_name,
        group_name=group_name
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        btn(lng(user_id).get('learn_mnu_btn'), 'LEARN'),
        btn(lng(user_id).get('tasks_mnu_btn'), 'TASKS'),
        btn(lng(user_id).get('polls_mnu_btn'), 'POLLS'),
        btn(lng(user_id).get('meet_mnu_btn'), 'MEET'),
        btn(lng(user_id).get('user_group_mnu_btn'), 'GROUP'),
        btn(lng(user_id).get('settings'), 'SETTINGS'),
    )
    bot.send_message(
        user_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def settings_menu(c):
    user_id = c.from_user.id
    mes_text = lng(user_id).get('settings_menu_text')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        btn(lng(user_id).get('en_lng_btn'), 'ENG'),
        btn(lng(user_id).get('ru_lng_btn'), 'RUS'),
        btn(lng(user_id).get('to_menu_btn'), 'MENU')
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
