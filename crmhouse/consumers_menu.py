# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from consumers_utils import (find_sellers_to_buyers, get_all_towns_info,
                             get_consumer_info, get_consumers_by_role,
                             get_district_info, get_districts_by_town_id,
                             get_prices_diap, get_town_by_district_id,
                             get_town_info)
from lang import ru
from paginators import paginator
from user_utils import get_user_info
from agent_utils import price_formatter

# telegram bot api
bot = telebot.TeleBot(config.token)


def btn(text, cb):
    button = types.InlineKeyboardButton(
        text=text,
        callback_data=cb
    )
    return button


def manager_menu(c=None, message=None):
    keyboard = types.InlineKeyboardMarkup()
    mes_text = ru.get('hiagent_footer')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('add_seller_mnu_btn'),
            callback_data='add_consumer%seller'
        ),
        types.InlineKeyboardButton(
            text=ru.get('add_buyer_mnu_btn'),
            callback_data='add_consumer%buyer'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('sellers_mnu_btn'),
            callback_data='клиенты*1*seller'
        ),
        types.InlineKeyboardButton(
            text=ru.get('buyers_mnu_btn'),
            callback_data='клиенты*1*buyer'
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


def clients_menu(consumer_role, c=None, message=None, page=1):
    consumers = get_consumers_by_role(role=consumer_role)
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


def add_consumer_select_town(consumer_role, c=None, message=None):
    towns = get_all_towns_info()
    if consumer_role == 'seller':
        role_text = ru.get('seller_role_to_add_fn')
    else:
        role_text = ru.get('buyer_role_to_add_fn')
    mes_text = ru.get('add_consumer_select_town').format(
        role=role_text
    )
    keyboard = types.InlineKeyboardMarkup()
    for town in towns:
        keyboard.add(
            types.InlineKeyboardButton(
                text=town.get('name'),
                callback_data='выбор_города%' + str(town.get('id')) + '%' + consumer_role
            )
        )
    if get_user_info(c.from_user.id).get('role') == 'manager':
        cb = 'menu'
    else:
        cb = 'agentmenu*' + consumer_role
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


def add_consumer_select_district(consumer_role, town_id, c=None, message=None):
    districts = get_districts_by_town_id(town_id)
    if consumer_role == 'seller':
        role_text = ru.get('seller_role_to_add_fn')
        mes_text = ru.get('add_consumer_seller_select_district').format(
            role=role_text,
            town=get_town_info(town_id).get('name')
        )
    else:
        role_text = ru.get('buyer_role_to_add_fn')
        mes_text = ru.get('add_consumer_select_district').format(
            role=role_text,
            town=get_town_info(town_id).get('name')
        )
    keyboard = types.InlineKeyboardMarkup()
    for district in districts:
        keyboard.add(
            types.InlineKeyboardButton(
                text=district.get('name'),
                callback_data='выбор_района>' + str(district.get('id')) + '>' + consumer_role
            )
        )
    if get_user_info(c.from_user.id).get('role') == 'manager':
        cb = 'menu'
    else:
        cb = 'agentmenu*' + consumer_role
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


def add_consumer_get_rooms(consumer_id):
    cinfo = get_consumer_info(consumer_id)
    consumer_name = cinfo.get('name')
    consumer_phone = cinfo.get('phone')
    if cinfo.get('role') == 'seller':
        role_text = ru.get('seller_role_to_add_fn')
        mes_text = ru.get('add_consumer_seller_get_rooms').format(
            role=role_text,
            town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
            district=get_district_info(cinfo.get('district_id')).get('name'),
            name=consumer_name,
            phone=consumer_phone
        )
    else:
        role_text = ru.get('buyer_role_to_add_fn')
        mes_text = ru.get('add_consumer_buyer_get_rooms').format(
            role=role_text,
            town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
            district=get_district_info(cinfo.get('district_id')).get('name'),
            name=consumer_name,
            phone=consumer_phone
        )
    return mes_text


def add_consumer_buyer_set_price(consumer_id, c=None, message=None, upd=None):
    cinfo = get_consumer_info(consumer_id)
    district_id = cinfo.get('district_id')
    if get_town_by_district_id(district_id).get('name') == 'Троицк':
        tprices = config.tow_prices.get('troick')
    else:
        tprices = config.tow_prices.get('chehov')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if upd:
        mes_text = ru.get('edit_consumer_buyer_get_price_new_rel').format(
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=cinfo.get('name'),
            phone=cinfo.get('phone'),
            address=cinfo.get('address')
        )
        edt = 1
    else:
        role_text = ru.get('seller_role_to_add_fn')
        mes_text = ru.get('add_consumer_buyer_get_price_new_rel').format(
            role=role_text,
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=cinfo.get('name'),
            phone=cinfo.get('phone'),
            address=cinfo.get('address')
        )
        edt = 0
    row = []
    for price in tprices:
        if price[0] == 0 and price[1] > 0:
            otprice = 'Меньше'
            doprice = price_formatter(price[1])
            pmin = 0
            pmax = price[1]
        elif price[1] == 0 and price[0] > 0:
            otprice = 'Больше'
            doprice = price_formatter(price[0])
            pmin = price[0]
            pmax = price[1]
        else:
            otprice = price_formatter(price[0])
            doprice = price_formatter(price[1])
            pmin = price[0]
            pmax = price[1]
        cb = 'CPD={cid}={pmin}={pmax}={edt}'.format(
            cid=consumer_id,
            pmin=pmin,
            pmax=pmax,
            edt=edt
        )
        row.append(
            btn(ru.get('prices_diap_btn').format(min=otprice, max=doprice), cb)
        )
    keyboard.add(*row)
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


def consumer_details(consumer_id, c=None, message=None):
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
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('find_seller_btn'),
                    callback_data='findseller/' + str(consumer_id)
                )
            )
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
        ),
        types.InlineKeyboardButton(
            text=ru.get('edit_phone_btn'),
            callback_data='cons_ephone=' + str(consumer_id)
        )
    )
    if get_consumer_info(consumer_id).get('role') == 'seller':
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('edit_address_btn'),
                callback_data='cons_eaddress=' + str(consumer_id)
            ),
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
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='клиенты*1*' + cinfo.get('role')
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


