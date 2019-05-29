# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from bot_utils import date_revers
from lng_fn import lng
from paginators import paginator
from tasks_utils import (get_task_info, get_tasks_by_user_id,
                         get_user_tasks_by_status, get_creator_tasks_by_status)
from user_menu import start_user_menu
from users_utils import (get_group_info_by_id, get_group_info_by_owner,
                         get_owner_group_users, get_user_info,
                         is_user_in_group, is_user_owner, isuser,
                         put_user_to_group)
from calendar_helper import create_calendar

# telegram bot api
bot = telebot.TeleBot(config.token)


def user_tasks_menu(message=None, c=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    tasks = get_tasks_by_user_id(user_id)
    if tasks:
        mes_text = lng(user_id).get('user_task_menu_text')
        for task in tasks:
            if task.get('status') == 1 or task.get('status') == 2:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=task.get('task_name'),
                        callback_data='task^' + str(task.get('task_id')) + '^main'
                    )
                )
    else:
        mes_text = lng(user_id).get('user_notask_menu_text')
    """keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('user_creator_task_btn'),
            callback_data='созданные_задачи'
        )
    )"""
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('end_tasks_mnu_btn'),
            callback_data='завершенные_задачи'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_task_to_user'),
            callback_data='создать_задачу/1'
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


def select_user_to_make_task(c=None, message=None, page=1):
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
                mes_text = lng(user_id).get('user_select_user_to_add_task').format(
                    groupname=groupinfo.get('name'),
                    users_count=len(group_users)
                )
                userspage = paginator(group_users, page)
                for user in userspage:
                    username = get_user_info(user.get('user_id')).get('name')
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=username,
                            callback_data='task_to_user!' + str(user.get('user_id'))
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
                                    callback_data='создать_задачу/' + str(page + 1)
                                )
                            )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='создать_задачу/' + str(page - 1)
                                ),
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='создать_задачу/' + str(page + 1)
                                )
                            )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('back_p'),
                                callback_data='создать_задачу/' + str(page - 1)
                            )
                        )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='задачи'
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
                mes_text = lng(user_id).get('user_select_user_to_add_task_nousers').format(
                    groupname=groupinfo.get('name'),
                    refer_link=refer_link
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='задачи'
                    )
                )
                if message:
                    bot.send_message(
                        message.chat.id,
                        text=mes_text,
                        parse_mode='html')
                else:
                    bot.edit_message_text(
                        chat_id=c.message.chat.id,
                        message_id=c.message.message_id,
                        text=mes_text,
                        parse_mode='html')
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
                mes_text = lng(user_id).get('user_select_user_to_add_task').format(
                    groupname=groupinfo.get('name'),
                    users_count=len(group_users)
                )
                userspage = paginator(group_users, page)
                for user in userspage:
                    username = get_user_info(user.get('user_id')).get('name')
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=username,
                            callback_data='task_to_user!' + str(user.get('user_id'))
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
                                    callback_data='создать_задачу/' + str(page + 1)
                                )
                            )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='создать_задачу/' + str(page - 1)
                                ),
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('next'),
                                    callback_data='создать_задачу/' + str(page + 1)
                                )
                            )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('back_p'),
                                callback_data='создать_задачу/' + str(page - 1)
                            )
                        )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='задачи'
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
                    mes_text = lng(user_id).get('user_select_user_to_add_task').format(
                        groupname=groupinfo.get('name'),
                        users_count=len(group_users)
                    )
                    userspage = paginator(group_users, page)
                    for user in userspage:
                        username = get_user_info(user.get('user_id')).get('name')
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=username,
                                callback_data='task_to_user!' + str(user.get('user_id'))
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
                                        callback_data='создать_задачу/' + str(page + 1)
                                    )
                                )
                            else:
                                keyboard.add(
                                    types.InlineKeyboardButton(
                                        text=lng(user_id).get('back_p'),
                                        callback_data='создать_задачу/' + str(page - 1)
                                    ),
                                    types.InlineKeyboardButton(
                                        text=lng(user_id).get('next'),
                                        callback_data='создать_задачу/' + str(page + 1)
                                    )
                                )
                        else:
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=lng(user_id).get('back_p'),
                                    callback_data='создать_задачу/' + str(page - 1)
                                )
                            )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('back_p'),
                            callback_data='задачи'
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


