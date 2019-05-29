# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import pytz
from telebot.types import InlineKeyboardButton

from config import TIMEZONE


class Basedate(object):
    def __init__(self, tzone=TIMEZONE):
        self.tz = tzone

    def date_hms(self):
        """ Возвращает год месяц день час минута секунда """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

    def date_hm(self):
        """ Возвращает год месяц день час минута """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d %H:%M')

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

    def plus_one_day(self, days=1):
        """Возвращает плюс один день от текущей даты"""
        dt = datetime.now(pytz.timezone(self.tz))
        plus_one = dt + timedelta(days=days)
        return datetime.strftime(plus_one, '%d-%m-%Y %H:%M')

    def plus_hours(self, hours=None, minutes=None):
        """Прибавляем часы минуты"""
        dt = datetime.now(pytz.timezone(self.tz))
        if hours and minutes:
            plus = dt + timedelta(hours=hours, minutes=minutes)
        else:
            if hours:
                plus = dt + timedelta(hours=hours)
            else:
                plus = dt + timedelta(minutes=minutes)
        return datetime.strftime(plus, '%d-%m-%Y %H:%M')

    def now_time(self):
        """ Возвращает текущий час минуту """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%H:%M')

    def delta_time_start_to_end(self, date_start, hours='01', minutes='00'):
        data = str(date_start).split(' ')[0]
        dtime = str(date_start).split(' ')[1]
        if '-' in data:
            day = data.split('-')[0]
            if len(day) == 4:
                year = data.split('-')[0]
                month = data.split('-')[1]
                day = data.split('-')[2]
            else:
                month = data.split('-')[1]
                year = data.split('-')[2]
        else:
            day = data.split('.')[0]
            month = data.split('.')[1]
            year = data.split('.')[2]
        hrs = dtime.split(':')[0]
        mnts = dtime.split(':')[1]
        date_start_obj = datetime(
            int(year),
            int(month),
            int(day),
            int(hrs),
            int(mnts)
        )
        response = date_start_obj + timedelta(hours=int(hours), minutes=int(minutes))
        return datetime.strftime(response, '%Y-%m-%d %H:%M')


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


def date_revers(date):
    try:
        if '.' in str(date):
            return date
        else:
            date = str(date).split(' ')
            data = date[0]
            time = date[1]
            hour = time.split(':')[0]
            minutes = time.split(':')[1]
            data = data.split('-')
            year = data[0]
            if len(year) == 4:
                month = data[1]
                day = data[2]
            else:
                day = data[0]
                month = data[1]
                year = data[2]
            to_ret = '{day}.{month}.{year} {hour}:{minutes}'.format(
                day=day,
                month=month,
                year=year,
                hour=hour,
                minutes=minutes
            )
    except:
        try:
            date = str_to_array(date)
            date = date[0]
        except:
            date = date[0]
        try:
            date = str(date).split('.')
            year = date[0]
            month = date[1]
            day = date[2]
            to_ret = '{day}.{month}.{year}'.format(
                day=day,
                month=month,
                year=year
            )
        except:
            try:
                date = str_to_array(date)
                date = date[0]
            except:
                pass
            date = str(date).replace("']", "").replace("['", "").split('-')
            year = date[0]
            month = date[1]
            day = date[2]
            to_ret = '{day}.{month}.{year}'.format(
                day=day,
                month=month,
                year=year
            )
    return to_ret


def to_base_date_cheker(dates):
    chek = str(dates)
    chek = chek.split(' ')
    if '.' in chek[0]:
        data = chek[0].split('.')
        if len(data[0]) <= 2:
            year = int(data[2])
            month = int(data[1])
            day = int(data[0])
            hour = int(chek[1].split(':')[0])
            minutes = int(chek[1].split(':')[1])
            date_cheked = datetime(
                year,
                month,
                day,
                hour,
                minutes
            )
        else:
            year = int(data[0])
            month = int(data[1])
            day = int(data[2])
            hour = int(chek[1].split(':')[0])
            minutes = int(chek[1].split(':')[1])
            date_cheked = datetime(
                year,
                month,
                day,
                hour,
                minutes
            )
    elif '-' in chek[0]:
        data = chek[0].split('-')
        if len(data[0]) <= 2:
            year = int(data[2])
            month = int(data[1])
            day = int(data[0])
            hour = int(chek[1].split(':')[0])
            minutes = int(chek[1].split(':')[1])
            date_cheked = datetime(
                year,
                month,
                day,
                hour,
                minutes
            )
        else:
            year = int(data[0])
            month = int(data[1])
            day = int(data[2])
            hour = int(chek[1].split(':')[0])
            minutes = int(chek[1].split(':')[1])
            date_cheked = datetime(
                year,
                month,
                day,
                hour,
                minutes
            )
    else:
        dates = date_cheked
    return date_cheked


def btn(text, cb):
    button = InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button
