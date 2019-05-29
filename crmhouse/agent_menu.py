# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from agent_utils import (
    consumer_move_to_base, create_client_step, create_st, del_consumer_tasks,
    filter_by_price_diap, get_agent_client_stadies, get_agent_consumers,
    get_agent_task_info, get_agent_tasks, get_client_stepname,
    get_clients_in_stadi, get_consumers_by_filter, get_consumers_rooms,
    get_current_st, get_current_task_name, get_stadi_info, price_formatter,
    upd_stadi, upd_sub_stadies)
from bot_calendar_helper import create_calendar
from bot_utils import Basedate
from consumers_utils import (buyer_update_seller_var, consumer_set_manager_id,
                             consumer_set_status, find_sellers_to_buyers,
                             get_all_towns_info, get_consumer_info,
                             get_district_info, get_districts_by_town_id,
                             get_prices_diap, get_town_by_district_id,
                             get_town_info)
from lang import ru
from paginators import paginator
from user_utils import get_user_info

# telegram bot api
bot = telebot.TeleBot(config.token)


def btn(text, cb):
    button = InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button


def agent_find_seller(consumer_id, c=None, message=None):
    cinfo = get_consumer_info(consumer_id)
    sellers = find_sellers_to_buyers(consumer_id)
    keyboard = types.InlineKeyboardMarkup()
    if sellers:
        mes_text = ru.get('find_sellers_mnu_text_sdelka_ask_variant').format(
            sellers_count=len(sellers)
        )
        for seller in sellers:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=seller.get('address'),
                    callback_data='ADD>S@B+' + str(consumer_id) + '+' + str(seller.get('id'))
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('get_find'),
                callback_data='FD-' + str(consumer_id)
            )
        )
        cb = 'agentmenu*' + cinfo.get('role')
        if cinfo.get('role') == 'seller':
            tobtn = ru.get('to_sellers')
        else:
            tobtn = ru.get('to_buyers')
        keyboard.add(
            types.InlineKeyboardButton(
                text=tobtn,
                callback_data=cb
            )
        )
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
    else:
        agent_base_view_select_town_menu('seller', c=c, message=message, fnd=consumer_id)


def agent_seller_finded_menu(consumer_id, var_id, c=None, message=None):
    cinfo = get_consumer_info(var_id)
    keyboard = types.InlineKeyboardMarkup()
    mes_text = ru.get('finded_customer_seller_detail_menu_agent_no_contacts').format(
        town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
        district=get_district_info(cinfo.get('district_id')).get('name'),
        name=cinfo.get('name'),
        address=cinfo.get('address'),
        area=cinfo.get('area'),
        house_floors=cinfo.get('info').get('house_floors'),
        floor=cinfo.get('info').get('floor'),
        rooms=int(cinfo.get('rooms')),
        price=cinfo.get('price')
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('select'),
            callback_data='SELECT&' + str(consumer_id) + '&' + str(var_id)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='FIND&' + str(consumer_id)
        )
    )
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


def agent_selected_seller_to_buyer(buyer_id, seller_id, c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    buyer_update_seller_var(buyer_id, seller_id)
    del_consumer_tasks(buyer_id)
    create_client_step(buyer_id, 'Сделка завершена', agent_id, 'buyer')
    sinfo = get_consumer_info(seller_id)
    if sinfo.get('manager_id'):
        mgid = get_current_st(seller_id, sinfo.get('manager_id')).get('id')
        upd_stadi(17, mgid)
        create_client_step(seller_id, 'Объект продан', sinfo.get('manager_id'), 'seller')
    else:
        consumer_set_manager_id(seller_id, agent_id)
        create_st(17, seller_id, agent_id)
        create_client_step(seller_id, 'Объект продан', agent_id, 'seller')
    client_in_stadi_detail_menu(buyer_id, 17, c=c, message=message)


def s_agent_stadies(consumer_id, sid, subsid, subsubsid, step, c=None, message=None, agent_id=None):
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


def task_time_menu(cbk, c=None, message=None):
    year = int(cbk.split(';')[1])
    month = int(cbk.split(';')[2])
    day = int(cbk.split(';')[3])
    consumer_id = int(cbk.split(';')[4].split('-')[0])
    sid = int(cbk.split(';')[4].split('-')[1])
    task_name = get_stadi_info(sid).get('name')
    mes_text = ru.get('task_get_time_time').format(
        task=task_name,
        date_meet='{day}.{month}.{year}'.format(
            day=day,
            month=month,
            year=year
        )
    )
    dt = '{y}-{m}-{d}'.format(
        y=year,
        m=month,
        d=day
    )
    keyboard = types.InlineKeyboardMarkup()
    times = [t for t in range(8, 21)]
    timeslst = []
    for t in times:
        time = str(t) + ':00'
        if len(time) == 4:
            time = '0' + time
        timeslst.append(time)
    keyboard.add(*[types.InlineKeyboardButton(
        text=time,
        callback_data='deltas>' + str(consumer_id) + '>' + str(sid) + '>' + dt + '>' + time) for time in timeslst])
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


def agent_task_menu(c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    tasks = get_agent_tasks(agent_id)
    keyboard = types.InlineKeyboardMarkup()
    if tasks:
        mes_text = ru.get('agent_tasks_menu')
        for task in tasks:
            cinfo = get_consumer_info(task.get('consumer_id'))
            if cinfo.get('role') == 'seller':
                addr = cinfo.get('address')
            else:
                addr = cinfo.get('name')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('task_btn').format(
                        name=task.get('name'),
                        addr=addr
                    ),
                    callback_data='AGT_' + str(task.get('id'))
                )
            )
    else:
        mes_text = ru.get('agent_tasks_menu_no_task')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('to_menu_btn'),
            callback_data='menu'
        )
    )
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


