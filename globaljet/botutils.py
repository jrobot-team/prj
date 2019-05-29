# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from datetime import date as _date

import pytz
import telebot

from base_creator import (Admin, Booking, BookingBase, MsgCount, Plane, Temper,
                          TempUserCatPlanes, User)
from config import TIMEZONE, TOKEN

# telegram bot api
bot = telebot.TeleBot(TOKEN)


class Basedate(object):
    def __init__(self, tzone=TIMEZONE):
        self.tz = tzone

    def date_hms(self):
        """ Возвращает год месяц день час минута секунда """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

    def date_mdh(self):
        """ Возвращает месяц день час минута секунда """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%m-%d %H:%M:%S')

    def date(self):
        """ Возвращает год месяц день """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d')

    def delta(self, days):
        """Отнимаем дни"""
        dt = datetime.now(pytz.timezone(self.tz))
        delta = dt + timedelta(days=days)
        return datetime.strftime(delta, '%Y-%m-%d')


def date_revers(date):
    date = str(date).split(' ')
    data = date[0]
    time = date[1]
    data = data.split('-')
    year = data[0]
    month = data[1]
    day = data[2]
    to_ret = '{day}.{month}.{year} {time}'.format(
        day=day,
        month=month,
        year=year,
        time=time
    )
    return to_ret


def get_msg_count(user_id):
    try:
        count = {
            'id': MsgCount.get(MsgCount.user_id == user_id).id,
            'user_id': user_id,
            'chat_id': user_id,
            'message_id': MsgCount.get(MsgCount.user_id == user_id).message_id
        }
    except:
        count = None
    return count


def msg_count(user_id, chat_id, message_id):
    count = get_msg_count(user_id)
    if count:
        MsgCount.delete().where(MsgCount.user_id == user_id).execute()
    MsgCount.create(
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id)


def msg_deleter(chat_id, message_id):
    count = 10
    msg_id = get_msg_count(chat_id)
    if msg_id:
        msg_id = msg_id.get('message_id')
    while count:
        message_id -= 1
        try:
            bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        except:
            try:
                message_id -= 1
                bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_id
                )
            except:
                count -= 1
                if count == 1:
                    break


def array_to_str(array):
    string = json.dumps(array, ensure_ascii=False)
    return string


def str_to_array(string):
    array = json.loads(string)
    return array


def replacer(text, rep=None):
    """ Ломаем HTML теги в тексте
    функция принимает текст и список типа [['<', '|']] """
    if rep is None:
        rep = [
            ['<', '⬅️'],
            ['>', '➡️'],
            ['/', '|'],
            ["'", "`"],
            ['"', '`'],
            ['\\', '|']]
    for i, r in rep:
        text = text.replace(i, r)
    return text


def make_admin(user_id, role):
    Admin.create(user_id=user_id, role=role)


def get_admins(role=None):
    if role:
        query = Admin.select().where(Admin.role == role)
    else:
        query = Admin.select()
    admins = []
    admins_uid = []
    for admin in query:
        admins_uid.append(admin.user_id)
        admins.append(
            {
                'id': admin.id,
                'user_id': admin.user_id,
                'role': admin.role,
                'status': admin.status,
                'lang': admin.lang
            }
        )
    return admins, admins_uid


def admin_info(user_id):
    try:
        admin = {
            'id': Admin.get(Admin.user_id == user_id).id,
            'user_id': user_id,
            'role': Admin.get(Admin.user_id == user_id).role,
            'status': Admin.get(Admin.user_id == user_id).status,
            'lang': Admin.get(Admin.user_id == user_id).lang
        }
    except:
        admin = None
    return admin


def reg_user(user_id, username, lang=0):
    if user_info(user_id):
        pass
    else:
        User.create(user_id=user_id, username=username, lang=lang)


def user_info(user_id):
    try:
        user = {
            'id': User.get(User.user_id == user_id).id,
            'user_id': user_id,
            'username': User.get(User.user_id == user_id).username,
            'fio': User.get(User.user_id == user_id).fio,
            'phone': User.get(User.user_id == user_id).phone,
            'register': User.get(User.user_id == user_id).register,
            'lang': User.get(User.user_id == user_id).lang
        }
    except:
        user = None
    return user


