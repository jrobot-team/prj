# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from botutils import (Basedate, admin_info, del_temp_user, get_booking,
                      get_user_all_booking, get_user_booking,
                      get_user_booking_by_id, get_users, msg_count,
                      msg_deleter, plane_info, reg_user, str_to_array,
                      user_info)
from lng_fn import lng

# telegram bot api
bot = telebot.TeleBot(config.TOKEN)


def admin_menu(message=False, c=False):
    date = Basedate().date()
    if message:
        user_id = message.from_user.id
    else:
        user_id = c.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.ADMIN:
        mes_text = lng(user_id).get('superadmin_menu_text')
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('su_admins_btn'),
                callback_data='управление_админами'))
    else:
        admin = admin_info(user_id)
        if admin.get('status'):
            if admin.get('role') == 'admin':
                mes_text = lng(user_id).get('admin_menu_text').format(
                    date=date,
                    asks_done=len(get_booking(status='done_ask')),
                    booking_done=len(get_booking(status='done_booking')),
                    users_count=len(get_users())
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('am_btn_stat_day'),
                        callback_data='stat_day'),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('am_btn_stat_week'),
                        callback_data='stat_week'),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('am_btn_stat_month'),
                        callback_data='stat_month'))
            else:
                asks = get_booking('ask')
                booking = get_booking('booking')
                mes_text = lng(user_id).get('manager_menu_text').format(
                    date=date,
                    asks_count=len(asks),
                    booking_count=len(booking)
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_btn_boking'),
                        callback_data='mng_booking'),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('mng_btn_asks'),
                        callback_data='mng_asks'))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('settings'),
                        callback_data='mngsettings'
                    )
                )
        else:
            mes_text = lng(user_id).get('error_message')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('reload_btn'),
                    callback_data='reload'))
    if message:
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        msg_count(user_id, user_id, msg.message_id)
        message_id = message.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        message_id = c.message.message_id
        chat_id = c.message.chat.id
        msg_deleter(chat_id, message_id)


def start_menu(message=False, c=False):
    if message:
        user_id = message.from_user.id
        username = message.from_user.first_name
    else:
        user_id = c.from_user.id
        username = c.from_user.first_name
    del_temp_user(user_id)
    user = user_info(user_id)
    keyboard = types.InlineKeyboardMarkup()
    if user and user.get('register'):
        mes_text = lng(user_id).get('hello_message_reg_user').format(
            fio=user.get('fio'))
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
    else:
        reg_user(user_id, username, lang=0)
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
    if message:
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        msg_count(user_id, user_id, msg.message_id)
        message_id = message.message_id
        chat_id = message.chat.id
        msg_deleter(chat_id, message_id)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        message_id = c.message.message_id
        chat_id = c.message.chat.id
        msg_deleter(chat_id, message_id)


def user_settings_menu(c):
    user_id = c.from_user.id
    user = user_info(user_id)
    mes_text = lng(user_id).get('settings_text').format(
        fio=user.get('fio'),
        phone=user.get('phone'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('lang_change_btn'),
            callback_data='change_lang'),
        types.InlineKeyboardButton(
            text=lng(user_id).get('edit_phone_btn'),
            callback_data='edit_phone'))
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


