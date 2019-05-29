# -*- coding: utf-8 -*-
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar
import pytz
from config import TIMEZONE


def create_callback_data(action, year, month, day, cb=None):
    if cb:
        return ';'.join([action, str(year), str(month), str(day), cb])
    else:
        return ';'.join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    return data.split(';')


def create_calendar(year=None, month=None, cb=None):
    now = datetime.datetime.now(pytz.timezone(TIMEZONE))
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    month_name = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }
    data_ignore = create_callback_data('IGNORE', year, month, 0)
    keyboard = InlineKeyboardMarkup(row_width=7)
    keyboard.add(InlineKeyboardButton(
        month_name[month] + ' ' + str(year), callback_data=data_ignore))
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    keyboard.add(*[InlineKeyboardButton(day, callback_data=data_ignore) for day in weekdays])
    my_calendar = calendar.monthcalendar(year, month)
    row = []
    for week in my_calendar:
        for day in week:
            if(day == 0):
                row.append(InlineKeyboardButton(
                    ' ', callback_data=data_ignore))
            else:
                if cb:
                    row.append(InlineKeyboardButton(
                        str(day), callback_data=create_callback_data('DAY', year, month, day, cb)))
                else:
                    row.append(InlineKeyboardButton(
                        str(day), callback_data=create_callback_data('DAY', year, month, day)))
    keyboard.add(*row)
    if cb:
        keyboard.add(
            InlineKeyboardButton(
                '<',
                callback_data=create_callback_data('PREV-MONTH', year, month, day, cb)),
            InlineKeyboardButton(
                '>',
                callback_data=create_callback_data('NEXT-MONTH', year, month, day, cb))
        )
    else:
        keyboard.add(
            InlineKeyboardButton(
                '<',
                callback_data=create_callback_data('PREV-MONTH', year, month, day)),
            InlineKeyboardButton(
                '>',
                callback_data=create_callback_data('NEXT-MONTH', year, month, day))
        )
    return keyboard