def upd_user_lang(user_id, lang):
    User.update(lang=lang).where(User.user_id == user_id).execute()


def upd_user_fio(user_id, fio):
    User.update(fio=fio).where(
        User.user_id == user_id).execute()


def upd_user_phone(user_id, phone):
    User.update(phone=phone, register=1).where(
        User.user_id == user_id).execute()


def make_plane(plane):
    Plane.create(plane=plane)


def upd_plane_seats(plane_id, seats_in):
    Plane.update(seats_in=seats_in).where(
        Plane.id == plane_id).execute()


def upd_plane_picture(plane_id, picture):
    Plane.update(picture=picture).where(
        Plane.id == plane_id).execute()


def upd_plane_producer(plane_id, producer):
    Plane.update(producer=producer).where(
        Plane.id == plane_id).execute()


def upd_plane_description(plane_id, description):
    Plane.update(description=description).where(
        Plane.id == plane_id).execute()


def upd_plane_producer_url(plane_id, producer_url):
    Plane.update(producer_url=producer_url).where(
        Plane.id == plane_id).execute()


def upd_plane_flight_time(plane_id, flight_time):
    Plane.update(flight_time=flight_time).where(
        Plane.id == plane_id).execute()


def upd_plane_fltime(plane_id, fltime):
    Plane.update(flight_time=fltime).where(
        Plane.id == plane_id).execute()


def get_planes(fltime=10, seats=18):
    query = Plane.select().where(Plane.fltime == fltime, Plane.seats_in >= seats)
    planes = []
    for plane in query:
        planes.append(
            {
                'id': plane.id,
                'plane': plane.plane,
                'producer': plane.producer,
                'seats_in': plane.seats_in,
                'picture': plane.picture,
                'description': plane.description,
                'producer_url': plane.producer_url,
                'flight_time': plane.flight_time,
                'fltime': plane.fltime
            }
        )
    return planes


def plane_info(plane_id):
    try:
        plane = {
            'id': plane_id,
            'plane': Plane.get(Plane.id == plane_id).plane,
            'producer': Plane.get(Plane.id == plane_id).producer,
            'seats_in': Plane.get(Plane.id == plane_id).seats_in,
            'picture': Plane.get(Plane.id == plane_id).picture,
            'description': Plane.get(Plane.id == plane_id).description,
            'producer_url': Plane.get(Plane.id == plane_id).producer_url,
            'flight_time': Plane.get(Plane.id == plane_id).flight_time,
            'fltime': Plane.get(Plane.id == plane_id).fltime
        }
    except:
        plane = None
    return plane


def make_booking_base(date, plane_id, seats_off):
    BookingBase.create(
        date=date,
        plane_id=plane_id,
        seats_of=seats_off
    )


def upd_booking_base_direction(booking_base_id, direction):
    BookingBase.update(direction=direction).where(
        BookingBase.id == booking_base_id).execute()


def upd_booking_base_price(booking_base_id, price):
    BookingBase.update(price=price).where(
        BookingBase.id == booking_base_id).execute()


def upd_booking_base_flight_time(booking_base_id, flight_time):
    BookingBase.update(flight_time=flight_time).where(
        BookingBase.id == booking_base_id).execute()


def upd_booking_base_status(booking_base_id, status):
    BookingBase.update(status=status).where(
        BookingBase.id == booking_base_id).execute()


def booking_base_info(booking_base_id):
    try:
        booking_base = {
            'id': booking_base_id,
            'date': BookingBase.get(
                BookingBase.id == booking_base_id).date,
            'plane_id': BookingBase.get(
                BookingBase.id == booking_base_id).plane_id,
            'seats_off': BookingBase.get(
                BookingBase.id == booking_base_id).seats_off,
            'direction': BookingBase.get(
                BookingBase.id == booking_base_id).direction,
            'price': BookingBase.get(
                BookingBase.id == booking_base_id).price,
            'flight_time': BookingBase.get(
                BookingBase.id == booking_base_id).flight_time,
            'status': BookingBase.get(
                BookingBase.id == booking_base_id).status,
        }
    except:
        booking_base = None
    return booking_base