def user_reise_menu(c):
    user_id = c.from_user.id
    booking = get_user_booking(user_id, 'ask')
    keyboard = types.InlineKeyboardMarkup()
    if len(booking):
        if len(booking) == 1:
            plane = plane_info(booking[0].get('plane_id'))
            mes_text = lng(user_id).get('reise_menu_one').format(
                plane=plane.get('plane'),
                seats=booking[0].get('seats'),
                ask_day=booking[0].get('date'),
                ask_status=lng(user_id).get(booking[0].get('status'))
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('edit_booking'),
                    callback_data='askview=' + str(booking[0].get('id'))))
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('make_user_ask'),
                    callback_data='user_planes_cat'),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            for ask in booking:
                plane = plane_info(ask.get('plane_id'))
                keyboard = types.InlineKeyboardMarkup()
                mes_text = lng(user_id).get('reise_menu_one').format(
                    plane=plane.get('plane'),
                    seats=ask.get('seats'),
                    ask_day=ask.get('date'),
                    ask_status=lng(user_id).get(ask.get('status'))
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('edit_booking'),
                        callback_data='askview=' + str(ask.get('id'))))
                msg = bot.send_message(
                    c.message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
                msg_count(user_id, user_id, msg.message_id)
            mes_text = lng(user_id).get('reise_down_menu')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('make_user_ask'),
                    callback_data='user_planes_cat'),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_to_menu_btn'),
                    callback_data='menu'))
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
            msg_count(user_id, user_id, msg.message_id)
    else:
        mes_text = lng(user_id).get('no_ask_to_reise')
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('make_user_ask'),
                callback_data='user_planes_cat'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def user_booking_menu(c):
    user_id = c.from_user.id
    get_booking = get_user_all_booking(user_id)
    booking = []
    for book in get_booking:
        st = book.get('status')
        if st == 'true_booking' or st == 'booking' or st == 'cancel_booking':
            booking.append(book)
    keyboard = types.InlineKeyboardMarkup()
    if len(booking):
        for book in booking:
            if book.get('status') == 'true_booking':
                if book.get('hard_reise') == 'no_hard':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='подробная_инф_о_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    hard = str_to_array(book.get('hard_reise')).get('type')
                    if hard == 'rew':
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('rew_book_btn').format(
                                    dir_out=book.get('direction_out'),
                                    dir_in=book.get('direction')
                                ),
                                callback_data='подробная_инф_о_брони-' + str(book.get('id'))
                            )
                        )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('hard_reise_btn').format(
                                    booking_id=book.get('id')
                                ),
                                callback_data='подробная_инф_о_брони-' + str(book.get('id'))
                            )
                        )
            else:
                if book.get('hard_reise') == 'no_hard':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='askview=' + str(book.get('id'))
                        )
                    )
                else:
                    hard = str_to_array(book.get('hard_reise')).get('type')
                    if hard == 'rew':
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('rew_book_btn').format(
                                    dir_out=book.get('direction_out'),
                                    dir_in=book.get('direction')
                                ),
                                callback_data='askview=' + str(book.get('id'))
                            )
                        )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=lng(user_id).get('hard_reise_btn').format(
                                    booking_id=book.get('id')
                                ),
                                callback_data='askview=' + str(book.get('id'))
                            )
                        )
        mes_text = lng(user_id).get('book_down_menu')
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('make_user_ask'),
                callback_data='makebook'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        mes_text = lng(user_id).get('no_book_to_reise')
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('make_user_ask'),
                callback_data='makebook'),
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def mng_booking_menu(c):
    user_id = c.from_user.id
    mes_text = lng(user_id).get('mng_booking_menu_text').format(
        booking_count=len(get_booking('booking')),
        true_booking_count=len(get_booking('true_booking')),
        done_booking_count=len(get_booking('done_booking')),
        cancel_booking_count=len(get_booking('cancel_booking'))
    )
    booking = get_booking('booking')
    keyboard = types.InlineKeyboardMarkup()
    if booking:
        for book in booking:
            hard = book.get('hard_reise')
            if hard == 'no_hard':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('book_btn').format(
                            dir_out=book.get('direction_out'),
                            dir_in=book.get('direction')
                        ),
                        callback_data='просмотр_брони-' + str(book.get('id'))
                    )
                )
            else:
                hard = str_to_array(book.get('hard_reise')).get('type')
                if hard == 'rew':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('rew_book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='просмотр_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('hard_reise_btn').format(
                                booking_id=book.get('id')
                            ),
                            callback_data='просмотр_брони-' + str(book.get('id'))
                        )
                    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('mng_book_true_btn'),
            callback_data='подтвержденные_брони'),
        types.InlineKeyboardButton(
            text=lng(user_id).get('mng_book_done_btn'),
            callback_data='выполненные_брони'),
        types.InlineKeyboardButton(
            text=lng(user_id).get('mng_book_cancel_btn'),
            callback_data='отмененные_брони')
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


def true_booking_menu(c):
    user_id = c.from_user.id
    booking_true = get_booking('true_booking')
    keyboard = types.InlineKeyboardMarkup()
    if booking_true:
        for book in booking_true:
            if book.get('hard_reise') == 'no_hard':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('book_btn').format(
                            dir_out=book.get('direction_out'),
                            dir_in=book.get('direction')
                        ),
                        callback_data='пр_подтв_брони-' + str(book.get('id'))
                    )
                )
            else:
                hard = str_to_array(book.get('hard_reise')).get('type')
                if hard == 'rew':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('rew_book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='пр_подтв_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('hard_reise_btn').format(
                                booking_id=book.get('id')
                            ),
                            callback_data='пр_подтв_брони-' + str(book.get('id'))
                        )
                    )
    mes_text = lng(user_id).get('mng_booking_true_footer_text').format(
        true_booking_count=len(booking_true)
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu'
        ),
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