def agent_task_detail_menu(task_id, c=None, message=None):
    task = get_agent_task_info(task_id)
    cinfo = get_consumer_info(task.get('consumer_id'))
    town = get_town_by_district_id(cinfo.get('district_id')).get('name')
    district = get_district_info(cinfo.get('district_id')).get('name')
    if cinfo.get('role') == 'buyer':
        if cinfo.get('var_id'):
            addr = get_consumer_info(cinfo.get('var_id')).get('address')
        else:
            addr = ru.get('noaddr')
    else:
        addr = cinfo.get('address')
    mes_text = ru.get('task_detail').format(
        task_name=task.get('name'),
        town=town,
        district=district,
        addr=addr,
        name=cinfo.get('name'),
        phone=cinfo.get('phone'),
    )
    keyboard = types.InlineKeyboardMarkup()
    consumer_id = task.get('consumer_id')
    agent_id = task.get('agent_id')
    sid = task.get('sid')
    cst = get_current_st(consumer_id, agent_id)
    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
        cid=consumer_id,
        sid=sid,
        subsid=cst.get('sub_stadies_id'),
        subsubsid=cst.get('sub_sub_stadies_id'),
        step=0
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('execute'),
            callback_data=cb
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='tasks'
        )
    )
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


def agent_create_task(consumer_id, sid, c=None, message=None):
    if sid == 17:
        cinfo = get_consumer_info(consumer_id)
        if cinfo.get('role') == 'buyer':
            var_id = cinfo.get('var_id')
            if var_id:
                vinfo = get_consumer_info(var_id)
                varagent_id = vinfo.get('manager_id')
                if varagent_id:
                    mgid = get_current_st(var_id, varagent_id).get('id')
                    upd_stadi(17, mgid)
                    create_client_step(var_id, 'Объект продан', varagent_id, 'seller')
        del_consumer_tasks(consumer_id)
        client_in_stadi_detail_menu(consumer_id, sid, c=c, message=message)
    else:
        task_name = get_stadi_info(sid).get('name')
        mes_text = ru.get('task_get_time').format(
            task=task_name,
            date=Basedate().date_mdh_ru()
        )
        clbk = str(consumer_id) + '-' + str(sid)
        markup = create_calendar(cb=clbk)
        if c:
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=markup)
        else:
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html',
                reply_markup=markup)