def get_booking_bases(status=0):
    query = BookingBase.select().where(BookingBase.status == status)
    booking_bases = []
    for booking_base in query:
        booking_bases.append(
            {
                'id': booking_base.id,
                'date': booking_base.date,
                'plane_id': booking_base.plane_id,
                'seats_off': booking_base.seats_off,
                'direction': booking_base.direction,
                'price': booking_base.price,
                'flight_time': booking_base.flight_time,
                'status': booking_base.status,
            }
        )
    return booking_bases


def get_asks(status='ask'):
    query = Booking.select().where(Booking.status == status)
    asks = []
    for ask in query:
        asks.append(
            {
                'id': ask.id,
                'user_id': ask.user_id,
                'price': ask.price,
                'seats': ask.seats,
                'day_to_flight': ask.day_to_flight,
                'date': date_revers(ask.date),
                'dtf_set': ask.dtf_set,
                'plane_id': ask.plane_id,
                'direction_out': ask.direction_out,
                'direction': ask.direction,
                'flight_time': ask.flight_time,
                'status': ask.status,
                'alerted': ask.alerted,
                'date_fly': ask.date_fly,
                'date_sync': ask.date_sync,
                'comment': ask.comment,
                'plane_model': ask.plane_model,
                'company': ask.company
            }
        )
    return asks


def get_temp_user_cat_planes(user_id):
    try:
        temp_user_cat_planes = {
            'id': TempUserCatPlanes.get(
                TempUserCatPlanes.user_id == user_id).id,
            'user_id': user_id,
            'seats': TempUserCatPlanes.get(
                TempUserCatPlanes.user_id == user_id).seats,
            'flight_time': TempUserCatPlanes.get(
                TempUserCatPlanes.user_id == user_id).flight_time,
            'plane_id': TempUserCatPlanes.get(
                TempUserCatPlanes.user_id == user_id).plane_id,
            'booking_id': TempUserCatPlanes.get(
                TempUserCatPlanes.user_id == user_id).booking_id,
        }
    except:
        temp_user_cat_planes = None
    return temp_user_cat_planes


def temp_user_cat_planes_seats(user_id, seats):
    if get_temp_user_cat_planes(user_id):
        TempUserCatPlanes.delete().where(TempUserCatPlanes.user_id == user_id).execute()
    TempUserCatPlanes.create(user_id=user_id, seats=seats)


def make_plane_id_temp(user_id, plane_id):
    TempUserCatPlanes.update(plane_id=plane_id).where(
        TempUserCatPlanes.user_id == user_id).execute()


def del_temp_user(user_id):
    TempUserCatPlanes.delete().where(TempUserCatPlanes.user_id == user_id).execute()


def sort_planes(user_id, fltime):
    seats = get_temp_user_cat_planes(user_id)
    if seats:
        seats = seats.get('seats')
    else:
        seats = 1
    if seats >= 18:
        seats = 18
    planes = get_planes(fltime=fltime, seats=seats)
    e = True
    while e:
        if planes:
            e = False
            break
        else:
            fltime = fltime + 1
            planes = get_planes(fltime=fltime, seats=seats)
    return planes


def make_ask_by_user(user_id):
    date = Basedate().date_hms()
    day_to_flight = Basedate().date()
    temp = get_temp_user_cat_planes(user_id)
    seats = temp.get('seats')
    plane_id = temp.get('plane_id')
    del_temp_user(user_id)
    Booking.create(
        user_id=user_id,
        seats=seats,
        date=date,
        day_to_flight=day_to_flight,
        plane_id=plane_id
    )
    try:
        ask_id = Booking.get(Booking.user_id == user_id, Booking.date == date).id
    except:
        ask_id = 0
    return ask_id


