# -*- coding: utf-8 -*-
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from agent_utils import (filter_by_price_diap, get_agent_client_stadies,
                         get_client_stepname, get_clients_in_stadi,
                         get_consumers_by_filter, get_consumers_rooms,
                         get_current_task_name, price_formatter)
from boss_utils import get_agents, get_client_history, get_consumer_stata
from consumers_utils import (get_all_towns_info, get_consumer_info,
                             get_consumers_by_role, get_district_info,
                             get_districts_by_town_id, get_prices_diap,
                             get_town_by_district_id, get_town_info)
from lang import ru
from paginators import paginator
from user_utils import get_user_info, get_user_info_by_id

# telegram bot api
bot = telebot.TeleBot(config.token)


def btn(text, cb):
    button = InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button


def boss_main_menu(c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup()
    stats = get_consumer_stata(user_id)
    mes_text = ru.get('boss_main_menu').format(
        sellers=stats.get('sellers'),
        new_sellers=stats.get('new_sellers'),
        buyers=stats.get('buyers'),
        new_buyers=stats.get('new_buyers')
    )
    keyboard.add(
        btn(
            ru.get('sellers_mnu_btn'),
            'boss_seller'
        ),
        btn(
            ru.get('buyers_mnu_btn'),
            'boss_buyer'
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


def boss_sub_menu(consumer_role, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    stats = get_consumer_stata(user_id)
    keyboard = InlineKeyboardMarkup()
    if consumer_role == 'seller':
        mes_text = ru.get('boss_sellers_menu').format(
            sellers=stats.get('sellers'),
            new_sellers=stats.get('new_sellers')
        )
        keyboard.add(
            btn(
                ru.get('sellers_base_btn'),
                'клиенты*1*seller'
            ),
            btn(
                ru.get('sellers_mnu_btn'),
                'agents-seller'
            )
        )
    else:
        mes_text = ru.get('boss_buyers_menu').format(
            buyers=stats.get('buyers'),
            new_buyers=stats.get('new_buyers')
        )
        keyboard.add(
            btn(
                ru.get('buyers_base_btn'),
                'клиенты*1*buyer'
            ),
            btn(
                ru.get('buyers_mnu_btn'),
                'agents-buyer'
            )
        )
    keyboard.add(
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_base_view_select_town_menu(consumer_role, c=None, message=None):
    towns = get_all_towns_info()
    if consumer_role == 'seller':
        mes_text = ru.get('find_seller_select_town')
    else:
        mes_text = ru.get('find_buyer_select_town')
    keyboard = InlineKeyboardMarkup()
    for town in towns:
        keyboard.add(
            btn(
                town.get('name'),
                'agbftown@' + str(town.get('id')) + '@' + consumer_role
            )
        )
    keyboard.add(
        btn(
            ru.get('back_p'),
            'boss_' + consumer_role
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_base_view_select_district_menu(consumer_role, town_id, c=None, message=None):
    districts = get_districts_by_town_id(town_id)
    if consumer_role == 'seller':
        mes_text = ru.get('find_seller_select_district').format(
            town=get_town_info(town_id).get('name')
        )
    else:
        mes_text = ru.get('find_buyer_select_district').format(
            town=get_town_info(town_id).get('name')
        )
    keyboard = InlineKeyboardMarkup()
    for district in districts:
        keyboard.add(
            btn(
                district.get('name'),
                'agfbdistrict@' + str(district.get('id')) + '@' + consumer_role
            )
        )
    keyboard.add(
        btn(
            ru.get('back_p'),
            'клиенты*1*' + consumer_role
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_base_view_select_prices_diap_menu(consumer_role, district_id, c=None, message=None):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    town_id = get_town_by_district_id(district_id).get('id')
    prices_diap = filter_by_price_diap(agent_id, district_id, consumer_role, config.prices_diap)
    keyboard = InlineKeyboardMarkup(row_width=2)
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
                InlineKeyboardButton(
                    text=ru.get('prices_diap_btn').format(
                        min=pmin,
                        max=pmax
                    ),
                    callback_data='Fpr@' + str(district_id) + '@' + consumer_role + '@' + str(_prices.get('min')) + '@' + str(_prices.get('max'))
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
    keyboard.add(
        btn(
            ru.get('back_p'),
            'agbftown@' + str(town_id) + '@' + consumer_role
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_base_view_select_rooms(consumer_role, district_id, prices, c=None, message=None):
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
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*[InlineKeyboardButton(
        text=str(room),
        callback_data='Ar@' + str(district_id) + '@' + consumer_role + '@' + str(prices.get('min')) + '@' + str(prices.get('max')) + '@' + str(room) + '@1') for room in rooms])
    keyboard.add(
        btn(
            ru.get('back_p'),
            'agfbdistrict@' + str(district_id) + '@' + consumer_role
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_filter_clients_menu(consumer_role, district_id, prices, rooms, c=None, message=None, page=1):
    if c:
        agent_id = c.from_user.id
    else:
        agent_id = message.from_user.id
    consumers = get_consumers_by_filter(
        agent_id,
        consumer_role,
        district_id,
        prices,
        rooms
    )
    keyboard = InlineKeyboardMarkup()
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
                + '@' + str(rooms) + '@' + str(consumer.get('id'))
            if consumer_role == 'seller':
                info = consumer.get('address')
            else:
                info = consumer.get('name')
            keyboard.add(
                InlineKeyboardButton(
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
                        + '@' + str(rooms) + '@' + str(page + 1)
                    keyboard.add(
                        InlineKeyboardButton(
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
                        + '@' + str(rooms) + '@' + str(page + 1)
                    keyboard.add(
                        InlineKeyboardButton(
                            text=ru.get('back'),
                            callback_data=cbm
                        ),
                        InlineKeyboardButton(
                            text=ru.get('next'),
                            callback_data=cbp
                        )
                    )
            else:
                cbm = 'Ar@' + str(district_id) + '@' + consumer_role + '@' \
                    + str(prices.get('min')) + '@' + str(prices.get('max')) \
                    + '@' + str(rooms) + '@' + str(page - 1)
                keyboard.add(
                    InlineKeyboardButton(
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
    keyboard.add(
        InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data=cbb
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_agents_menu(consumer_role, c=None, message=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup()
    agents = get_agents(user_id)
    if agents:
        mes_text = ru.get('boss_agents').format(
            agents=len(agents)
        )
        for agent in agents:
            keyboard.add(
                btn(
                    agent.get('name'),
                    'агент=' + str(agent.get('id')) + '=' + consumer_role
                )
            )
    else:
        mes_text = ru.get('boss_agents_no_agents')
    if consumer_role == 'seller':
        cb = 'boss_seller'
    else:
        cb = 'boss_buyer'
    keyboard.add(
        btn(
            ru.get('back_p'),
            cb
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


def boss_clients_menu(consumer_role, c=None, message=None, page=1):
    consumers = get_consumers_by_role(role=consumer_role)
    keyboard = InlineKeyboardMarkup()
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
                btn(
                    consumer.get('name'),
                    'клиент-' + str(consumer.get('id'))
                )
            )
        if len(consumers) <= config.pagelimit:
            pass
        else:
            chek_next_btn = len(paginator(consumers, page + 1))
            if chek_next_btn > 0:
                if page == 1:
                    keyboard.add(
                        btn(
                            ru.get('next'),
                            'клиенты*' + str(page + 1) + '*' + consumer_role
                        )
                    )
                else:
                    keyboard.add(
                        btn(
                            ru.get('back'),
                            'клиенты*' + str(page - 1) + '*' + consumer_role
                        ),
                        btn(
                            ru.get('next'),
                            'клиенты*' + str(page + 1) + '*' + consumer_role
                        )
                    )
            else:
                keyboard.add(
                    btn(
                        ru.get('back'),
                        'клиенты*' + str(page - 1) + '*' + consumer_role
                    )
                )
    else:
        if consumer_role == 'seller':
            mes_text = ru.get('no_sellers_mnu_text')
        else:
            mes_text = ru.get('no_buyers_mnu_text')
    if consumer_role == 'seller':
        cb = 'boss_seller'
    else:
        cb = 'boss_buyer'
    keyboard.add(
        btn(
            ru.get('back_p'),
            cb
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


def boss_consumer_details(consumer_id, prices, c=None, message=None):
    keyboard = InlineKeyboardMarkup()
    cinfo = get_consumer_info(consumer_id)
    district_id = cinfo.get('district_id')
    consumer_name = cinfo.get('name')
    consumer_role = cinfo.get('role')
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
            _prices = get_prices_diap(vinfo.get('prices_id'))
            prices_diap = ru.get('prices_diap').format(
                price_min=_prices.get('price_min'),
                price_max=_prices.get('price_max')
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
        _prices = get_prices_diap(cinfo.get('prices_id'))
        if _prices.get('price_min') == 0:
            pmin = 'Меньше'
            pmax = _prices.get('price_max')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        elif _prices.get('price_max') == 0:
            pmin = 'Больше'
            pmax = _prices.get('price_min')
            prices_diap = ru.get('prices_diap').format(
                price_min=pmin,
                price_max=price_formatter(pmax)
            )
        else:
            pmin = _prices.get('price_min')
            pmax = _prices.get('price_max')
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
        btn(
            ru.get('back_p'),
            'Ar@' + str(district_id) + '@' + consumer_role + '@' + str(prices.get('min')) + '@' + str(prices.get('max')) + '@' + str(rooms) + '@1'
        ),
        btn(
            ru.get('to_menu_btn'),
            'menu'
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


def boss_agent_clients_in_stadies(consumer_role, agent_id, c=None, message=None):
    if consumer_role == 'seller':
        cr = 's'
    else:
        cr = 'b'
    uid = agent_id
    agent_id = get_user_info_by_id(agent_id).get('user_id')
    keyboard = InlineKeyboardMarkup()
    client_stadies = get_agent_client_stadies(agent_id, consumer_role)
    if client_stadies:
        if consumer_role == 'seller':
            mes_text = ru.get('seller_agent_client_stadies_menu')
        else:
            mes_text = ru.get('buyer_agent_client_stadies_menu')
        for st in client_stadies:
            cb = 'AS!{sid}!{role}!{uid}'.format(
                sid=st,
                role=cr,
                uid=uid
            )
            keyboard.add(
                btn(
                    st,
                    cb
                )
            )
    else:
        mes_text = ru.get('boss_agents_in_stadies_no_clients')
    keyboard.add(
        btn(
            ru.get('back_p'),
            'agents-' + consumer_role
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


def boss_agent_client_list_in_stadi(agent_id, stadi, consumer_role, c=None, message=None):
    uid = agent_id
    agent_id = get_user_info_by_id(agent_id).get('user_id')
    keyboard = InlineKeyboardMarkup()
    clients = get_clients_in_stadi(stadi, agent_id)
    mes_text = ru.get('stadi_clients_list').format(
        sname=stadi
    )
    for client in clients:
        cb = 'CLA#{client_id}#{sid}#{uid}'.format(
            client_id=client.get('id'),
            sid=stadi,
            uid=uid
        )
        keyboard.add(
            btn(
                client.get('name'),
                cb
            )
        )
    keyboard.add(
        btn(
            ru.get('back_p'),
            'агент=' + str(uid) + '=' + consumer_role
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


def boss_client_in_stadi_detail_menu(uid, consumer_id, sid, c=None, message=None):
    agent_id = get_user_info_by_id(uid).get('user_id')
    history = get_client_history(consumer_id, agent_id)
    keyboard = InlineKeyboardMarkup()
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
        try:
            current_task = get_current_task_name(consumer_id, agent_id).get('name')
            date_end = get_current_task_name(consumer_id, agent_id).get('date_end')
        except:
            current_task = '---'  # get_client_stepname(consumer_id)
            date_end = '---'
        mes_text = ru.get('boss_stadi_seller_details_menu_text').format(
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
            current=current_task,
            date_end=date_end,
            history=history
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
            seller_info = ru.get('boss_sellers_info_to_buyer_details_no_seller')
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
        try:
            current_task = '---'  # get_current_task_name(consumer_id, agent_id).get('name')
            date_end = get_current_task_name(consumer_id, agent_id).get('date_end')
        except:
            current_task = 'Сделка завершена'
            date_end = '---'
        mes_text = ru.get('boss_stadi_buyer_details_menu_text').format(
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=consumer_name,
            phone=consumer_phone,
            rooms=rooms,
            prices_diap=prices_diap,
            seller_info=seller_info,
            agent_name=agent_name,
            current=current_task,
            date_end=date_end,
            history=history
        )
    st = get_client_stepname(consumer_id)
    if cinfo.get('role') == 'seller':
        cr = 's'
    else:
        cr = 'b'
    cb = 'AS!{sid}!{role}!{uid}'.format(
        sid=st,
        role=cr,
        uid=uid
    )
    keyboard.add(
        btn(
            ru.get('back_p'),
            cb
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
