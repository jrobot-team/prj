# -*- coding: utf-8 -*-
import telebot
import config
from poll_menu import poll_detail_menu
from poll_utils import get_poll_info
from users_utils import get_all_group_users_by_group_id
from tasks_menu import task_detail
from forum_utils import get_forum_info
from forum_menu import forum_detail_menu

bot = telebot.TeleBot(config.token)


def send_new_poll(poll_id):
    group_id = get_poll_info(poll_id).get('group_id')
    users = get_all_group_users_by_group_id(group_id)
    for user in users:
        try:
            poll_detail_menu(poll_id, uid=user.get('user_id'))
        except:
            pass


def send_new_task(task_id, uid):
    task_detail(task_id, uid=uid)


def send_new_forum(forum_id, send=0, head=0):
    group_id = get_forum_info(forum_id).get('group_id')
    users = get_all_group_users_by_group_id(group_id)
    for user in users:
        try:
            forum_detail_menu(forum_id, uid=user.get('user_id'), send=send, head=head)
        except:
            pass
