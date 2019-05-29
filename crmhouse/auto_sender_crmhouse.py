# -*- coding: utf-8 -*-
import time

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
import schedule
from agent_utils import get_consumer_info, get_stadi_info
from auto_sender_utils import (get_agent_prepares, get_agent_task,
                               get_clients_avans, get_clients_dog_do,
                               get_clients_meets, get_clients_pokaz,
                               get_clients_rek, get_clients_sdelka,
                               get_consumers_count, set_sended_agent_task)
from boss_utils import admininfo, get_admins
from bot_utils import Basedate
from lang import ru
from otchets_agents import agent_stadies
from user_utils import get_users_by_role

bot = telebot.TeleBot(config.token)


def btn(text, cb):
    button = InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button


def admin_otchet(diap='week'):
    for user in get_admins():
        uid = admininfo(user.get('user_id')).get('id')
        now = Basedate().date_mdh_ru()
        counts = get_consumers_count(diap)
        meets = get_clients_meets(uid, diap)
        dogs = get_clients_dog_do(uid, diap)
        reks = get_clients_rek(uid, diap)
        pok = get_clients_pokaz(uid, diap)
        avans = get_clients_avans(uid, diap)
        sdelka = get_clients_sdelka(uid, diap)
        if diap == 'week':
            mes_text = ru.get('boss_otchet_monday').format(
                date=now,
                sellers=counts.get('sellers'),
                new_sellers=counts.get('new_sellers'),
                buyers=counts.get('buyers'),
                new_buyers=counts.get('new_buyers'),
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
        else:
            mes_text = ru.get('boss_otchet_day').format(
                date=now,
                sellers=counts.get('sellers'),
                new_sellers=counts.get('new_sellers'),
                buyers=counts.get('buyers'),
                new_buyers=counts.get('new_buyers'),
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
                ru.get('agents_otchets'),
                'отчеты%' + diap
            )
        )
        try:
            bot.send_message(
                user.get('user_id'),
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        except:
            pass


def tasker():
    agents = get_users_by_role(role='agent')
    for agent in agents:
        tasks = get_agent_task(agent.get('user_id'))
        prepares = get_agent_prepares(agent.get('user_id'))
        for task in tasks:
            if task.get('sid') == 2:
                step_txt = ru.get('res_meet')
            if task.get('sid') == 4:
                step_txt = ru.get('res_res')
            if task.get('sid') == 6:
                step_txt = ru.get('res_pred_pod')
            if task.get('sid') == 7:
                step_txt = ru.get('res_zap_rek')
            if task.get('sid') == 11:
                step_txt = ru.get('res_pokaza')
            if task.get('sid') == 13:
                step_txt = ru.get('res_avans')
            if task.get('sid') == 13:
                step_txt = ru.get('res_avans')
            keyboard = InlineKeyboardMarkup()
            stinfo = get_stadi_info(task.get('sid'))
            step_txt = ru.get('res_meet')
            cinfo = get_consumer_info(task.get('consumer_id'))
            if get_consumer_info(task.get('consumer_id')).get('role') == 'seller':
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
            substeps = stinfo.get('details')
            for subst in substeps:
                if task.get('sid') == 11 and subst.get('id') == 4:
                    cstatus = get_consumer_info(task.get('consumer_id')).get('status')
                    if cstatus:
                        pass
                    else:
                        cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                            cid=task.get('consumer_id'),
                            sid=task.get('sid'),
                            subsid=subst.get('id'),
                            subsubsid=0,
                            step=1
                        )
                        keyboard.add(
                            btn(subst.get('sub_st_name'), cb)
                        )
                else:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=task.get('consumer_id'),
                        sid=task.get('sid'),
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        btn(subst.get('sub_st_name'), cb)
                    )
            try:
                bot.send_message(
                    agent.get('user_id'),
                    text=mes_text,
                    parse_mode='html',
                    reply_markup=keyboard)
            except:
                pass
            set_sended_agent_task(task.get('id'), sended=2)
        for prep in prepares:
            consumer_id = prep.get('consumer_id')
            sid = prep.get('sid')
            agent_id = prep.get('agent_id')
            agent_stadies(consumer_id, sid, 0, 0, 0, agent_id=agent_id)
            set_sended_agent_task(prep.get('task_id'), sended=1)


schedule.every(1).minutes.do(tasker)
schedule.every().monday.at('07:00').do(admin_otchet)
schedule.every().tuesday.at('07:00').do(admin_otchet, diap='day')
schedule.every().wednesday.at('07:00').do(admin_otchet, diap='day')
schedule.every().thursday.at('07:00').do(admin_otchet, diap='day')
schedule.every().friday.at('07:00').do(admin_otchet, diap='day')


while True:
    schedule.run_pending()
    time.sleep(1)
