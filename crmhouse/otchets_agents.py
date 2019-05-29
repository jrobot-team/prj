# -*- coding: utf-8 -*-
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from auto_sender_utils import (get_clients_avans, get_clients_dog_do,
                               get_clients_meets, get_clients_pokaz,
                               get_clients_rek, get_clients_sdelka)
from boss_utils import admininfo, get_agents
from bot_utils import Basedate
from lang import ru
from agent_utils import get_stadi_info, get_consumer_info, get_client_stepname
from agent_menu import client_in_stadi_detail_menu

# telegram bot api
bot = telebot.TeleBot(config.token)


def btn(text, cb):
    button = InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button


def agents_boss_list(c, diap):
    user_id = c.from_user.id
    keyboard = InlineKeyboardMarkup()
    agents = get_agents(user_id)
    if agents:
        mes_text = ru.get('boss_agents_otchets')
        for agent in agents:
            keyboard.add(
                btn(
                    agent.get('name'),
                    'OA+' + str(agent.get('user_id')) + '+' + diap
                )
            )
    else:
        mes_text = ru.get('boss_agents_no_agents')
    keyboard.add(
        btn(
            ru.get('to_menu_btn'),
            'menu'
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def agent_otchet(c, agent_id, diap):
    uid = admininfo(c.from_user.id).get('id')
    now = Basedate().date_mdh_ru()
    meets = get_clients_meets(uid, diap, agent_id=agent_id)
    dogs = get_clients_dog_do(uid, diap, agent_id=agent_id)
    reks = get_clients_rek(uid, diap, agent_id=agent_id)
    pok = get_clients_pokaz(uid, diap, agent_id=agent_id)
    avans = get_clients_avans(uid, diap, agent_id=agent_id)
    sdelka = get_clients_sdelka(uid, diap, agent_id=agent_id)
    mes_text = ru.get('boss_otchet_agent').format(
        date=now,
        sellers_meets=meets.get('meets'),
        sellers_meets_done=meets.get('meets_done'),
        dog_done=dogs.get('bdogs'),
        rek_do=reks.get('reks'),
        buyers_pokaz=pok.get('pokaz'),
        buyers_pokaz_done=pok.get('pokaz_done'),
        buyers_dog_done=dogs.get('sdogs'),
        avans_get=avans.get('avans'),
        sdelki_done=sdelka.get('sdelka')
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        btn(
            ru.get('back_p'),
            'отчеты%' + diap
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def agent_stadies(consumer_id, sid, subsid, subsubsid, step, c=None, message=None, agent_id=None):
    stinfo = get_stadi_info(sid)
    cinfo = get_consumer_info(consumer_id)
    substeps = stinfo.get('details')
    updsubsid = subsid + 1
    if updsubsid > len(substeps):
        sid = get_client_stepname(consumer_id)
        client_in_stadi_detail_menu(consumer_id, sid, c=c, message=message)
    else:
        keyboard = InlineKeyboardMarkup()
        for subst in substeps:
            if subst.get('id') == updsubsid:
                step_txt = subst.get('sub_st_name')
                step_btn = subst.get('do')
        cb = 'AGS|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
            cid=consumer_id,
            sid=sid,
            subsid=updsubsid,
            subsubsid=0,
            step=1
        )
        keyboard.add(
            btn(
                step_btn,
                cb
            )
        )
        if get_consumer_info(consumer_id).get('role') == 'seller':
            mes_text = ru.get('stadi_execute_menu_text_seller').format(
                stadi_name=stinfo.get('name'),
                name=cinfo.get('name'),
                phone=cinfo.get('phone'),
                address=cinfo.get('address'),
                step_text=step_txt
            )
        else:
            mes_text = ru.get('stadi_execute_menu_text_buyer').format(
                stadi_name=stinfo.get('name'),
                name=cinfo.get('name'),
                phone=cinfo.get('phone'),
                step_text=step_txt
            )
        if agent_id:
            bot.send_message(
                agent_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            if message:
                bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
            else:
                bot.edit_message_text(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
