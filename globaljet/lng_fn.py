# -*- coding: utf-8 -*-
import sqlite3
from config import ADMIN
from botutils import admin_info, user_info
from lang import en, ru


def base_connect():
    """
    Точка входа подключение к базе
    """
    connection = sqlite3.connect('database/jg_base.db')
    return connection


def lng(user_id):
    language = ru
    if user_id in ADMIN:
        connection = base_connect()
        with connection:
            cursor = connection.cursor()
            sql = 'SELECT lang FROM suadm WHERE user_id = ?'
            cursor.execute(sql, ([user_id]))
            lang = cursor.fetchone()
            lang = lang[0]
        connection.close()
        if lang:
            language = en
        else:
            language = ru
    else:
        user = user_info(user_id)
        if user:
            ulang = user.get('lang')
            if ulang:
                language = en
            else:
                language = ru
        else:
            user = admin_info(user_id)
            if user:
                ulang = user.get('lang')
                if ulang:
                    language = en
                else:
                    language = ru
            else:
                language = ru
    return language