def get_booking(status, period=False, dtf=False):
    if period:
        if period == 'day':
            day = Basedate().date()
            query = Booking.select().where(Booking.status == status, Booking.day_to_flight == day)
        if period == 'week':
            day = Basedate().delta(days=-7)
            query = Booking.select().where(Booking.status == status, Booking.day_to_flight >= day)
        if period == 'month':
            day = Basedate().delta(days=-30)
            query = Booking.select().where(Booking.status == status, Booking.day_to_flight >= day)
    else:
        if dtf:
            query = Booking.select().where(Booking.status == status, Booking.dtf_set == 1)
        else:
            query = Booking.select().where(Booking.status == status)
    booking = []
    for book in query:
        if dtf:
            booking.append(
                {
                    'id': book.id,
                    'user_id': book.user_id,
                    'price': book.price,
                    'seats': book.seats,
                    'day_to_flight': book.day_to_flight,
                    'date': book.date,
                    'dtf_set': book.dtf_set,
                    'plane_id': book.plane_id,
                    'direction_out': book.direction_out,
                    'direction': book.direction,
                    'flight_time': book.flight_time,
                    'status': book.status,
                    'alerted': book.alerted,
                    'hours_alert': book.hours_alert,
                    'date_fly': book.date_fly,
                    'date_sync': book.date_sync,
                    'comment': book.comment,
                    'plane_model': book.plane_model,
                    'company': book.company,
                    'price_char': book.price_char,
                    'hard_reise': book.hard_reise
                }
            )
        else:
            booking.append(
                {
                    'id': book.id,
                    'user_id': book.user_id,
                    'price': book.price,
                    'seats': book.seats,
                    'day_to_flight': book.day_to_flight,
                    'date': date_revers(book.date),
                    'dtf_set': book.dtf_set,
                    'plane_id': book.plane_id,
                    'direction_out': book.direction_out,
                    'direction': book.direction,
                    'flight_time': book.flight_time,
                    'status': book.status,
                    'alerted': book.alerted,
                    'hours_alert': book.hours_alert,
                    'date_fly': book.date_fly,
                    'date_sync': book.date_sync,
                    'comment': book.comment,
                    'plane_model': book.plane_model,
                    'company': book.company,
                    'price_char': book.price_char,
                    'hard_reise': book.hard_reise
                }
            )
    return booking


def get_users():
    query = User.select()
    users = []
    for user in query:
        users.append(
            {
                'id': user.id,
                'user_id': user.user_id,
                'username': user.username,
                'fio': user.fio,
                'phone': user.phone,
                'register': user.register,
                'lang': user.lang
            }
        )
    return users


def get_user_booking(user_id, status):
    query = Booking.select().where(Booking.user_id == user_id, Booking.status == status)
    booking = []
    for book in query:
        booking.append(
            {
                'id': book.id,
                'user_id': book.user_id,
                'price': book.price,
                'seats': book.seats,
                'day_to_flight': book.day_to_flight,
                'date': date_revers(book.date),
                'dtf_set': book.dtf_set,
                'plane_id': book.plane_id,
                'direction_out': book.direction_out,
                'direction': book.direction,
                'flight_time': book.flight_time,
                'status': book.status,
                'alerted': book.alerted,
                'date_fly': book.date_fly,
                'date_sync': book.date_sync,
                'comment': book.comment,
                'plane_model': book.plane_model,
                'company': book.company,
                'price_char': book.price_char,
                'hard_reise': book.hard_reise
            }
        )
    return booking


def get_user_all_booking(user_id):
    query = Booking.select().where(Booking.user_id == user_id)
    booking = []
    for book in query:
        booking.append(
            {
                'id': book.id,
                'user_id': book.user_id,
                'price': book.price,
                'seats': book.seats,
                'day_to_flight': book.day_to_flight,
                'date': date_revers(book.date),
                'dtf_set': book.dtf_set,
                'plane_id': book.plane_id,
                'direction_out': book.direction_out,
                'direction': book.direction,
                'flight_time': book.flight_time,
                'status': book.status,
                'alerted': book.alerted,
                'date_fly': book.date_fly,
                'date_sync': book.date_sync,
                'comment': book.comment,
                'plane_model': book.plane_model,
                'company': book.company,
                'price_char': book.price_char,
                'hard_reise': book.hard_reise
            }
        )
    return booking