def stadies(consumer_id, sid, subsid, subsubsid, step, c):
    def send(consumer_id, role, cinfo, sid, stinfo, keyboard, c, step_txt):
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
        cb = 'клагст#{client_id}#{sid}'.format(
            client_id=consumer_id,
            sid=get_client_stepname(consumer_id)
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data=cb
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    agent_id = c.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    step_txt = ' '
    stinfo = get_stadi_info(sid)
    cinfo = get_consumer_info(consumer_id)
    steps = stinfo.get('steps')
    if steps == 0:
        if sid == 2:
            if step:
                if subsid == 1:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 2:
                    """ans_text = ru.get('pred_pod')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Подписан договор', agent_id, 'seller')
                    agent_create_task(consumer_id, 5, c=c)
                if subsid == 3:
                    """ans_text = ru.get('podpisanie')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Проведена встреча', agent_id, 'seller')
                    agent_create_task(consumer_id, 4, c=c)
                if subsid == 4:
                    """ans_text = ru.get('vstrecha')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Проведена встреча', agent_id, 'seller')
                    agent_create_task(consumer_id, 2, c=c)
            else:
                step_txt = ru.get('res_meet')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 4:
            if step:
                if subsid == 1:
                    """ans_text = ru.get('podpisanie')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    agent_create_task(consumer_id, 4, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    """ans_text = ru.get('pred_pod')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Подписан договор', agent_id, 'seller')
                    agent_create_task(consumer_id, 6, c=c)
            else:
                step_txt = ru.get('res_res')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 6:
            if step:
                if subsid == 1:
                    """ans_text = ru.get('pred_pod')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    agent_create_task(consumer_id, 6, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    """ans_text = ru.get('rek_zapusk')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Подписан договор', agent_id, 'seller')
                    agent_create_task(consumer_id, 7, c=c)
            else:
                step_txt = ru.get('res_pred_pod')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 7:
            if step:
                if subsid == 1:
                    """ans_text = ru.get('rek_zapusk')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Реклама', agent_id, 'seller')
                    agent_create_task(consumer_id, 7, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    """ans_text = ru.get('rek_zapusk')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    # create_client_step(consumer_id, 'Реклама', agent_id, 'seller')
                    """mgid = get_current_st(consumer_id, agent_id).get('id')
                    upd_stadi(16, mgid)"""
                    # agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                    ##################################
                    s_agent_stadies(consumer_id, 16, 0, 0, 0, c=c)
                    mgid = get_current_st(consumer_id, agent_id).get('id')
                    upd_stadi(17, mgid)
                    create_client_step(consumer_id, 'Запуск рекламы', agent_id, 'seller')
                    del_consumer_tasks(consumer_id)
                    # agent_create_task(consumer_id, 17, c=c)
            else:
                step_txt = ru.get('res_zap_rek')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 11:
            if step:
                if subsid == 1:
                    """ans_text = ru.get('pokaz')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    agent_create_task(consumer_id, 11, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    """ans_text = ru.get('avans_z')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Объект подобран', agent_id, 'buyer')
                    agent_create_task(consumer_id, 13, c=c)
                if subsid == 4:
                    """ans_text = ru.get('pokaz')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Проведен показ', agent_id, 'buyer')
                    consumer_set_status(consumer_id, 1)
                    agent_create_task(consumer_id, 11, c=c)
            else:
                step_txt = ru.get('res_pokaza')
                substeps = stinfo.get('details')
                for subst in substeps:
                    if sid == 11 and subst.get('id') == 4:
                        cstatus = get_consumer_info(consumer_id).get('status')
                        if cstatus:
                            pass
                        else:
                            cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                                cid=consumer_id,
                                sid=sid,
                                subsid=subst.get('id'),
                                subsubsid=0,
                                step=1
                            )
                            keyboard.add(
                                types.InlineKeyboardButton(
                                    text=subst.get('sub_st_name'),
                                    callback_data=cb
                                )
                            )
                    else:
                        cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                            cid=consumer_id,
                            sid=sid,
                            subsid=subst.get('id'),
                            subsubsid=0,
                            step=1
                        )
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=subst.get('sub_st_name'),
                                callback_data=cb
                            )
                        )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 13:
            if step:
                if subsid == 1:
                    """ans_text = ru.get('avans_z')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    agent_create_task(consumer_id, 13, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    """ans_text = ru.get('sdelka')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)"""
                    create_client_step(consumer_id, 'Внесён аванс', agent_id, 'buyer')
                    agent_create_task(consumer_id, 15, c=c)
            else:
                step_txt = ru.get('res_avans')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
        if sid == 15:
            if step:
                if subsid == 1:
                    agent_create_task(consumer_id, 15, c=c)
                if subsid == 2:
                    consumer_move_to_base(consumer_id)
                    ans_text = ru.get('client_moved_to_base')
                    bot.answer_callback_query(
                        c.id,
                        text=ans_text,
                        show_alert=True)
                    agent_clients_in_stadies(get_consumer_info(consumer_id).get('role'), c)
                if subsid == 3:
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    if cinfo.get('var_id'):
                        mes_text = ru.get('seller_done_sdelka_ask_variant')
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('next_do'),
                                callback_data='NXTDO&' + str(consumer_id)
                            ),
                            types.InlineKeyboardButton(
                                text=ru.get('find_seller_btn'),
                                callback_data='FIND&' + str(consumer_id)
                            )
                        )
                    else:
                        mes_text = ru.get('seller_done_sdelka_ask_variant_no_var_id')
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('find_seller_btn'),
                                callback_data='FIND&' + str(consumer_id)
                            )
                        )
                    bot.edit_message_text(
                        chat_id=c.message.chat.id,
                        message_id=c.message.message_id,
                        text=mes_text,
                        parse_mode='html',
                        reply_markup=keyboard)
                    # create_client_step(consumer_id, 'Сделка завершена', agent_id, 'buyer')
                    # agent_create_task(consumer_id, 17, c=c)
            else:
                step_txt = ru.get('res_avans')
                substeps = stinfo.get('details')
                for subst in substeps:
                    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                        cid=consumer_id,
                        sid=sid,
                        subsid=subst.get('id'),
                        subsubsid=0,
                        step=1
                    )
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=subst.get('sub_st_name'),
                            callback_data=cb
                        )
                    )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
    if steps == 1:
        substeps_len = len(stinfo.get('details'))
        if step:
            if subsid < substeps_len:
                updsubsid = subsid + 1
                mgid = get_current_st(consumer_id, agent_id).get('id')
                upd_sub_stadies(mgid, substid=updsubsid)
                substeps = stinfo.get('details')
                for subst in substeps:
                    if subst.get('id') == updsubsid:
                        step_txt = subst.get('sub_st_name')
                        step_btn = subst.get('do')
                cst = get_current_st(consumer_id, agent_id)
                cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                    cid=consumer_id,
                    sid=sid,
                    subsid=cst.get('sub_stadies_id'),
                    subsubsid=cst.get('sub_sub_stadies_id'),
                    step=1
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=step_btn,
                        callback_data=cb
                    )
                )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
            else:
                mgid = get_current_st(consumer_id, agent_id).get('id')
                if sid > 16:
                    agent_clients_menu(get_consumer_info(consumer_id).get('role'), c)
                else:
                    if sid == 16:
                        upd_stadi(7, mgid)
                        client_in_stadi_detail_menu(consumer_id, 7, c)
                    else:
                        sid = sid + 1
                        upd_stadi(sid, mgid)
                        client_in_stadi_detail_menu(consumer_id, sid, c)
        else:
            if subsid == 0:
                substeps = stinfo.get('details')
                for subst in substeps:
                    if subst.get('id') == 1:
                        step_txt = subst.get('sub_st_name')
                        step_btn = subst.get('do')
                cst = get_current_st(consumer_id, agent_id)
                cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                    cid=consumer_id,
                    sid=sid,
                    subsid=cst.get('sub_stadies_id') + 1,
                    subsubsid=cst.get('sub_sub_stadies_id'),
                    step=1
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=step_btn,
                        callback_data=cb
                    )
                )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )
            else:
                stinfo = get_stadi_info(sid)
                substeps = stinfo.get('details')
                for subst in substeps:
                    if subst.get('id') == subsid:
                        step_txt = subst.get('sub_st_name')
                        step_btn = subst.get('do')
                cst = get_current_st(consumer_id, agent_id)
                cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
                    cid=consumer_id,
                    sid=sid,
                    subsid=cst.get('sub_stadies_id'),
                    subsubsid=cst.get('sub_sub_stadies_id'),
                    step=1
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=step_btn,
                        callback_data=cb
                    )
                )
                send(
                    consumer_id,
                    get_consumer_info(consumer_id).get('role'),
                    cinfo,
                    sid,
                    stinfo,
                    keyboard,
                    c,
                    step_txt
                )


def agent_start_menu(c=None, message=None):
    keyboard = types.InlineKeyboardMarkup()
    mes_text = ru.get('hiagent_footer')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('sellers_mnu_btn'),
            callback_data='agentmenu*seller'
        ),
        types.InlineKeyboardButton(
            text=ru.get('buyers_mnu_btn'),
            callback_data='agentmenu*buyer'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('tasks_mnu_btn'),
            callback_data='tasks'
        )
    )
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


def agent_main_menu(consumers_role, c=None, message=None):
    mes_text = ru.get('agent_sub_menu')
    if consumers_role == 'seller':
        base_btn = ru.get('sellers_base_btn')
        base_cb = 'base@seller'
        add_btn = ru.get('add_seller_mnu_btn')
        add_cb = 'add_consumer%seller'
        my_btn = ru.get('mysellers_mnu_btn')
        my_cb = 'клиенты*1*seller'
    else:
        base_btn = ru.get('buyers_base_btn')
        base_cb = 'base@buyer'
        add_btn = ru.get('add_buyer_mnu_btn')
        add_cb = 'add_consumer%buyer'
        my_btn = ru.get('mybuyers_mnu_btn')
        my_cb = 'клиенты*1*buyer'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=base_btn,
            callback_data=base_cb
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=add_btn,
            callback_data=add_cb
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=my_btn,
            callback_data=my_cb
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('to_menu_btn'),
            callback_data='menu'
        )
    )
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


def agent_clients_menu(consumer_role, c=None, message=None, page=1):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    consumers = get_agent_consumers(agent_id, role=consumer_role)
    keyboard = types.InlineKeyboardMarkup()
    if consumers:
        if consumer_role == 'seller':
            mes_text = ru.get('sellers_mnu_text').format(
                count=len(consumers)
            )
        else:
            mes_text = ru.get('buyers_mnu_text').format(
                count=len(consumers)
            )
        consumerspage = paginator(consumers, page)
        for consumer in consumerspage:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=consumer.get('name'),
                    callback_data='клиент-' + str(consumer.get('id'))
                )
            )
        if len(consumers) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(consumers, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='клиенты*' + str(page + 1) + '*' + consumer_role
                        )
                    )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back'),
                            callback_data='клиенты*' + str(page - 1) + '*' + consumer_role
                        ),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data='клиенты*' + str(page + 1) + '*' + consumer_role
                        )
                    )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back'),
                        callback_data='клиенты*' + str(page - 1) + '*' + consumer_role
                    )
                )
    else:
        if consumer_role == 'seller':
            mes_text = ru.get('no_sellers_mnu_text')
        else:
            mes_text = ru.get('no_buyers_mnu_text')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='agentmenu*' + consumer_role
        )
    )
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


def agent_base_view_select_town_menu(consumer_role, c=None, message=None, fnd=None):
    towns = get_all_towns_info()
    if consumer_role == 'seller':
        mes_text = ru.get('find_seller_select_town')
    else:
        mes_text = ru.get('find_buyer_select_town')
    keyboard = types.InlineKeyboardMarkup()
    if fnd:
        fmark = '@' + str(fnd)
    else:
        fmark = '@0'
    for town in towns:
        keyboard.add(
            types.InlineKeyboardButton(
                text=town.get('name'),
                callback_data='agbftown@' + str(town.get('id')) + '@' + consumer_role + fmark
            )
        )
    if fnd:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='FIND&' + str(fnd)
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='agentmenu*' + consumer_role
            )
        )
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


def agent_base_view_select_district_menu(consumer_role, town_id, c=None, message=None, fnd=None):
    districts = get_districts_by_town_id(town_id)
    if consumer_role == 'seller':
        mes_text = ru.get('find_seller_select_district').format(
            town=get_town_info(town_id).get('name')
        )
    else:
        mes_text = ru.get('find_buyer_select_district').format(
            town=get_town_info(town_id).get('name')
        )
    keyboard = types.InlineKeyboardMarkup()
    if fnd:
        fmark = '@' + str(fnd)
    else:
        fmark = '@0'
    for district in districts:
        keyboard.add(
            types.InlineKeyboardButton(
                text=district.get('name'),
                callback_data='agfbdistrict@' + str(district.get('id')) + '@' + consumer_role + fmark
            )
        )
    if consumer_role == 'seller':
        tobtn = ru.get('to_sellers')
    else:
        tobtn = ru.get('to_buyers')
    if fnd:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='FIND&' + str(fnd)
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=tobtn,
                callback_data='agentmenu*' + consumer_role
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='base@' + consumer_role
            )
        )
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


def agent_base_view_select_prices_diap_menu(consumer_role, district_id, c=None, message=None, fnd=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    town_id = get_town_by_district_id(district_id).get('id')
    prices_diap = filter_by_price_diap(agent_id, district_id, consumer_role, config.prices_diap)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if fnd:
        fmark = '@' + str(fnd)
    else:
        fmark = '@0'
    if prices_diap:
        if consumer_role == 'seller':
            mes_text = ru.get('find_seller_select_price').format(
                town=get_town_info(town_id).get('name'),
                district=get_district_info(district_id).get('name')
            )
        else:
            mes_text = ru.get('find_buyer_select_price').format(
                town=get_town_info(town_id).get('name'),
                district=get_district_info(district_id).get('name')
            )
        row = []
        for _prices in prices_diap:
            if _prices.get('min') == 0:
                pmin = 'Меньше'
                pmax = price_formatter(_prices.get('max'))
            elif _prices.get('max') == 0:
                pmin = 'Больше'
                pmax = price_formatter(_prices.get('min'))
            else:
                pmin = price_formatter(_prices.get('min'))
                pmax = price_formatter(_prices.get('max'))
            row.append(
                types.InlineKeyboardButton(
                    text=ru.get('prices_diap_btn').format(
                        min=pmin,
                        max=pmax
                    ),
                    callback_data='Fpr@' + str(district_id) + '@' + consumer_role + '@' + str(_prices.get('min')) + '@' + str(_prices.get('max')) + fmark
                )
            )
        keyboard.add(*row)
    else:
        if consumer_role == 'seller':
            mes_text = ru.get('find_seller_select_price_no').format(
                town=get_town_info(town_id).get('name'),
                district=get_district_info(district_id).get('name')
            )
        else:
            mes_text = ru.get('find_buyer_select_price_no').format(
                town=get_town_info(town_id).get('name'),
                district=get_district_info(district_id).get('name')
            )
    if fnd:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='FIND&' + str(fnd)
            )
        )
    else:
        if consumer_role == 'seller':
            tobtn = ru.get('to_sellers')
        else:
            tobtn = ru.get('to_buyers')
        keyboard.add(
            types.InlineKeyboardButton(
                text=tobtn,
                callback_data='agentmenu*' + consumer_role
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='agbftown@' + str(town_id) + '@' + consumer_role
            )
        )
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


def agent_base_view_select_rooms(consumer_role, district_id, prices, c=None, message=None, fnd=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    rooms = get_consumers_rooms(agent_id, consumer_role, district_id, prices)
    town_id = get_town_by_district_id(district_id).get('id')
    if prices.get('min') == 0:
        pmin = 'Меньше'
        pmax = price_formatter(prices.get('max'))
    elif prices.get('max') == 0:
        pmin = 'Больше'
        pmax = price_formatter(prices.get('min'))
    else:
        pmin = price_formatter(prices.get('min'))
        pmax = price_formatter(prices.get('max'))
    if consumer_role == 'seller':
        mes_text = ru.get('find_seller_select_room').format(
            town=get_town_info(town_id).get('name'),
            district=get_district_info(district_id).get('name'),
            price_min=pmin,
            price_max=pmax
        )
    else:
        mes_text = ru.get('find_buyer_select_room').format(
            town=get_town_info(town_id).get('name'),
            district=get_district_info(district_id).get('name'),
            price_min=pmin,
            price_max=pmax
        )
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    if fnd:
        fmark = '@' + str(fnd)
    else:
        fmark = '@0'
    keyboard.add(*[types.InlineKeyboardButton(
        text=str(room),
        callback_data='Ar@' + str(district_id) + '@' + consumer_role + '@' + str(prices.get('min')) + '@' + str(prices.get('max')) + '@' + str(room) + '@1' + fmark) for room in rooms])
    if fnd:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='FIND&' + str(fnd)
            )
        )
    else:
        if consumer_role == 'seller':
            tobtn = ru.get('to_sellers')
        else:
            tobtn = ru.get('to_buyers')
        keyboard.add(
            types.InlineKeyboardButton(
                text=tobtn,
                callback_data='agentmenu*' + consumer_role
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='agfbdistrict@' + str(district_id) + '@' + consumer_role
            )
        )
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


def agent_filter_clients_menu(consumer_role, district_id, prices, rooms, c=None, message=None, page=1, fnd=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    if fnd:
        fmark = '@' + str(fnd)
        consumers = get_consumers_by_filter(
            agent_id,
            consumer_role,
            district_id,
            prices,
            rooms,
            fnd=True
        )
    else:
        fmark = '@0'
        consumers = get_consumers_by_filter(
            agent_id,
            consumer_role,
            district_id,
            prices,
            rooms
        )
    if consumers:
        if consumer_role == 'seller':
            mes_text = ru.get('sellers_mnu_text').format(
                count=len(consumers)
            )
        else:
            mes_text = ru.get('buyers_mnu_text').format(
                count=len(consumers)
            )
        consumerspage = paginator(consumers, page)
        for consumer in consumerspage:
            cbc = 'aC@' + str(district_id) + '@' + consumer_role + '@' \
                + str(prices.get('min')) + '@' + str(prices.get('max')) \
                + '@' + str(rooms) + '@' + str(consumer.get('id')) + fmark
            if consumer_role == 'seller':
                info = consumer.get('address')
            else:
                info = consumer.get('name')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=info,
                    callback_data=cbc
                )
            )
        if len(consumers) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(consumers, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    cb = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
                        + str(prices.get('min')) + '@' + str(prices.get('max')) \
                        + '@' + str(rooms) + '@' + str(page + 1) + fmark
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data=cb
                        )
                    )
                else:
                    cbm = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
                        + str(prices.get('min')) + '@' + str(prices.get('max')) \
                        + '@' + str(rooms) + '@' + str(page - 1)
                    cbp = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
                        + str(prices.get('min')) + '@' + str(prices.get('max')) \
                        + '@' + str(rooms) + '@' + str(page + 1) + fmark
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back'),
                            callback_data=cbm
                        ),
                        types.InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data=cbp
                        )
                    )
            else:
                cbm = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
                    + str(prices.get('min')) + '@' + str(prices.get('max')) \
                    + '@' + str(rooms) + '@' + str(page - 1) + fmark
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=ru.get('back'),
                        callback_data=cbm
                    )
                )
    else:
        if consumer_role == 'seller':
            mes_text = ru.get('no_sellers_mnu_text')
        else:
            mes_text = ru.get('no_buyers_mnu_text')
    cbb = 'Fpr@' + str(district_id) + '@' + consumer_role \
        + '@' + str(prices.get('min')) + '@' + str(prices.get('max'))
    if consumer_role == 'seller':
        tobtn = ru.get('to_sellers')
    else:
        tobtn = ru.get('to_buyers')
    keyboard.add(
        types.InlineKeyboardButton(
            text=tobtn,
            callback_data='agentmenu*' + consumer_role
        ),
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data=cbb
        )
    )
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


def agent_client_fileterd_detail_menu_no_contacts(consumer_role, district_id, prices, rooms, consumer_id, c=None, message=None, fnd=None):
    cinfo = get_consumer_info(consumer_id)
    keyboard = types.InlineKeyboardMarkup()
    if consumer_role == 'seller':
        if cinfo.get('manager_id'):
            mes_text = ru.get('finded_customer_seller_detail_menu_agent_no_contacts').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                address=cinfo.get('address'),
                area=cinfo.get('area'),
                house_floors=cinfo.get('info').get('house_floors'),
                floor=cinfo.get('info').get('floor'),
                rooms=int(cinfo.get('rooms')),
                price=cinfo.get('price')
            )
        else:
            mes_text = ru.get('finded_customer_seller_detail_menu_no_agent_no_contacts').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                address=cinfo.get('address'),
                area=cinfo.get('area'),
                house_floors=cinfo.get('info').get('house_floors'),
                floor=cinfo.get('info').get('floor'),
                rooms=int(cinfo.get('rooms')),
                price=cinfo.get('price')
            )
    else:
        _prices = get_prices_diap(cinfo.get('prices_id'))
        if _prices.get('price_min') == 0:
            pmin = 'Меньше'
            pmax = price_formatter(_prices.get('price_max'))
        elif _prices.get('price_max') == 0:
            pmin = 'Больше'
            pmax = price_formatter(_prices.get('price_min'))
        else:
            pmin = price_formatter(_prices.get('price_min'))
            pmax = price_formatter(_prices.get('price_max'))
        if cinfo.get('manager_id'):
            mes_text = ru.get('finded_customer_buyer_detail_menu_agent_no_contacts').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                rooms=int(cinfo.get('rooms')),
                price_min=pmin,
                price_max=pmax
            )
        else:
            mes_text = ru.get('finded_customer_buyer_detail_menu_no_agent_no_contacts').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                rooms=int(cinfo.get('rooms')),
                price_min=pmin,
                price_max=pmax
            )
    if fnd:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('select'),
                callback_data='SELECT&' + str(fnd) + '&' + str(consumer_id)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data='FIND&' + str(fnd)
            )
        )
    else:
        cbc = 'ClI@' + str(district_id) + '@' + consumer_role + '@' \
            + str(prices.get('min')) + '@' + str(prices.get('max')) \
            + '@' + str(rooms) + '@' + str(consumer_id)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('view_contacts'),
                callback_data=cbc
            )
        )
        cbb = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
            + str(prices.get('min')) + '@' + str(prices.get('max')) \
            + '@' + str(rooms) + '@1'
        if consumer_role == 'seller':
            tobtn = ru.get('to_sellers')
        else:
            tobtn = ru.get('to_buyers')
        keyboard.add(
            types.InlineKeyboardButton(
                text=tobtn,
                callback_data='agentmenu*' + consumer_role
            ),
            types.InlineKeyboardButton(
                text=ru.get('back_p'),
                callback_data=cbb
            )
        )
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


def agent_client_fileterd_detail_menu(consumer_role, district_id, prices, rooms, consumer_id, c=None, message=None):
    cinfo = get_consumer_info(consumer_id)
    keyboard = types.InlineKeyboardMarkup()
    if consumer_role == 'seller':
        if cinfo.get('manager_id'):
            mes_text = ru.get('finded_customer_seller_detail_menu_agent').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                address=cinfo.get('address'),
                area=cinfo.get('area'),
                house_floors=cinfo.get('info').get('house_floors'),
                floor=cinfo.get('info').get('floor'),
                rooms=int(cinfo.get('rooms')),
                price=cinfo.get('price'),
                agent_name=get_user_info(cinfo.get('manager_id')).get('name'),
                agent_phone=get_user_info(cinfo.get('manager_id')).get('phone')
            )
        else:
            mes_text = ru.get('finded_customer_seller_detail_menu_no_agent').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                phone=cinfo.get('phone'),
                address=cinfo.get('address'),
                area=cinfo.get('area'),
                house_floors=cinfo.get('info').get('house_floors'),
                floor=cinfo.get('info').get('floor'),
                rooms=int(cinfo.get('rooms')),
                price=cinfo.get('price')
            )
    else:
        _prices = get_prices_diap(cinfo.get('prices_id'))
        if _prices.get('price_min') == 0:
            pmin = 'Меньше'
            pmax = price_formatter(_prices.get('price_max'))
        elif _prices.get('price_max') == 0:
            pmin = 'Больше'
            pmax = price_formatter(_prices.get('price_min'))
        else:
            pmin = price_formatter(_prices.get('price_min'))
            pmax = price_formatter(_prices.get('price_max'))
        if cinfo.get('manager_id'):
            mes_text = ru.get('finded_customer_buyer_detail_menu_agent').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                rooms=int(cinfo.get('rooms')),
                price_min=pmin,
                price_max=pmax,
                agent_name=get_user_info(cinfo.get('manager_id')).get('name'),
                agent_phone=get_user_info(cinfo.get('manager_id')).get('phone')
            )
        else:
            mes_text = ru.get('finded_customer_buyer_detail_menu_no_agent').format(
                town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                district=get_district_info(cinfo.get('district_id')).get('name'),
                name=cinfo.get('name'),
                phone=cinfo.get('phone'),
                rooms=int(cinfo.get('rooms')),
                price_min=pmin,
                price_max=pmax
            )
    if cinfo.get('manager_id') == 0:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('get_client_btn'),
                callback_data='getclient$' + str(consumer_id)
            )
        )
    cbb = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
        + str(prices.get('min')) + '@' + str(prices.get('max')) \
        + '@' + str(rooms) + '@1'
    if consumer_role == 'seller':
        tobtn = ru.get('to_sellers')
    else:
        tobtn = ru.get('to_buyers')
    keyboard.add(
        types.InlineKeyboardButton(
            text=tobtn,
            callback_data='agentmenu*' + consumer_role
        ),
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data=cbb
        )
    )
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


def agent_clients_in_stadies(consumer_role, c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    client_stadies = get_agent_client_stadies(agent_id, consumer_role)
    if client_stadies:
        if consumer_role == 'seller':
            mes_text = ru.get('seller_agent_client_stadies_menu')
        else:
            mes_text = ru.get('buyer_agent_client_stadies_menu')
        for st in client_stadies:
            cb = 'стадия!{sid}!{role}'.format(
                sid=st,
                role=consumer_role
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=st,
                    callback_data=cb
                )
            )
    else:
        if consumer_role == 'seller':
            mes_text = ru.get('seller_agent_client_stadies_menu_no_client')
            add_btn = ru.get('add_seller_mnu_btn')
            add_cb = 'add_consumer%seller'
            btn_text = ru.get('sellers_base_btn')
            cb = 'base@seller'
        else:
            mes_text = ru.get('buyer_agent_client_stadies_menu_no_client')
            add_btn = ru.get('add_buyer_mnu_btn')
            add_cb = 'add_consumer%buyer'
            btn_text = ru.get('buyers_base_btn')
            cb = 'base@buyer'
        keyboard.add(
            types.InlineKeyboardButton(
                text=add_btn,
                callback_data=add_cb
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=btn_text,
                callback_data=cb
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('to_menu_btn'),
            callback_data='agentmenu*' + consumer_role
        )
    )
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


def agent_client_list_in_stadi(sid, consumer_role, c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    clients = get_clients_in_stadi(sid, agent_id)
    mes_text = ru.get('stadi_clients_list').format(
        sname=sid
    )
    for client in clients:
        cb = 'клагст#{client_id}#{sid}'.format(
            client_id=client.get('id'),
            sid=sid
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=client.get('name'),
                callback_data=cb
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='клиенты*1*' + consumer_role
        )
    )
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


def client_in_stadi_detail_menu(consumer_id, sid, c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    echek = True
    cinfo = get_consumer_info(consumer_id)
    district_id = cinfo.get('district_id')
    consumer_name = cinfo.get('name')
    consumer_phone = cinfo.get('phone')
    consumer_address = cinfo.get('address')
    area = cinfo.get('area')
    house_floors = cinfo.get('info').get('house_floors')
    floor = cinfo.get('info').get('floor')
    rooms = str(cinfo.get('rooms'))
    if rooms.split('.')[1] == '0':
        rooms = int(float(rooms))
    else:
        rooms = float(rooms)
    price = int(cinfo.get('price'))
    if cinfo.get('manager_id'):
        agent_name = get_user_info(cinfo.get('manager_id')).get('name')
    else:
        agent_name = 'Не назначен'
    if cinfo.get('role') == 'seller':
        var_id = cinfo.get('var_id')
        if var_id:
            vinfo = get_consumer_info(var_id)
            prices = get_prices_diap(vinfo.get('prices_id'))
            if prices.get('price_min') == 0:
                pmin = 'Меньше'
                pmax = prices.get('price_max')
                prices_diap = ru.get('prices_diap').format(
                    price_min=pmin,
                    price_max=price_formatter(pmax)
                )
            elif prices.get('price_max') == 0:
                pmin = 'Больше'
                pmax = prices.get('price_min')
                prices_diap = ru.get('prices_diap').format(
                    price_min=pmin,
                    price_max=price_formatter(pmax)
                )
            else:
                pmin = prices.get('price_min')
                pmax = prices.get('price_max')
                prices_diap = ru.get('prices_diap').format(
                    price_min=price_formatter(pmin),
                    price_max=price_formatter(pmax)
                )
            variant = ru.get('buyer_info_to_seller').format(
                buyer_name=vinfo.get('name'),
                buyer_phone=vinfo.get('phone'),
                price_diap=prices_diap
            )
        else:
            variant = ru.get('nobuyer_info_to_seller')
        if sid == 'Объект продан':
            mes_text = ru.get('stadi_seller_details_menu_text_no_task').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=area,
                house_floors=house_floors,
                floor=floor,
                rooms=rooms,
                price=price,
                variant=variant,
                agent_name=agent_name
            )
        elif sid == 17:
            mes_text = ru.get('stadi_seller_details_menu_text_no_task').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=area,
                house_floors=house_floors,
                floor=floor,
                rooms=rooms,
                price=price,
                variant=variant,
                agent_name=agent_name
            )
        else:
            try:
                task_name = get_current_task_name(consumer_id, agent_id).get('name')
                date_end = get_current_task_name(consumer_id, agent_id).get('date_end')
                echek = True
            except:
                task_name = '---'  # get_client_stepname(consumer_id)
                date_end = '---'
                echek = False
            mes_text = ru.get('stadi_seller_details_menu_text').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=area,
                house_floors=house_floors,
                floor=floor,
                rooms=rooms,
                price=price,
                variant=variant,
                agent_name=agent_name,
                current=task_name,
                date_end=date_end
            )
    else:
        info = cinfo.get('info')
        seller_id = info.get('seller_id')
        if seller_id:
            sinfo = get_consumer_info(seller_id)
            seller_info = ru.get('sellers_info_to_buyer_details').format(
                seller_address=sinfo.get('address'),
                seller_name=sinfo.get('name'),
                seller_price=sinfo.get('price'),
                seller_phone=sinfo.get('phone')
            )
        else:
            seller_info = ru.get('sellers_info_to_buyer_details_no_seller')
            """keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('find_seller_btn'),
                    callback_data='findseller/' + str(consumer_id)
                )
            )"""
        prices = get_prices_diap(cinfo.get('prices_id'))
        if prices.get('price_min') == 0:
            pmin = 'Меньше'
            pmax = prices.get('price_max')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        elif prices.get('price_max') == 0:
            pmin = 'Больше'
            pmax = prices.get('price_min')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        else:
            pmin = prices.get('price_min')
            pmax = prices.get('price_max')
            prices_diap = ru.get('prices_diap').format(
                price_min=price_formatter(pmin),
                price_max=price_formatter(pmax)
            )
        if sid == 'Сделка завершена':
            mes_text = ru.get('stadi_buyer_details_menu_text_sdelka_over').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                rooms=rooms,
                prices_diap=prices_diap,
                seller_info=seller_info,
                agent_name=agent_name
            )
        elif sid == 17:
            mes_text = ru.get('stadi_buyer_details_menu_text_sdelka_over').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                rooms=rooms,
                prices_diap=prices_diap,
                seller_info=seller_info,
                agent_name=agent_name
            )
        else:
            try:
                task_name = get_current_task_name(consumer_id, agent_id).get('name')
                date_end = get_current_task_name(consumer_id, agent_id).get('date_end')
                echek = True
            except:
                task_name = '---'  # get_client_stepname(consumer_id)
                date_end = '---'
                echek = False
            mes_text = ru.get('stadi_buyer_details_menu_text').format(
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                rooms=rooms,
                prices_diap=prices_diap,
                seller_info=seller_info,
                agent_name=agent_name,
                current=task_name,
                date_end=date_end
            )
    cst = get_current_st(consumer_id, agent_id)
    cb = 'ST|{cid}|{sid}|{subsid}|{subsubsid}|{step}'.format(
        cid=consumer_id,
        sid=sid,
        subsid=cst.get('sub_stadies_id'),
        subsubsid=cst.get('sub_sub_stadies_id'),
        step=0
    )
    if sid == 'Не назначено':
        pass
    elif sid == 'Сделка завершена':
        pass
    elif sid == 17:
        pass
    else:
        if echek:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('execute'),
                    callback_data=cb
                )
            )
    cb = 'agentmenu*' + cinfo.get('role')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('edit'),
            callback_data='редкл@' + str(consumer_id) + '@' + str(sid)
        )
    )
    if cinfo.get('role') == 'seller':
        tobtn = ru.get('to_sellers')
    else:
        tobtn = ru.get('to_buyers')
    keyboard.add(
        types.InlineKeyboardButton(
            text=tobtn,
            callback_data=cb
        )
    )
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


def client_edit_menu(consumer_id, sid, c=None, message=None):
    keyboard = types.InlineKeyboardMarkup()
    cinfo = get_consumer_info(consumer_id)
    district_id = cinfo.get('district_id')
    consumer_name = cinfo.get('name')
    consumer_phone = cinfo.get('phone')
    consumer_address = cinfo.get('address')
    area = cinfo.get('area')
    house_floors = cinfo.get('info').get('house_floors')
    floor = cinfo.get('info').get('floor')
    rooms = str(cinfo.get('rooms'))
    if rooms.split('.')[1] == '0':
        rooms = int(float(rooms))
    else:
        rooms = float(rooms)
    price = int(cinfo.get('price'))
    if cinfo.get('manager_id'):
        agent_name = get_user_info(cinfo.get('manager_id')).get('name')
    else:
        agent_name = 'Не назначен'
    if cinfo.get('role') == 'seller':
        var_id = cinfo.get('var_id')
        if var_id:
            vinfo = get_consumer_info(var_id)
            prices = get_prices_diap(vinfo.get('prices_id'))
            prices_diap = ru.get('prices_diap').format(
                price_min=price_formatter(prices.get('price_min')),
                price_max=price_formatter(prices.get('price_max'))
            )
            variant = ru.get('buyer_info_to_seller').format(
                buyer_name=vinfo.get('name'),
                buyer_phone=vinfo.get('phone'),
                price_diap=prices_diap
            )
        else:
            variant = ru.get('nobuyer_info_to_seller')
        mes_text = ru.get('seller_details_menu_text').format(
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=consumer_name,
            phone=consumer_phone,
            address=consumer_address,
            area=area,
            house_floors=house_floors,
            floor=floor,
            rooms=rooms,
            price=price,
            variant=variant,
            agent_name=agent_name
        )
    else:
        info = cinfo.get('info')
        seller_id = info.get('seller_id')
        if seller_id:
            sinfo = get_consumer_info(seller_id)
            seller_info = ru.get('sellers_info_to_buyer_details').format(
                seller_address=sinfo.get('address'),
                seller_name=sinfo.get('name'),
                seller_price=sinfo.get('price'),
                seller_phone=sinfo.get('phone')
            )
        else:
            seller_info = ru.get('sellers_info_to_buyer_details_no_seller')
            """keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('find_seller_btn'),
                    callback_data='findseller/' + str(consumer_id)
                )
            )"""
        prices = get_prices_diap(cinfo.get('prices_id'))
        if prices.get('price_min') == 0:
            pmin = 'Меньше'
            pmax = prices.get('price_max')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        elif prices.get('price_max') == 0:
            pmin = 'Больше'
            pmax = prices.get('price_min')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        else:
            pmin = prices.get('price_min')
            pmax = prices.get('price_max')
            prices_diap = ru.get('prices_diap').format(
                price_min=price_formatter(pmin),
                price_max=price_formatter(pmax)
            )
        mes_text = ru.get('buyer_details_menu_text').format(
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=consumer_name,
            phone=consumer_phone,
            rooms=rooms,
            prices_diap=prices_diap,
            seller_info=seller_info,
            agent_name=agent_name
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('edit_name_btn'),
            callback_data='cons_ename=' + str(consumer_id)
        )
    )
    if get_consumer_info(consumer_id).get('role') == 'seller':
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_area_btn'),
                callback_data='cons_earea=' + str(consumer_id)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_floors_total_btn'),
                callback_data='cons_efloorshouse=' + str(consumer_id)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_floor_btn'),
                callback_data='cons_efloor=' + str(consumer_id)
            ),
            types.InlineKeyboardButton(
                text=ru.get('edit_price_btn'),
                callback_data='cons_eprice=' + str(consumer_id)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_rooms_btn'),
                callback_data='cons_erooms=' + str(consumer_id)
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_whanted_rooms_btn'),
                callback_data='cons_erooms=' + str(consumer_id)
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_diap_prices_btn'),
                callback_data='cons_epricesdiap=' + str(consumer_id)
            )
        )
    cb = 'клагст#{client_id}#{sid}'.format(
        client_id=consumer_id,
        sid=sid
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data=cb
        )
    )
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