def done_booking_menu(c):
    user_id = c.from_user.id
    booking_true = get_booking('done_booking')
    keyboard = types.InlineKeyboardMarkup()
    if booking_true:
        for book in booking_true:
            if book.get('hard_reise') == 'no_hard':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('book_btn').format(
                            dir_out=book.get('direction_out'),
                            dir_in=book.get('direction')
                        ),
                        callback_data='пр_выполненной_брони-' + str(book.get('id'))
                    )
                )
            else:
                hard = str_to_array(book.get('hard_reise')).get('type')
                if hard == 'rew':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('rew_book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='пр_выполненной_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('hard_reise_btn').format(
                                booking_id=book.get('id')
                            ),
                            callback_data='пр_выполненной_брони-' + str(book.get('id'))
                        )
                    )
    mes_text = lng(user_id).get('mng_booking_done_footer_text').format(
        true_booking_count=len(booking_true)
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu'
        ),
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


def cancel_booking_menu(c):
    user_id = c.from_user.id
    booking_true = get_booking('cancel_booking')
    keyboard = types.InlineKeyboardMarkup()
    if booking_true:
        for book in booking_true:
            if book.get('hard_reise') == 'no_hard':
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('book_btn').format(
                            dir_out=book.get('direction_out'),
                            dir_in=book.get('direction')
                        ),
                        callback_data='пр_отмененной_брони-' + str(book.get('id'))
                    )
                )
            else:
                hard = str_to_array(book.get('hard_reise')).get('type')
                if hard == 'rew':
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('rew_book_btn').format(
                                dir_out=book.get('direction_out'),
                                dir_in=book.get('direction')
                            ),
                            callback_data='пр_отмененной_брони-' + str(book.get('id'))
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=lng(user_id).get('hard_reise_btn').format(
                                booking_id=book.get('id')
                            ),
                            callback_data='пр_отмененной_брони-' + str(book.get('id'))
                        )
                    )
    mes_text = lng(user_id).get('mng_booking_cancel_footer_text').format(
        true_booking_count=len(booking_true)
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu'
        ),
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


def mng_asks_menu(c):
    user_id = c.from_user.id
    mes_text = lng(user_id).get('mng_asks_menu_text').format(
        asks_count=len(get_booking('ask')),
        done_asks_count=len(get_booking('done_ask'))
    )
    asks = get_booking('ask')
    keyboard = types.InlineKeyboardMarkup()
    if asks:
        for ask in asks:
            plane = plane_info(ask.get('plane_id')).get('plane')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=plane,
                    callback_data='просмотр_заявки-' + str(ask.get('id'))
                )
            )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('mng_book_done_btn'),
            callback_data='выполненные_заявки'),
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu')
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def done_asks_menu(c):
    user_id = c.from_user.id
    asks_done = get_booking('done_ask')
    keyboard = types.InlineKeyboardMarkup()
    if asks_done:
        for ask in asks_done:
            plane = plane_info(ask.get('plane_id')).get('plane')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=plane,
                    callback_data='пр_выполненной_заявки-' + str(ask.get('id'))
                )
            )
    mes_text = lng(user_id).get('mng_ask_done_footer_text').format(
        done_ask_count=len(asks_done)
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu'
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


def user_plane_cat_menu(c):
    pass


def menu_book_edited(message, booking_id):
    user_id = message.from_user.id
    book = get_user_booking_by_id(user_id, booking_id)
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
    keyboard = types.InlineKeyboardMarkup()
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
            text=lng(user_id).get('back_to_menu_btn'),
            callback_data='menu'
        )
    )
    msg = bot.send_message(
        message.chat.id,
        text=lng(user_id).get('edited'),
        parse_mode='html')
    msg_count(user_id, user_id, msg.message_id)
    msg = bot.send_message(
        message.chat.id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
    msg_count(user_id, user_id, msg.message_id)
