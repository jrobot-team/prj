# -*- coding: utf-8 -*-
import logging

import cherrypy
import telebot

import config
from alerter import alert_cancel_task, alert_close_task, alert_do_task
from bot_utils import Basedate, date_revers, replacer
from calendar_helper import create_calendar
from forum_menu import (forum_calendar_menu, forum_delta_menu,
                        forum_detail_menu, forum_menu, forum_time_menu,
                        forum_users_menu, forums_by_status_menu)
from forum_utils import (chek_date, chek_delta, create_forum, get_forum_info,
                         update_forum_comment, update_forum_date_start,
                         update_forum_delta, update_forum_name,
                         update_forum_status, update_forum_theme)
from lang import ru
from lng_fn import lng
from main_menu import keymenu, startmenu
from poll_menu import (arch_polls_menu, poll_calendar_menu, poll_detail_menu,
                       poll_time_menu, polls_menu, user_select_poll_variant)
from poll_utils import create_poll, date_end_cheker, update_poll_date_end
from publicator import send_new_forum, send_new_poll, send_new_task
from tasks_menu import (select_user_to_make_task, task_calendar_menu,
                        task_detail, task_time_menu, user_tasks_menu,
                        user_view_tasks_list)
from tasks_utils import (create_task, get_task_info, get_uid_by_task_id,
                         update_task_date_end, update_task_status)
from tester_menu import (chek_learn_answer, chek_user_learn, learn,
                         learn_question, rec_test_answer, test, tester_menu,
                         user_choose_learn_curs, user_get_test, user_learn,
                         user_tester_menu)
from user_menu import (refer_aprowed_user, settings_menu, start_user_menu,
                       user_aprowed_start_menu, user_cancel_start_menu,
                       user_group_menu, user_profile, users_view, view_users)
from users_utils import create_group, update_user_status


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
    '/start',
    '/Start',
    '/cancel',
    ru.get('learn_mnu_btn'),
    ru.get('tasks_mnu_btn'),
    ru.get('polls_mnu_btn'),
    ru.get('users_mnu_btn'),
    ru.get('meet_mnu_btn'),
    ru.get('user_group_mnu_btn'),
]

###################################################