def find_seller(consumer_id, c=None, message=None):
    sellers = find_sellers_to_buyers(consumer_id)
    keyboard = types.InlineKeyboardMarkup()
    if sellers:
        mes_text = ru.get('find_sellers_mnu_text').format(
            sellers_count=len(sellers)
        )
        for seller in sellers:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=seller.get('address'),
                    callback_data='addsellertobuyer+' + str(consumer_id) + '+' + str(seller.get('id'))
                )
            )
    else:
        mes_text = ru.get('find_sellers_mnu_text_no_sellers')
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('back_p'),
            callback_data='клиент-' + str(consumer_id)
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


def consumers_menu(message=None, c=None, status=1, page=1):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    consumers = get_consumers_by_role('all', status=status)
    keyboard = types.InlineKeyboardMarkup()
    if user_id in config.admin:
        if consumers:
            if status:
                mes_text = ru.get('sellers_mnu_text').forma(
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
                                callback_data='consumers*' + str(page + 1) + '*' + str(status)
                            )
                        )
                    else:
                        keyboard.add(
                            types.InlineKeyboardButton(
                                text=ru.get('back'),
                                callback_data='consumers*' + str(page - 1) + '*' + str(status)
                            ),
                            types.InlineKeyboardButton(
                                text=ru.get('next'),
                                callback_data='consumers*' + str(page + 1) + '*' + str(status)
                            )
                        )
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=ru.get('back'),
                            callback_data='consumers*' + str(page - 1) + '*' + str(status)
                        )
                    )
        else:
            if status:
                mes_text = ru.get('no_sellers_mnu_text')
            else:
                mes_text = ru.get('no_buyers_mnu_text')
    else:
        if consumers:
            if status:
                mes_text = ru.get('sellers_mnu_text').format(
                    count=len(consumers)
                )
            else:
                mes_text = ru.get('buyers_mnu_text').format(
                    count=len(consumers)
                )
        else:
            if status:
                mes_text = ru.get('no_sellers_mnu_text')
            else:
                mes_text = ru.get('no_buyers_mnu_text')
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