def get_user_booking_by_id(user_id, booking_id):
    booking = {
        'id': booking_id,
        'user_id': user_id,
        'price': Booking.get(Booking.id == booking_id).price,
        'seats': Booking.get(Booking.id == booking_id).seats,
        'day_to_flight': Booking.get(Booking.id == booking_id).day_to_flight,
        'date': date_revers(Booking.get(Booking.id == booking_id).date),
        'dtf_set': Booking.get(Booking.id == booking_id).dtf_set,
        'plane_id': Booking.get(Booking.id == booking_id).plane_id,
        'direction_out': Booking.get(Booking.id == booking_id).direction_out,
        'direction': Booking.get(Booking.id == booking_id).direction,
        'flight_time': Booking.get(Booking.id == booking_id).flight_time,
        'status': Booking.get(Booking.id == booking_id).status,
        'alerted': Booking.get(Booking.id == booking_id).alerted,
        'date_fly': Booking.get(Booking.id == booking_id).date_fly,
        'date_sync': Booking.get(Booking.id == booking_id).date_sync,
        'comment': Booking.get(Booking.id == booking_id).comment,
        'plane_model': Booking.get(Booking.id == booking_id).plane_model,
        'company': Booking.get(Booking.id == booking_id).company,
        'price_char': Booking.get(Booking.id == booking_id).price_char,
        'hard_reise': Booking.get(Booking.id == booking_id).hard_reise
    }
    return booking


def make_place_from(user_id, place, date):
    day_to_flight = Basedate().date()
    Booking.create(
        user_id=user_id,
        direction_out=place,
        date=date,
        day_to_flight=day_to_flight,
        plane_id=0,
        status='booking'
    )


def edit_direction_out_fn(direction_out, booking_id):
    Booking.update(direction_out=direction_out).where(
        Booking.id == booking_id).execute()


def get_booking_id_by_date(user_id, date):
    booking_id = Booking.get(Booking.user_id == user_id, Booking.date == date).id
    return booking_id


def make_temp_booking_id(user_id, booking_id):
    if get_temp_user_cat_planes(user_id):
        TempUserCatPlanes.delete().where(TempUserCatPlanes.user_id == user_id).execute()
    TempUserCatPlanes.create(user_id=user_id, booking_id=booking_id)


def make_to_direction_place_fn(direction, booking_id):
    Booking.update(direction=direction).where(
        Booking.id == booking_id).execute()


def make_date_fly_fn(user_id, booking_id, date_fly):
    Booking.update(date_fly=date_fly).where(
        Booking.id == booking_id).execute()


def make_seats_booking_fn(user_id, booking_id, seats):
    Booking.update(seats=seats).where(
        Booking.id == booking_id).execute()
    if get_temp_user_cat_planes(user_id):
        TempUserCatPlanes.delete().where(TempUserCatPlanes.user_id == user_id).execute()


def make_seats_booking_edt(user_id, booking_id, seats):
    Booking.update(seats=seats).where(
        Booking.id == booking_id).execute()


def make_comment(user_id, booking_id, comment):
    Booking.update(comment=comment).where(
        Booking.id == booking_id).execute()


def cancel_booking(booking_id):
    Booking.delete().where(Booking.id == booking_id).execute()


def get_booking_info(booking_id):
    try:
        booking = {
            'id': booking_id,
            'user_id': Booking.get(Booking.id == booking_id).user_id,
            'price': Booking.get(Booking.id == booking_id).price,
            'seats': Booking.get(Booking.id == booking_id).seats,
            'day_to_flight': Booking.get(Booking.id == booking_id).day_to_flight,
            'date': date_revers(Booking.get(Booking.id == booking_id).date),
            'dtf_set': Booking.get(Booking.id == booking_id).dtf_set,
            'plane_id': Booking.get(Booking.id == booking_id).plane_id,
            'direction_out': Booking.get(Booking.id == booking_id).direction_out,
            'direction': Booking.get(Booking.id == booking_id).direction,
            'flight_time': Booking.get(Booking.id == booking_id).flight_time,
            'status': Booking.get(Booking.id == booking_id).status,
            'alerted': Booking.get(Booking.id == booking_id).alerted,
            'hours_alert': Booking.get(Booking.id == booking_id).hours_alert,
            'date_fly': Booking.get(Booking.id == booking_id).date_fly,
            'date_sync': Booking.get(Booking.id == booking_id).date_sync,
            'comment': Booking.get(Booking.id == booking_id).comment,
            'plane_model': Booking.get(Booking.id == booking_id).plane_model,
            'company': Booking.get(Booking.id == booking_id).company,
            'price_char': Booking.get(Booking.id == booking_id).price_char,
            'hard_reise': Booking.get(Booking.id == booking_id).hard_reise
        }
    except:
        booking = None
    return booking


