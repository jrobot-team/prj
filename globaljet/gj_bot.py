# -*- coding: utf-8 -*-
import logging

import cherrypy
import telebot
from telebot import types

import config
from botutils import (Basedate, cancel_booking, change_lang, date_actualaiser,
                      date_time_updater, edit_direction_out_fn, get_admins,
                      get_booking, get_booking_id_by_date, get_booking_info,
                      get_temp_user_cat_planes, get_user_booking_by_id,
                      get_user_current_lang, make_ask_by_user, make_comment,
                      make_date_fly_fn, make_hard_reise, make_place_from,
                      make_plane_id_temp, make_rewinder_reise,
                      make_seats_booking_edt, make_seats_booking_fn,
                      make_temp_booking_id, make_to_direction_place_fn,
                      msg_count, msg_deleter, plane_info, reg_user, replacer,
                      sort_planes, str_to_array, temp_user_cat_planes_seats,
                      upd_book_status, upd_booking_set_company,
                      upd_booking_set_plane, upd_booking_set_price,
                      upd_user_fio, upd_user_phone, user_info)
from lng_fn import lng
from menu import (admin_menu, cancel_booking_menu, done_asks_menu,
                  done_booking_menu, menu_book_edited, mng_asks_menu,
                  mng_booking_menu, start_menu, true_booking_menu,
                  user_booking_menu, user_settings_menu)
from sender import (alert_hard_reise, alert_manager_ask_create,
                    alert_new_booking, alert_user_ask_set_true,
                    alert_user_booking_cancel, alert_user_booking_true)


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
    '/start'
]

###################################################


def make_phone(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        phone = replacer(message.text)
        upd_user_phone(user_id, phone)
        mes_text = lng(user_id).get('register_complite')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        start_menu(message=message)


def make_phone_from_ask(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        phone = message.contact.phone_number
        upd_user_phone(user_id, phone)
        make_ask_by_user(user_id)
        mes_text = lng(user_id).get('ask_complite')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton(lng(user_id).get('back_to_menu_btn')))
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        msg_count(user_id, user_id, msg.message_id)


def make_fio(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    if message.text in cancel:
        start_menu(message=message)
    else:
        fio = replacer(message.text)
        reg_user(user_id, username)
        upd_user_fio(user_id, fio)
        mes_text = lng(user_id).get('make_phone_message')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_phone)


def edit_fio(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        fio = replacer(message.text)
        upd_user_fio(user_id, fio)
        start_menu(message=message)


def ask_plane_seats(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        keyboard = types.InlineKeyboardMarkup()
        seats = replacer(message.text)
        seats = seats.replace(' ', '')
        seats = seats.replace(',', '')
        seats = seats.replace('.', '')
        if seats.isdigit():
            temp_user_cat_planes_seats(user_id, seats)
            mes_text = lng(user_id).get('seats_message').format(
                seats=seats
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('fl_time_1-2'),
                    callback_data='fltime_1-6')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('fl_time_3-5'),
                    callback_data='fltime_6-9')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('fl_time_5-10'),
                    callback_data='fltime_9-10')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='user_planes_cat'),)
        else:
            mes_text = lng(user_id).get('seats_error_message')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'))
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        msg_count(user_id, user_id, msg.message_id)


