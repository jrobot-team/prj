# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from botutils import (get_admins, get_booking_info, get_user_current_lang,
                      plane_info, str_to_array, user_info)
from lng_fn import lng

# telegram bot api
bot = telebot.TeleBot(config.TOKEN)


def alert_hard_reise(booking_id):
    book = get_booking_info(booking_id)
    user = user_info(book.get('user_id'))
    user_id = book.get('user_id')
    managers_uids = get_admins(role='manager')[1]
    comment = str_to_array(book.get('hard_reise')).get('comment')
    mes_text = lng(user_id).get('hard_reise_alert_text').format(
        date=book.get('date'),
        phone=user.get('phone'),
        comment=comment
    )
    if managers_uids:
        for manager_id in managers_uids:
            try:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('view'),
                        callback_data='просмотр_брони-' + str(booking_id)
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_to_menu_btn'),
                        callback_data='menu'
                    )
                )
                bot.send_message(
                    chat_id=manager_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard
                )
            except:
                pass


def alert_new_booking(booking_id):
    book = get_booking_info(booking_id)
    user = user_info(book.get('user_id'))
    user_id = book.get('user_id')
    managers_uids = get_admins(role='manager')[1]
    if book.get('hard_reise') == 'no_hard':
        mes_text = lng(user_id).get('mng_send_new_booking').format(
            date_pub=book.get('date'),
            phone=user.get('phone'),
            date_to_fly=book.get('date_fly'),
            seats=book.get('seats'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction')
        )
    else:
        mes_text = lng(user_id).get('rew_mng_send_new_booking').format(
            date_pub=book.get('date'),
            phone=user.get('phone'),
            date_to_fly=book.get('date_fly'),
            seats=book.get('seats'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            rew_dir=book.get('direction_out')
        )
    if managers_uids:
        for manager_id in managers_uids:
            try:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('view'),
                        callback_data='просмотр_брони-' + str(booking_id)
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_to_menu_btn'),
                        callback_data='menu'
                    )
                )
                bot.send_message(
                    chat_id=manager_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard
                )
            except:
                pass


def alert_user_booking_true(booking_id):
    book = get_booking_info(booking_id)
    user_id = book.get('user_id')
    if book.get('hard_reise') == 'no_hard':
        mes_text = lng(user_id).get('user_booking_true_text').format(
            date_fly=book.get('date'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            plane_model=book.get('plane_model'),
            company=book.get('company'),
            price=book.get('price_char')
        )
    else:
        hard = str_to_array(book.get('hard_reise')).get('type')
        if hard == 'rew':
            mes_text = lng(user_id).get('user_booking_true_text').format(
                date_fly=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                rew_dir=book.get('direction_out'),
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char')
            )
        else:
            comment = str_to_array(book.get('hard_reise')).get('comment')
            mes_text = lng(user_id).get('hard_reise_true_view').format(
                booking_id=book.get('id'),
                date=book.get('date'),
                phone=user_info(book.get('user_id')).get('phone'),
                comment=comment
            )
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('view'),
                callback_data='подробная_инф_о_брони-' + str(booking_id)
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.send_message(
            chat_id=book.get('user_id'),
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard
        )
    except:
        pass


def alert_user_booking_cancel(booking_id):
    book = get_booking_info(booking_id)
    user_id = book.get('user_id')
    if book.get('hard_reise') == 'no_hard':
        mes_text = lng(user_id).get('user_booking_cancel_text').format(
            date_fly=book.get('date'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            plane_model=book.get('plane_model'),
            company=book.get('company'),
            price=book.get('price_char')
        )
    else:
        hard = str_to_array(book.get('hard_reise')).get('type')
        if hard == 'rew':
            mes_text = lng(user_id).get('rew_user_booking_cancel_text').format(
                date_fly=book.get('date'),
                direction_out=book.get('direction_out'),
                direction=book.get('direction'),
                rew_dir=book.get('direction_out'),
                plane_model=book.get('plane_model'),
                company=book.get('company'),
                price=book.get('price_char')
            )
        else:
            comment = str_to_array(book.get('hard_reise')).get('comment')
            mes_text = lng(user_id).get('hard_reise_cancel_view').format(
                booking_id=book.get('id'),
                date=book.get('date'),
                phone=user_info(book.get('user_id')).get('phone'),
                comment=comment
            )
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('view'),
                callback_data='подробная_инф_о_брони-' + str(booking_id)
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.send_message(
            chat_id=book.get('user_id'),
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard
        )
    except:
        pass


def alert_user_ask_set_true(ask_id):
    ask = get_booking_info(ask_id)
    user_id = ask.get('user_id')
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
    mes_text = lng(user_id).get('user_ask_details_text').format(
        date=ask.get('date'),
        plane=lng(user_id).get('plane').format(
            model=plane.get('plane'),
            prod=plane.get('producer'),
            seats_in=plane.get('seats_in'),
            flight_time=flt
        ),
        phone=user_info(ask.get('user_id')).get('phone'),
        seats=ask.get('seats')
    )
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'
            )
        )
        bot.send_message(
            chat_id=ask.get('user_id'),
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard
        )
    except:
        pass


def alert_manager_ask_create(ask_id):
    managers_uids = get_admins(role='manager')[1]
    ask = get_booking_info(ask_id)
    user_id = ask.get('user_id')
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
    mes_text = lng(user_id).get('mng_ask_details_text_created').format(
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
    for manager_id in managers_uids:
        try:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('view'),
                    callback_data='просмотр_заявки-' + str(ask_id)
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'
                )
            )
            bot.send_message(
                chat_id=manager_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard
            )
        except:
            pass


def alert_auto_func(booking_id):
    book = get_booking_info(booking_id)
    user_id = book.get('user_id')
    if book.get('hard_reise') == 'no_hard':
        mes_text = lng(user_id).get('alert_text').format(
            date=book.get('date'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            seats=book.get('seats')
        )
    else:
        mes_text = lng(user_id).get('alert_text').format(
            date=book.get('date'),
            direction_out=book.get('direction_out'),
            direction=book.get('direction'),
            rew_dir=book.get('direction_out'),
            seats=book.get('seats')
        )
    bot.send_message(
        chat_id=book.get('user_id'),
        text=mes_text,
        parse_mode='html'
    )
