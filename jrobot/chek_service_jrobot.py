# -*- coding: utf-8 -*-
import telebot
import config
import time
from datetime import datetime, timedelta
from dbclasses import Poll, Task, Forum
from publicator import send_new_poll, send_new_forum
from alerter import alert_15_min_task_end
from forum_menu import forum_detail_menu


bot = telebot.TeleBot(config.token)


def chek_polls_end():
    date = datetime.now() + timedelta(hours=1)
    delta_plus = date + timedelta(minutes=1)
    delta_minus = date - timedelta(minutes=1)
    polls_query = Poll.select().where(Poll.date_end.between(delta_minus, delta_plus))
    for poll in polls_query:
        if poll.status:
            Poll.update(status=0).where(Poll.id == poll.id).execute()
            send_new_poll(poll.id)


def send_alert_end_task():
    date = datetime.now() + timedelta(hours=1)
    date = date + timedelta(minutes=15)
    delta_plus = date + timedelta(minutes=1)
    delta_minus = date - timedelta(minutes=1)
    task_query = Task.select().where(Task.date_end.between(delta_minus, delta_plus))
    for task in task_query:
        if task.status == 2 and task.send == 0:
            Task.update(send=1).where(Task.id == task.id).execute()
            alert_15_min_task_end(task.id)


def send_alert_start_forum():
    date = datetime.now() + timedelta(hours=1)
    date = date + timedelta(minutes=15)
    delta_plus = date + timedelta(minutes=1)
    delta_minus = date - timedelta(minutes=1)
    forum_query = Forum.select().where(Forum.date_start.between(delta_minus, delta_plus))
    for forum in forum_query:
        if forum.status == 1 and forum.send == 0:
            Forum.update(send=1).where(Forum.id == forum.id).execute()
            send_new_forum(forum.id, send=1)


def send_past_forum_to_creator():
    date = datetime.now() + timedelta(hours=1)
    date = date - timedelta(minutes=10)
    delta_plus = date + timedelta(minutes=1)
    delta_minus = date - timedelta(minutes=1)
    forum_query = Forum.select().where(Forum.date_end.between(delta_minus, delta_plus))
    for forum in forum_query:
        if forum.status == 1 and forum.send == 1:
            Forum.update(status=0, send=2).where(Forum.id == forum.id).execute()
            forum_detail_menu(forum.id, uid=forum.creator_id)


def main():
    while True:
        try:
            chek_polls_end()
            send_alert_end_task()
            send_alert_start_forum()
            send_past_forum_to_creator()
            time.sleep(60)
        except Exception as e:
            bot.send_message(
                5675578,
                text=e,
                parse_mode='html')
            time.sleep(10)


if __name__ == "__main__":
    main()