def make_book_from_place(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        place = replacer(message.text)
        date = Basedate().date_hms()
        make_place_from(user_id, place, date)
        booking_id = get_booking_id_by_date(user_id, date)
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('to_direction_place_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_to_direction_place)


def make_to_direction_place(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        direction = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        make_to_direction_place_fn(direction, booking_id)
        mes_text = lng(user_id).get('date_fly_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_date_fly, booking_id=booking_id)


def make_date_fly(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        date_fly = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        make_date_fly_fn(user_id, booking_id, date_fly)
        mes_text = lng(user_id).get('ask_seats_message')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_seats_booking, booking_id=booking_id)


def make_seats_booking(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        seats = replacer(message.text)
        seats = seats.replace(' ', '')
        seats = seats.replace(',', '')
        seats = seats.replace('.', '')
        keyboard = types.InlineKeyboardMarkup()
        if seats.isdigit():
            temp = get_temp_user_cat_planes(user_id)
            if temp:
                booking_id = temp.get('booking_id')
            make_seats_booking_fn(user_id, booking_id, seats)
            if user_info(user_id).get('phone'):
                booking = get_user_booking_by_id(user_id, booking_id)
                alert_new_booking(booking_id)
                if booking.get('hard_reise') == 'no_hard':
                    mes_text = lng(user_id).get('booking_message_text').format(
                        date_fly=booking.get('date_fly'),
                        direction_out=booking.get('direction_out'),
                        direction=booking.get('direction'),
                        seats=seats
                    )
                else:
                    mes_text = lng(user_id).get('rew_booking_message_text').format(
                        date_fly=booking.get('date_fly'),
                        direction_out=booking.get('direction_out'),
                        direction=booking.get('direction'),
                        rew_dir=booking.get('direction_out'),
                        seats=seats
                    )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_to_menu_btn'),
                        callback_data='menu')
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
            else:
                mes_text = lng(user_id).get('user_whant_to_send_phone')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_phone = types.KeyboardButton(
                    text=lng(user_id).get('send_phone'),
                    request_contact=True)
                keyboard.add(button_phone)
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
                bot.register_next_step_handler(msg, ask_phone, booking_id=booking_id)
        else:
            temp = get_temp_user_cat_planes(user_id)
            if temp:
                booking_id = temp.get('booking_id')
            make_seats_booking(user_id, booking_id, 1)
            booking = get_user_booking_by_id(user_id, booking_id)
            mes_text = lng(user_id).get('booking_message_text_seats_error').format(
                date_fly=booking.get('date_fly'),
                direction_out=booking.get('direction_out'),
                direction=booking.get('direction'),
                seats=booking.get('seats')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu')
            )
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)


def ask_phone(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        phone = message.contact.phone_number
        upd_user_phone(user_id, phone)
        booking = get_user_booking_by_id(user_id, booking_id)
        alert_new_booking(booking_id)
        if booking.get('hard_reise') == 'no_hard':
            mes_text = lng(user_id).get('booking_message_text').format(
                date_fly=booking.get('date_fly'),
                direction_out=booking.get('direction_out'),
                direction=booking.get('direction'),
                seats=booking.get('seats')
            )
        else:
            mes_text = lng(user_id).get('rew_booking_message_text').format(
                date_fly=booking.get('date_fly'),
                direction_out=booking.get('direction_out'),
                direction=booking.get('direction'),
                rew_dir=booking.get('direction_out'),
                seats=booking.get('seats')
            )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu')
        )
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def hard_reise_ask_phone(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        phone = message.contact.phone_number
        upd_user_phone(user_id, phone)
        alert_hard_reise(booking_id)
        mes_text = lng(user_id).get('hard_reise_meked_text')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='reise'
            )
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard
        )


def edit_fly_date(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        fly_date = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        else:
            booking_id = 0
        make_date_fly_fn(user_id, booking_id, fly_date)
        menu_book_edited(message, booking_id)


def edit_direction_out(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        direction_out = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        else:
            booking_id = 0
        edit_direction_out_fn(direction_out, booking_id)
        menu_book_edited(message, booking_id)


def edit_direction(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        direction = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        else:
            booking_id = 0
        make_to_direction_place_fn(direction, booking_id)
        menu_book_edited(message, booking_id)


def edit_seats(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        seats = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        else:
            booking_id = 0
        make_seats_booking_edt(user_id, booking_id, seats)
        menu_book_edited(message, booking_id)


def edit_comment(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        comment = replacer(message.text)
        temp = get_temp_user_cat_planes(user_id)
        if temp:
            booking_id = temp.get('booking_id')
        else:
            booking_id = 0
        make_comment(user_id, booking_id, comment)
        menu_book_edited(message, booking_id)


def actual_date(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        actual_date = date_actualaiser(message.text, booking_id=booking_id)
        keyboard = types.InlineKeyboardMarkup()
        if actual_date:
            mes_text = lng(user_id).get('mng_actual_date_done')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='просмотр_брони-' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_btn_boking'),
                    callback_data='mng_booking'
                )
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            msg_count(user_id, user_id, msg.message_id)
        else:
            mes_text = lng(user_id).get('mng_actual_date_false')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='просмотр_брони-' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_resend'),
                    callback_data='синхронизировать_дату-' + str(booking_id)
                )
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            msg_count(user_id, user_id, msg.message_id)
        message_id = message.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_date(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        upd_date = date_time_updater(message.text, booking_id=booking_id)
        if upd_date:
            mes_text = lng(user_id).get('mng_update_book_info_date_success')
            msg = bot.send_message(
                chat_id=message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
            msg_count(user_id, user_id, msg.message_id)
            bot.register_next_step_handler(msg, upd_book_info_dir_out, booking_id=booking_id)
        else:
            keyboard = types.InlineKeyboardMarkup()
            mes_text = lng(user_id).get('mng_update_book_info_date_error')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='просмотр_брони-' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_resend'),
                    callback_data='обновить_информацию_брони-' + str(booking_id)
                )
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            msg_count(user_id, user_id, msg.message_id)
        message_id = message.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_dir_out(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        dir_out = replacer(message.text)
        edit_direction_out_fn(dir_out, booking_id)
        mes_text = lng(user_id).get('mng_update_book_info_direction_out')
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html'
        )
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, upd_book_info_direction, booking_id=booking_id)
        message_id = msg.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_direction(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        direction = replacer(message.text)
        make_to_direction_place_fn(direction, booking_id)
        mes_text = lng(user_id).get('mng_update_book_set_plane')
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, upd_book_info_set_plane, booking_id=booking_id)
        message_id = msg.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_set_plane(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        plane_model = replacer(message.text)
        upd_booking_set_plane(plane_model, booking_id)
        mes_text = lng(user_id).get('mng_update_book_set_company')
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html'
        )
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, upd_book_info_set_company, booking_id=booking_id)
        message_id = msg.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_set_company(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        company = replacer(message.text)
        upd_booking_set_company(company, booking_id)
        mes_text = lng(user_id).get('mng_update_book_set_price')
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html'
        )
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, upd_book_info_set_price, booking_id=booking_id)
        message_id = msg.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def upd_book_info_set_price(message, booking_id=0):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        price = message.text
        upd_booking_set_price(price, booking_id)
        book = get_booking_info(booking_id)
        mes_text = lng(user_id).get('mng_update_book_done').format(
            date_fly=book.get('date'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            plane_model=book.get('plane_model'),
            company=book.get('company'),
            price=book.get('price_char')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='просмотр_брони-' + str(booking_id)
            )
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard
        )
        msg_count(user_id, user_id, msg.message_id)
        message_id = msg.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)


def hard_reise_maker(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        hard_resie = replacer(message.text)
        booking_id = make_hard_reise(user_id, hard_resie)
        if user_info(user_id).get('phone'):
            alert_hard_reise(booking_id)
            mes_text = lng(user_id).get('hard_reise_meked_text')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='reise'
                )
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard
            )
        else:
            mes_text = lng(user_id).get('user_whant_to_send_phone')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_phone = types.KeyboardButton(
                text=lng(user_id).get('send_phone'),
                request_contact=True)
            keyboard.add(button_phone)
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            bot.register_next_step_handler(msg, hard_reise_ask_phone, booking_id=booking_id)


def two_reise_maker(message):
    user_id = message.from_user.id
    if message.text in cancel:
        start_menu(message=message)
    else:
        rew_reise = replacer(message.text)
        booking_id = make_rewinder_reise(user_id, rew_reise)
        mes_text = lng(user_id).get('to_direction_place_text')
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, make_to_direction_place, booking_id=booking_id)


# Регистрация
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    admins = get_admins()
    if user_id in admins[1] or user_id in config.ADMIN:
        admin_menu(message=message)
    else:
        user = user_info(user_id)
        if user:
            start_menu(message=message)
        else:
            mes_text = lng(user_id).get('choose_lang_text')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('ru_lang'),
                    callback_data='choose_ru'),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('en_lang'),
                    callback_data='choose_en'))
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)


