# -*- coding: utf-8 -*-
from dbclasses import Lang
from lang import en, ru


def get_user_lang(user_id):
    lang = 0
    try:
        lang = Lang.get(Lang.user_id == user_id).lang
    except:
        Lang.create(user_id=user_id)
    return lang


def lng(user_id):
    if get_user_lang(user_id):
        language = en
    else:
        language = ru
    return language
