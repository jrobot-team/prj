# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config
from lng_fn import lng
from dbclasses import User, Group, GroupUsers, Task, UserTask
from bot_utils import str_to_array, date_revers

bot = telebot.TeleBot(config.token)


def alert_new_user(user_id, refer_id):
    username = User.get(User.user_id == user_id).name
    date_reg = date_revers(str_to_array(User.get(User.user_id == user_id).info).get('date_reg'))
    group_id = GroupUsers.get(GroupUsers.user_id == user_id).group_id
    group_name = Group.get(Group.id == group_id).name
    mes_text = lng(user_id).get('message_send_new_referal').format(
        group_name=group_name,
        username=username,
        date_reg=date_reg
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('aprowe_btn'),
            callback_data='подтвердитьU' + str(user_id)
        ),
        types.InlineKeyboardButton(
            text=lng(user_id).get('cancel_reg'),
            callback_data='отклонить_регуU' + str(user_id)
        )
    )
    bot.send_message(
        refer_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def alert_close_task(task_id):
    creator_id = Task.get(Task.id == task_id).creator_id
    task_name = Task.get(Task.id == task_id).name
    comment = str_to_array(Task.get(Task.id == task_id).info).get('comment')
    mes_text = lng(creator_id).get('alert_close_task').format(
        task_name=task_name,
        comment=comment
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('view_task'),
            callback_data='task^' + str(task_id) + '^main'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('to_menu_btn'),
            callback_data='MENU'
        )
    )
    bot.send_message(
        creator_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def alert_do_task(task_id):
    creator_id = Task.get(Task.id == task_id).creator_id
    task_name = Task.get(Task.id == task_id).name
    mes_text = lng(creator_id).get('alert_do_task').format(
        task_name=task_name
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('view_task'),
            callback_data='task^' + str(task_id) + '^main'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('to_menu_btn'),
            callback_data='MENU'
        )
    )
    bot.send_message(
        creator_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def alert_cancel_task(task_id):
    creator_id = Task.get(Task.id == task_id).creator_id
    task_name = Task.get(Task.id == task_id).name
    mes_text = lng(creator_id).get('alert_cancel_task').format(
        task_name=task_name
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('view_task'),
            callback_data='task^' + str(task_id) + '^main'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(creator_id).get('to_menu_btn'),
            callback_data='MENU'
        )
    )
    bot.send_message(
        creator_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def alert_15_min_task_end(task_id):
    user_id = UserTask.get(UserTask.task_id == task_id).user_id
    task_name = Task.get(Task.id == task_id).name
    creator_id = Task.get(Task.id == task_id).creator_id
    creator_username = User.get(User.user_id == creator_id).name
    date_start = Task.get(Task.id == task_id).date_start
    date_end = Task.get(Task.id == task_id).date_end
    task_text = str_to_array(Task.get(Task.id == task_id).info).get('task_text')
    mes_text = lng(user_id).get('alert_15_do_task').format(
        task_name=task_name,
        creator_username=creator_username,
        date_start=date_revers(date_start),
        date_end=date_revers(date_end),
        task_text=task_text
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('close_task_mnu_btn'),
            callback_data='изменить_статус_задачи#' + str(task_id) + '#0'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('to_menu_btn'),
            callback_data='MENU'
        )
    )
    bot.send_message(
        user_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
