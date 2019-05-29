# -*- coding: utf-8 -*-
import logging

import cherrypy
import telebot
from telebot import types

import config
from botutils import (del_answers_list, del_chek_answers, get_user_info,
                      make_agency_fn, make_fio_fn, make_town_fn,
                      record_answer_story, replacer,
                      upd_user_learn_question_id, upd_user_test_question_id,
                      validate_answers)
from lang import ru
from menu import (learn_test_question, start_learn_menu, start_menu,
                  test_question)


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
bot = telebot.TeleBot(config.TOKEN)
cancel = [
    '/start',
]

###################################################


def make_fio(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        fio = replacer(message.text)
        make_fio_fn(user_id, fio)
        mes_text = ru.get('reg_message_agency')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_agency)


def make_agency(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        agency = replacer(message.text)
        make_agency_fn(user_id, agency)
        mes_text = ru.get('reg_message_town')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_town)


def make_town(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        town = replacer(message.text)
        make_town_fn(user_id, town)
        test_count = get_user_info(user_id)[0].get('test_count')
        mes_text = ru.get('menu_message').format(
            test_count=test_count
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('learn_btn'),
                callback_data='learn'),
            types.InlineKeyboardButton(
                text=ru.get('test_btn'),
                callback_data='prepare_your_anus'))
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


# Регистрация
@bot.message_handler(commands=['start'])
def start(message):
    start_menu(message=message)


# Нижнее меню
@bot.message_handler(func=lambda message: True, content_types=['text'])
def menu(message):
    pass


# Inline
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'menu':
        start_menu(c=c)

    if c.data == 'register':
        mes_text = ru.get('reg_message_fio')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_fio)

    if c.data == 'learn':
        user_id = c.from_user.id
        mes_text = ru.get('learn_message')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('begin'),
                callback_data='start_learn'),
            types.InlineKeyboardButton(
                text=ru.get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'start_learn':
        start_learn_menu(c)

    if 'learn_test_question-' in c.data:
        answer_id = int(c.data.split('-')[1])
        learn_test_question(c, answer_id)

    if c.data == 'chek_answer':
        user_id = c.from_user.id
        question_id = get_user_info(user_id)[0].get('learn_question_id')
        valid = validate_answers(user_id, test=False)
        if valid == 'valid':
            upd_user_learn_question_id(user_id, question_id)
            ans_text = ru.get('answer_valid')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            start_learn_menu(c)
        elif valid == 'invalid':
            ans_text = ru.get('answer_invalid')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            start_learn_menu(c)
        else:
            ans_text = ru.get('answer_error')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)

    if c.data == 'prepare_your_anus':
        mes_text = ru.get('test_prepare_message')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('begin'),
                callback_data='testing'),
            types.InlineKeyboardButton(
                text=ru.get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'testing':
        user_id = c.from_user.id
        del_chek_answers(user_id)
        del_answers_list(user_id)
        test_question(c, 0)

    if 'question_test-' in c.data:
        answer_id = int(c.data.split('-')[1])
        test_question(c, answer_id)

    if c.data == 'chekanswertest':
        user_id = c.from_user.id
        valid = validate_answers(user_id)
        if valid != 'error':
            question_id = get_user_info(user_id)[0].get('test_question_id')
            record_answer_story(user_id, question_id, valid)
            del_chek_answers(user_id)
            del_answers_list(user_id)
            upd_user_test_question_id(user_id, question_id)
            test_question(c, 0)
        else:
            ans_text = ru.get('answer_error')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)

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