def task_detail(task_id, c=None, message=None, where_come='main', uid=0):
    if c:
        user_id = c.from_user.id
    if message:
        user_id = message.from_user.id
    if uid:
        user_id = uid
    task = get_task_info(task_id)
    if task.get('status'):
        if task.get('status') == 1:
            status_text = lng(user_id).get('task_active')
            task_comment = ''
        elif task.get('status') == 2:
            status_text = lng(user_id).get('task_doing')
            task_comment = ''
        else:
            status_text = lng(user_id).get('task_cancel')
            task_comment = ''
    else:
        status_text = lng(user_id).get('task_end')
        task_comment = lng(user_id).get('task_comment').format(
            comment=task.get('info').get('comment')
        )
    creator_username = get_user_info(task.get('creator_id')).get('name')
    mes_text = lng(user_id).get('task_details_text').format(
        task_name=task.get('task_name'),
        creator_username=creator_username,
        date_start=date_revers(task.get('date_start')),
        date_end=date_revers(task.get('date_end')),
        task_text=task.get('info').get('task_text'),
        status=status_text,
        comment=task_comment
    )
    user_tasks = get_tasks_by_user_id(user_id)
    user_tasks_list = []
    for taskid in user_tasks:
        user_tasks_list.append(
            taskid.get('task_id')
        )
    keyboard = types.InlineKeyboardMarkup()
    if task_id in user_tasks_list and task.get('status') == 1:
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('im_do_this_task'),
                callback_data='изменить_статус_задачи#' + str(task_id) + '#2'
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('fuck_this_task'),
                callback_data='изменить_статус_задачи#' + str(task_id) + '#3'
            )
        )
    if task_id in user_tasks_list and task.get('status') == 2:
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('close_task_mnu_btn'),
                callback_data='изменить_статус_задачи#' + str(task_id) + '#0'
            )
        )
    if where_come == 'main':
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='задачи'
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='завершенные_задачи'
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


def user_view_tasks_list(c=None, message=None, status=0):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    tasks = get_user_tasks_by_status(user_id, status=status)
    tasks.extend(get_creator_tasks_by_status(user_id, status=status))
    if tasks:
        if status == 0:
            mes_text = lng(user_id).get('user_closed_task_menu_text').format(
                task_count=len(tasks)
            )
            where_come = '^closed'
        if status == 1:
            mes_text = lng(user_id).get('user_active_task_menu_text').format(
                task_count=len(tasks)
            )
            where_come = '^active'
        if status == 2:
            mes_text = lng(user_id).get('user_doing_task_menu_text').format(
                task_count=len(tasks)
            )
            where_come = '^doing'
        if status == 2:
            mes_text = lng(user_id).get('user_fucked_task_menu_text').format(
                task_count=len(tasks)
            )
            where_come = '^fucked'
        for task in tasks:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=task.get('task_name'),
                    callback_data='task^' + str(task.get('task_id')) + where_come
                )
            )
    else:
        if status == 0:
            mes_text = lng(user_id).get('user_noclosed_task_menu_text')
        if status == 1:
            mes_text = lng(user_id).get('user_noactive_task_menu_text')
        if status == 2:
            mes_text = lng(user_id).get('user_nodoing_task_menu_text')
        if status == 2:
            mes_text = lng(user_id).get('user_nofucked_task_menu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='задачи'
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


def task_calendar_menu(task_id, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('task_create_get_date')
    cb = 'task+' + str(task_id)
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


def task_time_menu(task_id, date_end, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('task_create_time_text')
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
        callback_data='завремя>' + str(task_id) + '>' + date_end + '>' + time) for time in timeslst])
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('add_date'),
            callback_data='завремя>' + str(task_id) + '>' + date_end + '>manual'
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