def get_tmp(user_id):
    try:
        tmp = {
            'id': Temper.get(Temper.user_id == user_id).id,
            'user_id': user_id,
            'temp_id': Temper.get(Temper.user_id == user_id),
            'temp': Temper.get(Temper.user_id == user_id).temp,
        }
    except:
        tmp = None
    return tmp


def make_tmp(user_id, temp_id=0, temp=''):
    if get_tmp(user_id):
        Temper.delete().where(Temper.user_id == user_id).execute()
    Temper.create(user_id=user_id, temp_id=temp_id, temp=temp)


def date_actualaiser(date_to_fly, booking_id):
    try:
        date_to_fly = date_to_fly.split(' ')
        year = date_to_fly[2]
        month = date_to_fly[1]
        day = date_to_fly[0]
        if month[0] == '0':
            month = month[1:]
        if day[0] == '0':
            day = day[1:]
        Booking.update(day_to_flight=_date(int(year), int(month), int(day)), date_sync=1).where(
            Booking.id == booking_id).execute()
    except Exception as e:
        print(e)
        date_to_fly = None
    return date_to_fly


def upd_booking_set_plane(plane_model, booking_id):
    Booking.update(plane_model=plane_model).where(Booking.id == booking_id).execute()


def upd_booking_set_company(company, booking_id):
    Booking.update(company=company).where(Booking.id == booking_id).execute()


def upd_booking_set_price(price, booking_id):
    price = price.replace(',', '.')
    Booking.update(price_char=price).where(Booking.id == booking_id).execute()


def date_time_updater(date_time, booking_id):
    try:
        date_time = date_time.split(' ')
        date = date_time[0].split('.')
        time = date_time[1]
        day = date[0]
        month = date[1]
        year = date[2].replace(' ', '')
        hour = time.split(':')[0]
        minutes = time.split(':')[1]
        to_base_date_time = '{year}-{month}-{day} {hour}:{minutes}:00'.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minutes=minutes
        )
        Booking.update(date=to_base_date_time, dtf_set=1, date_sync=1).where(
            Booking.id == booking_id).execute()
    except Exception as e:
        print(e)
        to_base_date_time = None
    return to_base_date_time


def upd_book_status(status, booking_id):
    Booking.update(status=status).where(Booking.id == booking_id).execute()


def make_hard_reise(user_id, hard_reise):
    reise = {
        'type': 'hard',
        'comment': hard_reise
    }
    reise = array_to_str(reise)
    d = Basedate().date()
    dt = Basedate().date_hms()
    Booking.create(
        user_id=user_id,
        hard_reise=reise,
        date=dt,
        day_to_flight=d,
        status='booking')
    booking_id = Booking.get(Booking.date == dt).id
    return booking_id


def make_rewinder_reise(user_id, rew_reise):
    reise = {
        'type': 'rew',
        'comment': rew_reise
    }
    reise = array_to_str(reise)
    d = Basedate().date()
    dt = Basedate().date_hms()
    Booking.create(
        user_id=user_id,
        direction_out=rew_reise,
        hard_reise=reise,
        date=dt,
        day_to_flight=d,
        plane_id=0,
        status='booking')
    booking_id = Booking.get(Booking.date == dt).id
    return booking_id


def change_lang(user_id):
    admins = get_admins()
    if user_id in admins[1]:
        language = admin_info(user_id).get('lang')
        if language:
            Admin.update(lang=0).where(Admin.user_id == user_id).execute()
        else:
            Admin.update(lang=1).where(Admin.user_id == user_id).execute()
    else:
        language = user_info(user_id).get('lang')
        if language:
            User.update(lang=0).where(User.user_id == user_id).execute()
        else:
            User.update(lang=1).where(User.user_id == user_id).execute()


def get_user_current_lang(user_id):
    admins = get_admins()
    if user_id in admins[1]:
        language = admin_info(user_id).get('lang')
    else:
        language = user_info(user_id).get('lang')
    return language