def create_group_fn(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        group_name = replacer(message.text)
        create_group(user_id, group_name)
        user_group_menu(message=message)


def create_poll_fn(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        poll_name = replacer(message.text)
        mes_text = lng(user_id).get('create_poll_polltext_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, create_poll_text_fn, poll_name=poll_name)


def create_poll_text_fn(message, poll_name='без названия'):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        poll_text = replacer(message.text)
        mes_text = lng(user_id).get('create_poll_poll_chooses_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, create_poll_chooses_fn, poll_name=poll_name, poll_text=poll_text)


def create_poll_chooses_fn(message, poll_name='без названия', poll_text='нет текста'):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        poll_chooses = message.text
        poll_id = create_poll(
            user_id,
            poll_name,
            poll_text,
            poll_chooses,
            date_end=Basedate().plus_one_day()
        )
        poll_calendar_menu(poll_id, message=message)


def create_poll_date_end_fn(message, poll_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_end = message.text
        if date_end_cheker(date_end):
            poll_time_menu(poll_id, date_end, message=message)
        else:
            mes_text = lng(user_id).get('create_poll_add_date_end_error').format(
                date_end=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_poll_date_end_again_fn,
                poll_id=poll_id)


def create_poll_date_end_again_fn(message, poll_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_end = date_end_cheker(message.text)
        if date_end:
            poll_time_menu(poll_id, date_end, message=message)
        else:
            mes_text = lng(user_id).get('create_poll_add_date_end_error').format(
                date_end=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_poll_date_end_fn,
                poll_id=poll_id)


def create_task_name_fn(message, recepient_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        task_name = replacer(message.text)
        mes_text = lng(user_id).get('create_task_text_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            create_task_text_fn,
            recepient_id=recepient_id,
            task_name=task_name)


def create_task_text_fn(message, recepient_id=0, task_name='без названия'):
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        task_text = replacer(message.text)
        task_id = create_task(
            message.from_user.id,
            recepient_id,
            task_name,
            task_text,
            date_end=Basedate().date_hm()
        )
        update_task_status(task_id, status=4)
        task_calendar_menu(task_id, message=message)


def create_task_date_end_fn(message, task_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_end = message.text
        if date_end_cheker(date_end):
            task_time_menu(task_id, date_end, message=message)
        else:
            dtend = date_revers(Basedate().date())
            mes_text = lng(user_id).get('create_task_date_end_text_again').format(
                date_end=dtend
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_task_date_end_again_fn,
                task_id=task_id)


def create_task_date_end_again_fn(message, task_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_end = message.text
        if date_end_cheker(date_end):
            task_time_menu(task_id, date_end, message=message)
        else:
            dtend = date_revers(Basedate().date())
            mes_text = lng(user_id).get('create_task_date_end_text_again').format(
                date_end=dtend
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_task_date_end_fn,
                task_id=task_id)


def close_task_fn(message, task_id=0):
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        task_comment = replacer(message.text)
        update_task_status(task_id, comment=task_comment)
        task_detail(task_id, message=message)
        alert_close_task(task_id)


def create_forum_name_fn(message):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        forum_name = replacer(message.text)
        mes_text = lng(user_id).get('forum_create_theme_text').format(
            forum_name=forum_name
        )
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            create_forum_theme_fn,
            forum_name=forum_name
        )


def create_forum_theme_fn(message, forum_name='без названия'):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        forum_theme = replacer(message.text)
        forum_id = create_forum(
            forum_name,
            user_id,
            forum_theme,
            '01:00',
            users=[user_id]
        )
        forum_calendar_menu(forum_id, message=message)


def create_forum_date_start_fn(message, forum_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_start = chek_date(message.text)
        if date_start:
            date_start = str(date_start).split(' ')[0]
            forum_time_menu(forum_id, date_start, message=message)
        else:
            mes_text = lng(user_id).get('forum_create_date_text_again').format(
                forum_name=get_forum_info(forum_id).get('forum_name'),
                date_now=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_forum_date_start_again_fn,
                forum_id=forum_id
            )


def create_forum_date_start_again_fn(message, forum_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        date_start = chek_date(message.text)
        if date_start:
            date_start = str(date_start).split(' ')[0]
            forum_time_menu(forum_id, date_start, message=message)
        else:
            mes_text = lng(user_id).get('forum_create_date_text_again').format(
                forum_name=get_forum_info(forum_id).get('forum_name'),
                date_now=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_forum_date_start_fn,
                forum_id=forum_id
            )


def create_forum_time_fn(message, forum_id=0, date_start=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            forum_delta_menu(forum_id, date_start, time, message=message)
        else:
            mes_text = lng(user_id).get('forum_create_manual_time_agian_menu').format(
                forum_name=get_forum_info(forum_id).get('forum_name')
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_forum_time_again_fn, forum_id=forum_id, date_start=date_start)


def create_forum_time_again_fn(message, forum_id=0, date_start=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            forum_delta_menu(forum_id, date_start, time, message=message)
        else:
            mes_text = lng(user_id).get('forum_create_manual_time_agian_menu').format(
                forum_name=get_forum_info(forum_id).get('forum_name')
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_forum_time_fn, forum_id=forum_id, date_start=date_start)


def create_task_time_fn(message, task_id=0, date_end=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            date_end = date_end + ' ' + time
            update_task_date_end(task_id, date_end)
            uid = get_uid_by_task_id(task_id)
            creator_id = get_task_info(task_id).get('creator_id')
            if uid == creator_id:
                status = 2
            else:
                status = 1
            update_task_status(task_id, status=status)
            if uid != creator_id:
                task_detail(task_id, message=message)
            send_new_task(task_id, uid)
        else:
            mes_text = lng(user_id).get('task_create_manual_time_again_menu')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_task_time_again_fn, task_id=task_id, date_end=date_end)


def create_task_time_again_fn(message, task_id=0, date_end=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            date_end = date_end + ' ' + time
            update_task_date_end(task_id, date_end)
            uid = get_uid_by_task_id(task_id)
            creator_id = get_task_info(task_id).get('creator_id')
            if uid == creator_id:
                status = 2
            else:
                status = 1
            update_task_status(task_id, status=status)
            if uid != creator_id:
                task_detail(task_id, message=message)
            send_new_task(task_id, uid)
        else:
            mes_text = lng(user_id).get('task_create_manual_time_again_menu')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_task_time_fn, task_id=task_id, date_end=date_end)


def create_poll_time_fn(message, poll_id=0, date_end=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            date_end = date_end + ' ' + time
            update_poll_date_end(poll_id, date_end)
            send_new_poll(poll_id)
        else:
            mes_text = lng(user_id).get('poll_create_manual_time_again_menu')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_poll_time_again_fn, poll_id=poll_id, date_end=date_end)


def create_poll_time_again_fn(message, poll_id=0, date_end=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        time = message.text
        if chek_delta(time):
            date_end = date_end + ' ' + time
            update_poll_date_end(poll_id, date_end)
            send_new_poll(poll_id)
        else:
            mes_text = lng(user_id).get('poll_create_manual_time_again_menu')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_poll_time_fn, poll_id=poll_id, date_end=date_end)


def forum_end_add_comment_fn(message, forum_id=0):
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        comment = message.text
        update_forum_comment(forum_id, comment)
        update_forum_status(forum_id, status=0)
        forum_detail_menu(forum_id, message=message, where_from='ended')
        send_new_forum(forum_id, send=0, head=1)


def forum_edit_name_fn(message, forum_id=0):
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        forum_name = message.text
        update_forum_name(forum_id, forum_name)
        forum_detail_menu(forum_id, message=message)


def forum_edit_theme_fn(message, forum_id=0):
    if message.text in cancel:
        keymenu(message, cncl=True)
    else:
        forum_name = message.text
        update_forum_theme(forum_id, forum_name)
        forum_detail_menu(forum_id, message=message)


# Регистрация
@bot.message_handler(commands=['start', 'Start', 'cancel'])
def start(message):
    startmenu(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'document'])
def menu(message):
    user_id = message.from_user.id
    if message.text in cancel:
        if message.text == lng(user_id).get('user_group_mnu_btn'):
            chek_group = user_group_menu(message=message)
            if chek_group:
                pass
            else:
                mes_text = lng(user_id).get('create_group_message_text')
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(msg, create_group_fn)
        else:
            keymenu(message, cncl=True)
    else:
        pass


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'SETTINGS':
        settings_menu(c)

    if 'DAY' in c.data:
        year = c.data.split(';')[1]
        month = c.data.split(';')[2]
        day = c.data.split(';')[3]
        cb = c.data.split(';')[4]
        fn = cb.split('+')[0]
        if fn == 'poll':
            poll_id = cb.split('+')[1]
            date_end = '{y}-{m}-{d}'.format(
                y=year,
                m=month,
                d=day
            )
            poll_time_menu(poll_id, date_end, c=c)
        elif fn == 'task':
            task_id = cb.split('+')[1]
            date_end = '{y}-{m}-{d}'.format(
                y=year,
                m=month,
                d=day
            )
            task_time_menu(task_id, date_end, c=c)
        else:
            forum_id = cb.split('+')[1]
            date_start = '{y}-{m}-{d}'.format(
                y=year,
                m=month,
                d=day
            )
            forum_time_menu(forum_id, date_start, c=c)

    if '-MONTH' in c.data:
        user_id = c.from_user.id
        medt = c.data.split(';')[0].split('-')[0]
        year = int(c.data.split(';')[1])
        month = int(c.data.split(';')[2])
        cbk = c.data.split(';')[4]
        if medt == 'NEXT':
            month = month + 1
            if month > 12:
                year = year + 1
                month = 1
        else:
            month = month - 1
            if month == 0:
                year = year - 1
                month = 12
        mes_text = lng(user_id).get('poll_create_get_date')
        markup = create_calendar(year=year, month=month, cb=cbk)
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=markup)

    if c.data == 'MENU':
        start_user_menu(c=c)

    if c.data == 'LEARN':
        user_tester_menu(c=c)

    if c.data == 'TASKS':
        user_tasks_menu(c=c)

    if c.data == 'POLLS':
        polls_menu(c=c)

    if c.data == 'MEET':
        forum_menu(c=c)

    if c.data == 'GROUP':
        user_group_menu(c=c, fr=True)

    if 'learn)' in c.data:
        question_number = int(c.data.split(')')[1])
        learn(c, question_number=question_number)

    if 'lquestion)' in c.data:
        question_number = int(c.data.split(')')[1])
        answer_id = int(c.data.split(')')[2])
        learn_question(c, question_number=question_number, answer_id=answer_id)

    if 'chek_learn_answer-' in c.data:
        question_number = int(c.data.split('-')[1])
        chek_learn_answer(c, question_number)

    if 'test)' in c.data:
        question_number = int(c.data.split(')')[1])
        answer_id = int(c.data.split(')')[2])
        test(c, question_number=question_number, answer_id=answer_id)

    if 'rec_test_answer-' in c.data:
        question_id = int(c.data.split('-')[1])
        rec_test_answer(c, question_id)
        question_number = question_id + 1
        test(c, question_number=question_number, answer_id=0)

    if c.data == 'testmenu':
        tester_menu(c=c)

    if c.data == 'usersview':
        users_view(c=c)

    if 'viewallusers+' in c.data:
        page = int(c.data.split('+')[1])
        view_users(c, page=page)

    if 'группа-' in c.data:
        user_id = c.from_user.id
        page = int(c.data.split('-')[1])
        chek_group = user_group_menu(c=c, page=page)
        if chek_group:
            pass
        else:
            mes_text = lng(user_id).get('create_group_message_text')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_group_fn)

    if c.data == 'обучение':
        user_tester_menu(c=c)

    if c.data == 'обучение_приветствие':
        user_choose_learn_curs(c)

    if 'обучалка-' in c.data:
        question_id = int(c.data.split('-')[1])
        answer_id = int(c.data.split('-')[2])
        user_learn(c, question_id, answer_id=answer_id)

    if 'проверка=' in c.data:
        question_id = int(c.data.split('=')[1])
        chek_user_learn(c, question_id)

    if 'тестирование*' in c.data:
        question_id = int(c.data.split('*')[1])
        answer_id = int(c.data.split('*')[2])
        user_get_test(c, question_id=question_id, answer_id=answer_id)

    if 'uprofile-' in c.data:
        profile_id = int(c.data.split('-')[1])
        user_profile(c, profile_id)

    if c.data == 'создать_опрос':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('create_poll_name_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, create_poll_fn)

    if c.data == 'опросы':
        polls_menu(c=c)

    if c.data == 'архив_опросов':
        arch_polls_menu(c=c)

    if 'poll-' in c.data:
        poll_id = int(c.data.split('-')[1])
        poll_detail_menu(poll_id, c=c)

    if 'датопрос#' in c.data:
        user_id = c.from_user.id
        poll_id = int(c.data.split('#')[1])
        date_end = c.data.split('#')[2]
        if date_end == 'add':
            mes_text = lng(user_id).get('create_poll_add_date_end_error').format(
                date_end=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_poll_date_end_fn,
                poll_id=poll_id)
        else:
            poll_time_menu(poll_id, date_end, c=c)

    if 'заопрос>' in c.data:
        user_id = c.from_user.id
        poll_id = int(c.data.split('>')[1])
        date_end = c.data.split('>')[2]
        time = c.data.split('>')[3]
        if time == 'manual':
            mes_text = lng(user_id).get('poll_create_manual_time_menu')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_poll_time_fn, poll_id=poll_id, date_end=date_end)
        else:
            date_end = date_end + ' ' + time
            update_poll_date_end(poll_id, date_end)
            send_new_poll(poll_id)

    if 'вариант@' in c.data:
        poll_id = int(c.data.split('@')[1])
        var_id = int(c.data.split('@')[2])
        user_select_poll_variant(c, poll_id, var_id)

    if c.data == 'задачи':
        user_tasks_menu(c=c)

    if 'создать_задачу/' in c.data:
        page = int(c.data.split('/')[1])
        select_user_to_make_task(c=c, page=page)

    if 'task_to_user!' in c.data:
        user_id = c.from_user.id
        recepient_id = int(c.data.split('!')[1])
        mes_text = lng(user_id).get('create_task_name_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, create_task_name_fn, recepient_id=recepient_id)

    if 'taskdata#' in c.data:
        user_id = c.from_user.id
        task_id = int(c.data.split('#')[1])
        date_end = c.data.split('#')[2]
        if date_end == 'add':
            dtend = date_revers(Basedate().date())
            mes_text = lng(user_id).get('create_task_date_end_text').format(
                date_end=dtend
            )
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_task_date_end_fn,
                task_id=task_id)
        else:
            task_time_menu(task_id, date_end, c=c)

    if 'завремя>' in c.data:
        user_id = c.from_user.id
        task_id = int(c.data.split('>')[1])
        date_end = c.data.split('>')[2]
        time = c.data.split('>')[3]
        if time == 'manual':
            mes_text = lng(user_id).get('task_create_manual_time_menu')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_task_time_fn, task_id=task_id, date_end=date_end)
        else:
            date_end = date_end + ' ' + time
            update_task_date_end(task_id, date_end)
            uid = get_uid_by_task_id(task_id)
            creator_id = get_task_info(task_id).get('creator_id')
            if uid == creator_id:
                status = 2
            else:
                status = 1
            update_task_status(task_id, status=status)
            if uid != creator_id:
                task_detail(task_id, c=c)
            send_new_task(task_id, uid)

    if 'task^' in c.data:
        task_id = int(c.data.split('^')[1])
        where_come = c.data.split('^')[2]
        task_detail(task_id, c=c, where_come=where_come)

    if 'изменить_статус_задачи#' in c.data:
        user_id = c.from_user.id
        task_id = int(c.data.split('#')[1])
        status = int(c.data.split('#')[2])
        if status == 0:
            mes_text = lng(user_id).get('close_task_get_comment')
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, close_task_fn, task_id=task_id)
        if status == 2:
            alert_do_task(task_id)
        if status == 3:
            alert_cancel_task(task_id)
        update_task_status(task_id, status=status)
        task_detail(task_id, c=c)

    if c.data == 'завершенные_задачи':
        user_view_tasks_list(c=c)

    if c.data == 'собрания':
        forum_menu(c=c)

    if c.data == 'завершенные_собрания':
        forums_by_status_menu(c=c)

    if 'forum%' in c.data:
        forum_id = int(c.data.split('%')[1])
        where_from = c.data.split('%')[2]
        forum_detail_menu(forum_id, c=c, where_from=where_from)

    if c.data == 'запланировать_собрание':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('forum_create_name_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, create_forum_name_fn)

    if 'ФДАТА#' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('#')[1])
        chek_date = c.data.split('#')[2]
        if chek_date == 'add':
            mes_text = lng(user_id).get('forum_create_date_text').format(
                forum_name=get_forum_info(forum_id).get('forum_name'),
                date_now=date_revers(Basedate().date())
            )
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_forum_date_start_fn, forum_id=forum_id)
        else:
            forum_time_menu(forum_id, chek_date, c=c)

    if 'deltas>' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('>')[1])
        date_start = c.data.split('>')[2]
        time = c.data.split('>')[3]
        if time == 'manual':
            mes_text = lng(user_id).get('forum_create_manual_time_menu').format(
                forum_name=get_forum_info(forum_id).get('forum_name')
            )
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(msg, create_forum_time_fn, forum_id=forum_id, date_start=date_start)
        else:
            forum_delta_menu(forum_id, date_start, time, c=c)

    if ';фв>' in c.data:
        forum_id = int(c.data.split('>')[1])
        date_start = c.data.split('>')[2]
        time = c.data.split('>')[3]
        delta = c.data.split('>')[4]
        page = int(c.data.split('>')[5])
        uid = int(c.data.split('>')[6])
        forum_users_menu(
            c,
            forum_id,
            date_start,
            time,
            delta,
            page,
            uid
        )

    if 'зсф<' in c.data:
        forum_id = int(c.data.split('<')[1])
        date_start = c.data.split('<')[2]
        time = c.data.split('<')[3]
        delta = c.data.split('<')[4]
        date_start = date_start + ' ' + time
        update_forum_date_start(forum_id, date_start)
        update_forum_delta(forum_id, delta)
        update_forum_status(forum_id, status=1)
        send_new_forum(forum_id)

    if 'собраниеучастники=' in c.data:
        forum_id = int(c.data.split('=')[1])
        forum_users_menu(c, forum_id, '0', '0', '0', 1, 0, edit=1)

    if 'ФУ>' in c.data:
        forum_id = int(c.data.split('>')[1])
        date_start = c.data.split('>')[2]
        time = c.data.split('>')[3]
        delta = c.data.split('>')[4]
        page = int(c.data.split('>')[5])
        uid = int(c.data.split('>')[6])
        forum_users_menu(
            c,
            forum_id,
            date_start,
            time,
            delta,
            page,
            uid,
            edit=1
        )

    if 'ЗУФ<' in c.data:
        forum_id = int(c.data.split('<')[1])
        forum_detail_menu(forum_id, c=c)

    if 'отменить_собрание.' in c.data:
        forum_id = int(c.data.split('.')[1])
        update_forum_status(forum_id, status=0)
        forum_detail_menu(forum_id, c=c, where_from='ended')

    if 'завершить_собрание!' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('!')[1])
        mes_text = lng(user_id).get('forum_end_add_comment_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, forum_end_add_comment_fn, forum_id=forum_id)

    if 'итогис!' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('!')[1])
        mes_text = lng(user_id).get('forum_end_add_comment_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, forum_end_add_comment_fn, forum_id=forum_id)

    if 'собрание-изменить-имя=' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('=')[1])
        mes_text = lng(user_id).get('forum_update_name_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, forum_edit_name_fn, forum_id=forum_id)

    if 'собраниедата=' in c.data:
        forum_id = int(c.data.split('=')[1])
        forum_calendar_menu(forum_id, c=c)

    if 'собраниеповестка=' in c.data:
        user_id = c.from_user.id
        forum_id = int(c.data.split('=')[1])
        mes_text = lng(user_id).get('forum_update_theme_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, forum_edit_theme_fn, forum_id=forum_id)

    if 'подтвердитьU' in c.data:
        user_id = int(c.data.split('U')[1])
        update_user_status(user_id, 1)
        user_aprowed_start_menu(user_id)
        refer_aprowed_user(c, status=1)

    if 'отклонить_регуU' in c.data:
        user_id = int(c.data.split('U')[1])
        refer_aprowed_user(c, status=0)
        user_cancel_start_menu(user_id)

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