# Нижнее меню
@bot.message_handler(func=lambda message: True, content_types=['text'])
def menu(message):
    user_id = message.from_user.id
    if message.text == lng(user_id).get('back_to_menu_btn'):
        start_menu(message=message)


# Inline
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'choose_ru':
        user_id = c.from_user.id
        username = c.from_user.first_name
        reg_user(user_id, username, lang=0)
        keyboard = types.InlineKeyboardMarkup()
        mes_text = lng(user_id).get('hello_message_reg_user').format(
            fio=username)
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('reise'),
                callback_data='reise'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('planes_cat_btn'),
                callback_data='user_planes_cat'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('settings'),
                callback_data='settings'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'choose_en':
        user_id = c.from_user.id
        username = c.from_user.first_name
        reg_user(user_id, username, lang=1)
        keyboard = types.InlineKeyboardMarkup()
        mes_text = lng(user_id).get('hello_message_reg_user').format(
            fio=username)
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('reise'),
                callback_data='reise'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('planes_cat_btn'),
                callback_data='user_planes_cat'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('settings'),
                callback_data='settings'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'stat_' in c.data:
        user_id = c.from_user.id
        period = c.data.split('_')[1]
        mes_text = lng(user_id).get('admin_stata_menu_text').format(
            period=lng(user_id).get(period),
            new_booking=len(get_booking('booking', period=period)),
            true_booking=len(get_booking('true_booking', period=period)),
            done_booking=len(get_booking('done_booking', period=period)),
            cancel_booking=len(get_booking('cancel_booking', period=period)),
            new_ask=len(get_booking('ask', period=period)),
            done_ask=len(get_booking('done_ask', period=period)),
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'fltime_' in c.data:
        user_id = c.from_user.id
        fltime = int(c.data.split('_')[1].split('-')[1])
        planes = sort_planes(user_id, fltime)
        seats = get_temp_user_cat_planes(user_id).get('seats')
        keyboard = types.InlineKeyboardMarkup()
        for plane in planes:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=plane.get('plane'),
                    callback_data='plane_' + str(plane.get('id')) + '*' + str(fltime)
                )
            )
        mes_text = lng(user_id).get('plane_sort_menu_text')
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'plane_' in c.data:
        user_id = c.from_user.id
        tmp = c.data.split('_')[1]
        plane_id = int(tmp.split('*')[0])
        fltime = tmp.split('*')[1]
        plane = plane_info(plane_id)
        keyboard = types.InlineKeyboardMarkup()
        current_lng = get_user_current_lang(user_id)
        if current_lng:
            ft = plane.get('flight_time')
            if ft == 'До 6 часов':
                flt = 'Up to 6 hours'
            if ft == 'От 6 до 9 часов':
                flt = '6 to 9 hours'
            if ft == 'Свыше 9 часов':
                flt = 'Over 9 hours'
        else:
            flt = plane.get('flight_time')
        if plane.get('seats_in') >= 18:
            mes_text = lng(user_id).get('plane_18_info_text').format(
                model=plane.get('plane'),
                prod=plane.get('producer'),
                seats_in=plane.get('seats_in'),
                flight_time=flt,
                url=plane.get('producer_url')
            )
        else:
            mes_text = lng(user_id).get('plane_info_text').format(
                model=plane.get('plane'),
                prod=plane.get('producer'),
                seats_in=plane.get('seats_in'),
                flight_time=flt,
                url=plane.get('producer_url')
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('make_ask'),
                callback_data='makeask_' + str(plane_id)
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='fltime_0-' + str(fltime)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'makeask_' in c.data:
        user_id = c.from_user.id
        plane_id = int(c.data.split('_')[1])
        plane = plane_info(plane_id)
        seats = get_temp_user_cat_planes(user_id).get('seats')
        user = user_info(user_id)
        current_lng = get_user_current_lang(user_id)
        if current_lng:
            ft = plane.get('flight_time')
            if ft == 'До 6 часов':
                flt = 'Up to 6 hours'
            if ft == 'От 6 до 9 часов':
                flt = '6 to 9 hours'
            if ft == 'Свыше 9 часов':
                flt = 'Over 9 hours'
        else:
            flt = plane.get('flight_time')
        if user:
            phone = user.get('phone')
        else:
            username = c.from_user.first_name
            reg_user(user_id, username)
            user = user_info(user_id)
            phone = user.get('phone')
        if len(phone):
            keyboard = types.InlineKeyboardMarkup()
            mes_text = lng(user_id).get('make_ask_text').format(
                model=plane.get('plane'),
                seats=seats,
                flight_time=flt,
                phone=phone
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('yes_make_ask'),
                    callback_data='yesmakeask-' + str(plane_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'
                )
            )
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            make_plane_id_temp(user_id, plane_id)
            mes_text = lng(user_id).get('make_ask_text_no_phone').format(
                model=plane.get('plane'),
                seats=seats,
                flight_time=flt,
                phone=phone
            )
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_phone = types.KeyboardButton(
                text=lng(user_id).get('send_phone'),
                request_contact=True)
            keyboard.add(button_phone)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            msg_count(user_id, user_id, msg.message_id)
            bot.register_next_step_handler(msg, make_phone_from_ask)

    if 'yesmakeask-' in c.data:
        user_id = c.from_user.id
        plane_id = int(c.data.split('-')[1])
        make_plane_id_temp(user_id, plane_id)
        ask_id = make_ask_by_user(user_id)
        if ask_id:
            alert_manager_ask_create(ask_id)
        mes_text = lng(user_id).get('ask_complite')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'askview=' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('=')[1])
        book = get_user_booking_by_id(user_id, booking_id)
        keyboard = types.InlineKeyboardMarkup()
        if book.get('hard_reise') == 'no_hard':
            plane = plane_info(book.get('plane_id'))
            if plane:
                plane = plane.get('plane')
            else:
                plane = lng(user_id).get('plane_no_append')
            mes_text = lng(user_id).get('book_menu_view_text').format(
                plane=plane,
                seats=book.get('seats'),
                ask_day=book.get('day_to_flight'),
                date=book.get('date_fly'),
                ask_status=lng(user_id).get(book.get('status')),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_date_fly_btn'),
                    callback_data='edit_datefly+' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_direction_out_btn'),
                    callback_data='edit_dirout+' + str(booking_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_direction_btn'),
                    callback_data='edit_dir+' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_seats_btn'),
                    callback_data='edit_seats+' + str(booking_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_comment_btn'),
                    callback_data='addcomment+' + str(booking_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='reise'
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'
                )
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                plane = plane_info(book.get('plane_id'))
                if plane:
                    plane = plane.get('plane')
                else:
                    plane = lng(user_id).get('plane_no_append')
                mes_text = lng(user_id).get('rew_book_menu_view_text').format(
                    plane=plane,
                    seats=book.get('seats'),
                    ask_day=book.get('day_to_flight'),
                    date=book.get('date_fly'),
                    ask_status=lng(user_id).get(book.get('status')),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    rew_dir=book.get('direction_out'),
                    comment=book.get('comment')
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_date_fly_btn'),
                        callback_data='edit_datefly+' + str(booking_id)
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_direction_out_btn'),
                        callback_data='edit_dirout+' + str(booking_id)
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_direction_btn'),
                        callback_data='edit_dir+' + str(booking_id)
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_seats_btn'),
                        callback_data='edit_seats+' + str(booking_id)
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_comment_btn'),
                        callback_data='addcomment+' + str(booking_id)
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back'),
                        callback_data='reise'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_to_menu_btn'),
                        callback_data='menu'
                    )
                )
            else:
                comment = str_to_array(book.get('hard_reise'))
                mes_text = lng(user_id).get('hard_reise_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment.get('comment')
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_to_menu_btn'),
                        callback_data='menu'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back'),
                        callback_data='reise'
                    )
                )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'отмена_бронирования-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        cancel_booking(booking_id)
        user_booking_menu(c)

    if 'edit_datefly+' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('+')[1])
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('edit_date_fly_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_fly_date)

    if 'edit_dirout+' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('+')[1])
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('edit_direction_out_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_direction_out)

    if 'edit_dir+' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('+')[1])
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('edit_direction_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_direction)

    if 'edit_seats+' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('+')[1])
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('edit_seats_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_seats)

    if 'addcomment+' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('+')[1])
        make_temp_booking_id(user_id, booking_id)
        mes_text = lng(user_id).get('edit_comment_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_comment)

    if c.data == 'reise':
        user_booking_menu(c)

    if c.data == 'menu':
        user_id = c.from_user.id
        admins = get_admins()
        if user_id in admins[1] or user_id in config.ADMIN:
            admin_menu(c=c)
        else:
            message_id = c.message.message_id
            chat_id = c.message.chat.id
            start_menu(c=c)
            msg_deleter(chat_id, message_id)

    if c.data == 'settings':
        user_settings_menu(c)

    if c.data == 'mng_booking':
        mng_booking_menu(c)

    if c.data == 'mng_asks':
        mng_asks_menu(c)

    if c.data == 'user_planes_cat':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('ask_seats_message')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, ask_plane_seats)

    if c.data == 'register':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('make_fio_message')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_fio)

    if c.data == 'edit_phone':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('make_phone_message')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_phone)

    if c.data == 'edit_fio':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('make_fio_message')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, edit_fio)

    if c.data == 'makebook':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('makebook_choise_menu')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('book_one_direction_btn'),
                callback_data='make_one_dir_book'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('book_two_direction_btn'),
                callback_data='make_two_dir_book'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('book_hard_direction_btn'),
                callback_data='make_hard_dir_book'
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'make_two_dir_book':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('two_from_place_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, two_reise_maker)

    if c.data == 'make_hard_dir_book':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('make_hard_reise_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(msg, hard_reise_maker)

    if c.data == 'make_one_dir_book':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('from_place_text')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, make_book_from_place)

    if 'просмотр_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        book = get_booking_info(booking_id)
        keyboard = types.InlineKeyboardMarkup()
        if book:
            if book.get('hard_reise') == 'no_hard':
                if book.get('dtf_set'):
                    date_pub = book.get('date')
                else:
                    date_pub = lng(user_id).get('not_set')
                mes_text = lng(user_id).get('mng_booking_details_text').format(
                    date_pub=date_pub,
                    fio=user_info(book.get('user_id')).get('fio'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    date_to_fly=book.get('date_fly'),
                    seats=book.get('seats'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    comment=book.get('comment'),
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_reload_info_btn'),
                        callback_data='обновить_информацию_брони-' + str(book.get('id'))
                    )
                )
            else:
                hard = str_to_array(book.get('hard_reise')).get('type')
                if hard == 'rew':
                    if book.get('dtf_set'):
                        date_pub = book.get('date')
                    else:
                        date_pub = lng(user_id).get('not_set')
                    mes_text = lng(user_id).get('rew_mng_booking_details_text').format(
                        date_pub=date_pub,
                        fio=user_info(book.get('user_id')).get('fio'),
                        phone=user_info(book.get('user_id')).get('phone'),
                        date_to_fly=book.get('date_fly'),
                        seats=book.get('seats'),
                        direction_out=book.get('direction_out'),
                        direction=book.get('direction'),
                        rew_dir=book.get('direction_out'),
                        comment=book.get('comment'),
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('mng_reload_info_btn'),
                            callback_data='обновить_информацию_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    comment = str_to_array(book.get('hard_reise'))
                    mes_text = lng(user_id).get('hard_reise_view').format(
                        booking_id=book.get('id'),
                        date=book.get('date'),
                        phone=user_info(book.get('user_id')).get('phone'),
                        comment=comment.get('comment')
                    )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_make_success_btn'),
                    callback_data='подтвердить_бронь-' + str(book.get('id'))
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_cancel_btn'),
                    callback_data='отменить_бронь-' + str(book.get('id'))
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='mng_booking'
                )
            )
        else:
            mes_text = lng(user_id).get('error')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back'),
                    callback_data='mng_booking'
                )
            )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'синхронизировать_дату-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        mes_text = lng(user_id).get('mng_actual_date_year')
        msg = bot.send_message(
            chat_id=c.message.chat.id,
            text=mes_text,
            parse_mode='html'
        )
        msg_count(user_id, user_id, msg.message_id)
        bot.register_next_step_handler(msg, actual_date, booking_id=booking_id)

    if 'обновить_информацию_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        mes_text = lng(user_id).get('mng_update_book_info')
        msg = bot.send_message(
            chat_id=c.message.chat.id,
            text=mes_text,
            parse_mode='html'
        )
        msg_count(user_id, user_id, msg.message_id)
        message_id = msg.message_id
        chat_id = c.message.chat.id
        msg_deleter(chat_id, message_id)
        bot.register_next_step_handler(msg, upd_book_info_date, booking_id=booking_id)

    if 'отменить_бронь-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        upd_book_status('cancel_booking', booking_id)
        alert_user_booking_cancel(booking_id)
        ans_text = lng(user_id).get('mng_book_set_cancel')
        bot.answer_callback_query(
            callback_query_id=c.id,
            text=ans_text,
            show_alert=True
        )
        mng_booking_menu(c)

    if 'подтвердить_бронь-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        upd_book_status('true_booking', booking_id)
        alert_user_booking_true(booking_id)
        ans_text = lng(user_id).get('mng_book_set_true')
        bot.answer_callback_query(
            callback_query_id=c.id,
            text=ans_text,
            show_alert=True
        )
        book = get_booking_info(booking_id)
        if book.get('hard_reise') == 'no_hard':
            if book.get('dtf_set'):
                date_pub = book.get('date')
            else:
                date_pub = lng(user_id).get('not_set')
            mes_text = lng(user_id).get('mng_booking_details_text').format(
                date_pub=date_pub,
                fio=user_info(book.get('user_id')).get('fio'),
                phone=user_info(book.get('user_id')).get('phone'),
                date_to_fly=book.get('date_fly'),
                seats=book.get('seats'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_reload_info_btn'),
                    callback_data='обновить_информацию_брони-' + str(booking_id)
                )
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                if book.get('dtf_set'):
                    date_pub = book.get('date')
                else:
                    date_pub = lng(user_id).get('not_set')
                mes_text = lng(user_id).get('rew_mng_booking_details_text').format(
                    date_pub=date_pub,
                    fio=user_info(book.get('user_id')).get('fio'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    date_to_fly=book.get('date_fly'),
                    seats=book.get('seats'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    rew_dir=book.get('direction_out'),
                    comment=book.get('comment')
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_reload_info_btn'),
                        callback_data='обновить_информацию_брони-' + str(booking_id)
                    )
                )
            else:
                comment = str_to_array(book.get('hard_reise')).get('comment')
                mes_text = lng(user_id).get('hard_reise_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment
                )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='mng_booking'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'подробная_инф_о_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        book = get_booking_info(booking_id)
        if book.get('hard_reise') == 'no_hard':
            mes_text = lng(user_id).get('view_booking_by_user_text').format(
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char'),
                seats=book.get('seats'),
                date=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment'),
                ask_status=lng(user_id).get(book.get('status'))
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                mes_text = lng(user_id).get('rew_view_booking_by_user_text').format(
                    plane_model=book.get('plane_model'),
                    company=book.get('company'),
                    price=book.get('price_char'),
                    seats=book.get('seats'),
                    date=book.get('date'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    rew_dir=book.get('direction_out'),
                    comment=book.get('comment'),
                    ask_status=lng(user_id).get(book.get('status'))
                )
            else:
                comment = str_to_array(book.get('hard_reise')).get('comment')
                mes_text = lng(user_id).get('hard_reise_true_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment
                )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='reise'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'подтвержденные_брони':
        true_booking_menu(c)

    if 'пр_подтв_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        book = get_booking_info(booking_id)
        keyboard = types.InlineKeyboardMarkup()
        if book.get('hard_reise') == 'no_hard':
            mes_text = lng(user_id).get('view_booking_by_user_text').format(
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char'),
                seats=book.get('seats'),
                date=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment'),
                ask_status=lng(user_id).get(book.get('status'))
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_reload_info_btn'),
                    callback_data='обновить_информацию_брони-' + str(book.get('id'))
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('mng_cancel_btn'),
                    callback_data='отменить_бронь-' + str(book.get('id'))
                )
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                mes_text = lng(user_id).get('rew_view_booking_by_user_text').format(
                    plane_model=book.get('plane_model'),
                    company=book.get('company'),
                    price=book.get('price_char'),
                    seats=book.get('seats'),
                    date=book.get('date'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    rew_dir=book.get('direction_out'),
                    comment=book.get('comment'),
                    ask_status=lng(user_id).get(book.get('status'))
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_reload_info_btn'),
                        callback_data='обновить_информацию_брони-' + str(book.get('id'))
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_cancel_btn'),
                        callback_data='отменить_бронь-' + str(book.get('id'))
                    )
                )
            else:
                comment = str_to_array(book.get('hard_reise')).get('comment')
                mes_text = lng(user_id).get('hard_reise_true_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment
                )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='подтвержденные_брони'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'выполненные_брони':
        done_booking_menu(c)

    if 'пр_выполненной_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        book = get_booking_info(booking_id)
        if book.get('hard_reise') == 'no_hard':
            mes_text = lng(user_id).get('view_booking_by_user_text').format(
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char'),
                seats=book.get('seats'),
                date=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment'),
                ask_status=lng(user_id).get(book.get('status'))
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                mes_text = lng(user_id).get('rew_view_booking_by_user_text').format(
                    plane_model=book.get('plane_model'),
                    company=book.get('company'),
                    price=book.get('price_char'),
                    seats=book.get('seats'),
                    date=book.get('date'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    comment=book.get('comment'),
                    ask_status=lng(user_id).get(book.get('status'))
                )
            else:
                comment = str_to_array(book.get('hard_reise')).get('comment')
                mes_text = lng(user_id).get('hard_reise_true_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment
                )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='выполненные_брони'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'отмененные_брони':
        cancel_booking_menu(c)

    if 'пр_отмененной_брони-' in c.data:
        user_id = c.from_user.id
        booking_id = int(c.data.split('-')[1])
        book = get_booking_info(booking_id)
        if book.get('hard_reise') == 'no_hard':
            mes_text = lng(user_id).get('view_booking_by_user_text').format(
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char'),
                seats=book.get('seats'),
                date=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                comment=book.get('comment'),
                ask_status=lng(user_id).get(book.get('status'))
            )
        else:
            hard = str_to_array(book.get('hard_reise')).get('type')
            if hard == 'rew':
                mes_text = lng(user_id).get('rew_view_booking_by_user_text').format(
                    plane_model=book.get('plane_model'),
                    company=book.get('company'),
                    price=book.get('price_char'),
                    seats=book.get('seats'),
                    date=book.get('date'),
                    direction_out=book.get('direction_out'),
                    direction=book.get('direction'),
                    comment=book.get('comment'),
                    ask_status=lng(user_id).get(book.get('status'))
                )
            else:
                comment = str_to_array(book.get('hard_reise')).get('comment')
                mes_text = lng(user_id).get('hard_reise_cancel_view').format(
                    booking_id=book.get('id'),
                    date=book.get('date'),
                    phone=user_info(book.get('user_id')).get('phone'),
                    comment=comment
                )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='отмененные_брони'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'просмотр_заявки-' in c.data:
        user_id = c.from_user.id
        ask_id = int(c.data.split('-')[1])
        ask = get_booking_info(ask_id)
        plane = plane_info(ask.get('plane_id'))
        current_lng = get_user_current_lang(user_id)
        if current_lng:
            ft = plane.get('flight_time')
            if ft == 'До 6 часов':
                flt = 'Up to 6 hours'
            if ft == 'От 6 до 9 часов':
                flt = '6 to 9 hours'
            if ft == 'Свыше 9 часов':
                flt = 'Over 9 hours'
        else:
            flt = plane.get('flight_time')
        mes_text = lng(user_id).get('mng_ask_details_text').format(
            date=ask.get('date'),
            plane=lng(user_id).get('plane').format(
                model=plane.get('plane'),
                prod=plane.get('producer'),
                seats_in=plane.get('seats_in'),
                flight_time=flt
            ),
            fio=user_info(ask.get('user_id')).get('fio'),
            phone=user_info(ask.get('user_id')).get('phone'),
            seats=ask.get('seats')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('mng_ask_set_true'),
                callback_data='статус_заявки_выполнить-' + str(ask_id)
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='mng_asks'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if 'статус_заявки_выполнить-' in c.data:
        user_id = c.from_user.id
        ask_id = int(c.data.split('-')[1])
        upd_book_status('done_ask', ask_id)
        alert_user_ask_set_true(ask_id)
        ans_text = lng(user_id).get('mng_ask_set_true_succes')
        bot.answer_callback_query(
            callback_query_id=c.id,
            text=ans_text,
            show_alert=True
        )
        ask = get_booking_info(ask_id)
        plane = plane_info(ask.get('plane_id'))
        current_lng = get_user_current_lang(user_id)
        if current_lng:
            ft = plane.get('flight_time')
            if ft == 'До 6 часов':
                flt = 'Up to 6 hours'
            if ft == 'От 6 до 9 часов':
                flt = '6 to 9 hours'
            if ft == 'Свыше 9 часов':
                flt = 'Over 9 hours'
        else:
            flt = plane.get('flight_time')
        mes_text = lng(user_id).get('mng_ask_details_text').format(
            date=ask.get('date'),
            plane=lng(user_id).get('plane').format(
                model=plane.get('plane'),
                prod=plane.get('producer'),
                seats_in=plane.get('seats_in'),
                flight_time=flt
            ),
            fio=user_info(ask.get('user_id')).get('fio'),
            phone=user_info(ask.get('user_id')).get('phone'),
            seats=ask.get('seats')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='mng_asks'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'выполненные_заявки':
        done_asks_menu(c)

    if 'пр_выполненной_заявки-' in c.data:
        user_id = c.from_user.id
        ask_id = int(c.data.split('-')[1])
        ask = get_booking_info(ask_id)
        plane = plane_info(ask.get('plane_id'))
        current_lng = get_user_current_lang(user_id)
        if current_lng:
            ft = plane.get('flight_time')
            if ft == 'До 6 часов':
                flt = 'Up to 6 hours'
            if ft == 'От 6 до 9 часов':
                flt = '6 to 9 hours'
            if ft == 'Свыше 9 часов':
                flt = 'Over 9 hours'
        else:
            flt = plane.get('flight_time')
        mes_text = lng(user_id).get('mng_ask_details_text').format(
            date=ask.get('date'),
            plane=lng(user_id).get('plane').format(
                model=plane.get('plane'),
                prod=plane.get('producer'),
                seats_in=plane.get('seats_in'),
                flight_time=flt
            ),
            fio=user_info(ask.get('user_id')).get('fio'),
            phone=user_info(ask.get('user_id')).get('phone'),
            seats=ask.get('seats')
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back'),
                callback_data='выполненные_заявки'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

    if c.data == 'change_lang':
        user_id = c.from_user.id
        admins = get_admins()
        change_lang(user_id)
        if user_id in admins[1] or user_id in config.ADMIN:
            admin_menu(c=c)
        else:
            start_menu(c=c)

    if c.data == 'mngsettings':
        user_id = c.from_user.id
        mes_text = lng(user_id).get('mng_settings_text')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('lang_change_btn'),
                callback_data='change_lang'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)

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
