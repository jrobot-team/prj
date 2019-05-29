# -*- coding: utf-8 -*-
import logging

import cherrypy
import telebot
from telebot import types

import config
from dbclasses import Manager, Admin
from agent_menu import (
    agent_base_view_select_district_menu,
    agent_base_view_select_prices_diap_menu, agent_base_view_select_rooms,
    agent_base_view_select_town_menu, agent_client_fileterd_detail_menu,
    agent_client_fileterd_detail_menu_no_contacts, agent_client_list_in_stadi,
    agent_clients_in_stadies, agent_create_task, agent_filter_clients_menu,
    agent_find_seller, agent_main_menu, agent_selected_seller_to_buyer,
    agent_seller_finded_menu, agent_start_menu, agent_task_detail_menu,
    agent_task_menu, client_edit_menu, client_in_stadi_detail_menu, stadies,
    task_time_menu)
from agent_utils import (buyer_prep_to_view, create_agent_task,
                         create_client_step, get_client_stepname,
                         get_current_sid, get_current_st, get_stadi_info,
                         seller_prep_to_meet, upd_stadi)
from boss_menu import (
    boss_agent_client_list_in_stadi, boss_agent_clients_in_stadies,
    boss_agents_menu, boss_base_view_select_district_menu,
    boss_base_view_select_prices_diap_menu, boss_base_view_select_rooms,
    boss_base_view_select_town_menu, boss_client_in_stadi_detail_menu,
    boss_consumer_details, boss_filter_clients_menu, boss_main_menu,
    boss_sub_menu)
from boss_utils import admininfo
from bot_calendar_helper import create_calendar
from bot_utils import Basedate, date_time_to_base_format, replacer
from consumers_menu import (add_consumer_get_rooms,
                            add_consumer_select_district,
                            add_consumer_select_town, clients_menu,
                            consumer_details, consumers_menu, find_seller,
                            manager_menu, add_consumer_buyer_set_price)
from consumers_utils import (buyer_update_seller_var, consumer_set_address,
                             consumer_set_area, consumer_set_floor,
                             consumer_set_manager_id, consumer_set_price,
                             consumer_set_rooms, consumer_update_floor,
                             consumer_update_floors_house,
                             consumer_update_name, consumer_update_phone,
                             consumer_update_price_diap, create_consumer,
                             get_consumer_info, get_district_info,
                             get_town_by_district_id)
from lang import ru
from main_menu import keymenu, startmenu
from otchets_agents import agent_otchet, agent_stadies, agents_boss_list
from user_utils import get_user_info, cheking_manager_phone
from users_menu import choose_role_users_menu, users_menu


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


# telegram bot api
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.token)

cancel = [
    '/start',
    '/Start',
    ru.get('sellers_mnu_btn'),
    ru.get('buyers_mnu_btn'),
    ru.get('sellers_mnu_btn'),
    ru.get('buyers_mnu_btn'),
    ru.get('tasks_mnu_btn'),
    ru.get('reports_mnu_btn'),
    ru.get('add_seller_mnu_btn'),
    ru.get('add_buyer_mnu_btn'),
    ru.get('users_mnu_btn'),
]


def edit_consumer_name_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        name = replacer(message.text)
        consumer_update_name(consumer_id, name)
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_phone_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        phone = replacer(message.text)
        consumer_update_phone(consumer_id, phone)
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_address_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        address = replacer(message.text)
        consumer_set_address(consumer_id, address)
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_area_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        area = replacer(message.text)
        chek = consumer_set_area(consumer_id, area)
        if chek:
            pass
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_floors_house_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        floors = replacer(message.text)
        if floors.isdigit():
            consumer_update_floors_house(consumer_id, floors)
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_floor_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        floor = replacer(message.text)
        if floor.isdigit():
            consumer_update_floor(consumer_id, floor)
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_price_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        price = replacer(message.text)
        if price.isdigit():
            consumer_set_price(consumer_id, seller_price=price)
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_rooms_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        rooms = replacer(message.text)
        if rooms.isdigit():
            consumer_set_rooms(consumer_id, rooms)
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def edit_consumer_price_diap_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        prices = replacer(message.text)
        chek = consumer_update_price_diap(consumer_id, prices)
        if chek:
            pass
        else:
            mes_text = ru.get('edit_error')
            bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html'
            )
        if get_user_info(message.from_user.id).get('role') == 'agent':
            sid = get_current_sid(consumer_id, message.from_user.id)
            client_edit_menu(consumer_id, sid, message=message)
        else:
            consumer_details(consumer_id, message=message)


def create_consumer_name_fn(message, consumer_role=None, district_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_name = replacer(message.text)
        if consumer_role == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
        else:
            role_text = ru.get('buyer_role_to_add_fn')
        mes_text = ru.get('add_consumer_get_phone').format(
            role=role_text,
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name'),
            name=consumer_name
        )
        msg = bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            create_consumer_phone_fn,
            consumer_role=consumer_role,
            district_id=district_id,
            consumer_name=consumer_name
        )


def create_consumer_phone_fn(message, consumer_role=None, district_id=None, consumer_name=None):
    user_id = message.from_user.id
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_phone = replacer(message.text)
        agent = get_user_info(user_id).get('role')
        if agent == 'agent':
            consumer_id = create_consumer(
                consumer_role,
                consumer_name,
                district_id,
                consumer_phone,
                agent_id=user_id
            )
            if get_consumer_info(consumer_id).get('role') == 'seller':
                seller_prep_to_meet(consumer_id, user_id)
            else:
                buyer_prep_to_view(consumer_id, user_id)
        else:
            consumer_id = create_consumer(
                consumer_role,
                consumer_name,
                district_id,
                consumer_phone
            )
        if consumer_role == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_get_address').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_address_fn,
                consumer_id=int(consumer_id)
            )
        else:
            add_consumer_buyer_set_price(consumer_id, message=message)


def create_consumer_address_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_address = replacer(message.text)
        consumer_set_address(consumer_id, consumer_address)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        if get_consumer_info(consumer_id).get('role') == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_seller_get_price_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_seller_get_price_fn,
                consumer_id=consumer_id
            )
        else:
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_buyer_get_price_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_buyer_price_fn,
                consumer_id=consumer_id
            )


def create_consumer_seller_area_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_area = replacer(message.text)
        chek = consumer_set_area(consumer_id, consumer_area)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        role_text = ru.get('seller_role_to_add_fn')
        if chek:
            mes_text = ru.get('add_consumer_seller_get_floor_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=consumer_area,
                price=cinfo.get('price'),
                rooms=cinfo.get('rooms')
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floor_fn,
                consumer_id=consumer_id
            )
        else:
            mes_text = ru.get('add_consumer_seller_get_area_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_area_again_fn,
                consumer_id=consumer_id
            )


def create_consumer_seller_area_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_area = replacer(message.text)
        chek = consumer_set_area(consumer_id, consumer_area)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        role_text = ru.get('seller_role_to_add_fn')
        if chek:
            mes_text = ru.get('add_consumer_seller_get_floor_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=cinfo.get('price'),
                area=consumer_area,
                rooms=cinfo.get('rooms')
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floor_fn,
                consumer_id=consumer_id
            )
        else:
            mes_text = ru.get('add_consumer_seller_get_area_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_area_fn,
                consumer_id=consumer_id
            )


def create_consumer_seller_floor_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_floor = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        area = cinfo.get('area')
        role_text = ru.get('seller_role_to_add_fn')
        if consumer_floor.isdigit():
            mes_text = ru.get('add_consumer_seller_get_floor_house_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=cinfo.get('area'),
                price=cinfo.get('price'),
                rooms=cinfo.get('rooms'),
                floor=consumer_floor
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floors_house_fn,
                consumer_id=consumer_id,
                floor=consumer_floor
            )
        else:
            mes_text = ru.get('add_consumer_seller_get_floor_house_new_rel_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=cinfo.get('price'),
                area=area
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floor_again_fn,
                consumer_id=consumer_id
            )


def create_consumer_seller_floor_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_floor = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        area = cinfo.get('area')
        role_text = ru.get('seller_role_to_add_fn')
        if consumer_floor.isdigit():
            mes_text = ru.get('add_consumer_seller_get_floor_house_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=cinfo.get('area'),
                price=cinfo.get('price'),
                floor=consumer_floor
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floors_house_fn,
                consumer_id=consumer_id,
                floor=consumer_floor
            )
        else:
            mes_text = ru.get('add_consumer_seller_get_floor_house_new_rel_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=cinfo.get('price'),
                floor=cinfo.get('floor'),
                area=area
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floor_fn,
                consumer_id=consumer_id
            )


def create_consumer_seller_floors_house_fn(message, consumer_id=None, floor=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_house_floors = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        area = cinfo.get('area')
        role_text = ru.get('seller_role_to_add_fn')
        if consumer_house_floors.isdigit():
            agent_id = message.from_user.id
            consumer_set_floor(consumer_id, floor, consumer_house_floors)
            if get_user_info(agent_id).get('role') == 'agent':
                create_client_step(consumer_id, 'Назначена встреча', agent_id, 'seller')
                seller_prep_to_meet(consumer_id, agent_id)
                agent_create_task(consumer_id, 2, message=message)
            else:
                consumer_details(consumer_id, message=message)
        else:
            mes_text = ru.get('add_consumer_seller_get_floor_house_new_rel_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=cinfo.get('price'),
                floor=cinfo.get('floor'),
                area=area
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floors_house_again_fn,
                consumer_id=consumer_id,
                floor=floor
            )


def create_consumer_seller_floors_house_again_fn(message, consumer_id=None, floor=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_house_floors = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        area = cinfo.get('area')
        role_text = ru.get('seller_role_to_add_fn')
        if consumer_house_floors.isdigit():
            agent_id = message.from_user.id
            consumer_set_floor(consumer_id, floor, consumer_house_floors)
            if get_user_info(agent_id).get('role') == 'agent':
                create_client_step(consumer_id, 'Назначена встреча', agent_id, 'seller')
                seller_prep_to_meet(consumer_id, agent_id)
                agent_create_task(consumer_id, 2, message=message)
            else:
                consumer_details(consumer_id, message=message)
        else:
            mes_text = ru.get('add_consumer_seller_get_floors_house_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                area=area
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_seller_floors_house_fn,
                consumer_id=consumer_id,
                floor=floor
            )


def create_consumer_get_rooms_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_rooms = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        price = cinfo.get('price')
        if cinfo.get('role') == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
            if consumer_rooms.isdigit():
                consumer_set_rooms(consumer_id, consumer_rooms)
                rooms = get_consumer_info(consumer_id).get('rooms')
                mes_text = ru.get('add_consumer_seller_get_area_new_rel').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    price=price,
                    rooms=rooms
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_seller_area_fn,
                    consumer_id=consumer_id
                )
            else:
                mes_text = ru.get('add_consumer_seller_get_rooms_new_rel_again').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    price=price
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_get_rooms_again_fn,
                    consumer_id=consumer_id
                )
        else:
            if consumer_rooms.isdigit():
                consumer_set_rooms(consumer_id, consumer_rooms)
                agent_id = message.from_user.id
                if get_user_info(agent_id).get('role') == 'agent':
                    create_client_step(consumer_id, 'Назначен показ', agent_id, 'buyer')
                    seller_prep_to_meet(consumer_id, agent_id)
                    agent_create_task(consumer_id, 11, message=message)
                else:
                    consumer_details(consumer_id, message=message)
            else:
                role_text = ru.get('buyer_role_to_add_fn')
                mes_text = ru.get('add_consumer_buyer_get_rooms_again').format(
                    role=role_text,
                    town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                    district=get_district_info(cinfo.get('district_id')).get('name'),
                    name=consumer_name,
                    phone=consumer_phone
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_get_rooms_again_fn,
                    consumer_id=consumer_id
                )


def create_consumer_get_rooms_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_rooms = replacer(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        price = cinfo.get('price')
        if cinfo.get('role') == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
            if consumer_rooms.isdigit():
                consumer_set_rooms(consumer_id, consumer_rooms)
                mes_text = ru.get('add_consumer_seller_get_area_new_rel').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    price=price,
                    rooms=consumer_rooms
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_seller_area_fn,
                    consumer_id=consumer_id
                )
            else:
                mes_text = ru.get('add_consumer_seller_get_rooms_new_rel_again').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    price=price
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_get_rooms_fn,
                    consumer_id=consumer_id
                )
        else:
            if consumer_rooms.isdigit():
                consumer_set_rooms(consumer_id, consumer_rooms)
                agent_id = message.from_user.id
                if get_user_info(agent_id).get('role') == 'agent':
                    create_client_step(consumer_id, 'Назначен показ', agent_id, 'buyer')
                    seller_prep_to_meet(consumer_id, agent_id)
                    agent_create_task(consumer_id, 11, message=message)
                else:
                    consumer_details(consumer_id, message=message)
            else:
                role_text = ru.get('buyer_role_to_add_fn')
                mes_text = ru.get('add_consumer_buyer_get_rooms_again').format(
                    role=role_text,
                    town=get_town_by_district_id(cinfo.get('district_id')).get('name'),
                    district=get_district_info(cinfo.get('district_id')).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    price=price
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    create_consumer_get_rooms_fn,
                    consumer_id=consumer_id
                )


def date_time_meet_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        date_time = date_time_to_base_format(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        rooms = str(cinfo.get('rooms'))
        if date_time:
            agent_id = message.from_user.id
            mgid = get_current_st(consumer_id, agent_id).get('id')
            if cinfo.get('role') == 'seller':
                upd_stadi(2, mgid)
                create_client_step(consumer_id, 'Назначена встреча', agent_id, 'seller')
                create_agent_task(agent_id, consumer_id, 2, date_time)
                client_in_stadi_detail_menu(consumer_id, 'Назначен показ', message=message)
            else:
                upd_stadi(11, mgid)
                create_client_step(consumer_id, 'Назначен показ', agent_id, 'buyer')
                create_agent_task(agent_id, consumer_id, 11, date_time)
                client_in_stadi_detail_menu(consumer_id, 'Назначен показ', message=message)
        else:
            if cinfo.get('role') == 'seller':
                consumer_address = cinfo.get('address')
                area = cinfo.get('area')
                house_floors = cinfo.get('info').get('house_floors')
                floor = cinfo.get('info').get('floor')
                role_text = ru.get('seller_role_to_add_fn')
                consumer_price = cinfo.get('price')
                mes_text = ru.get('add_consumer_seller_get_date_time_meet').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    area=area,
                    house_floors=house_floors,
                    floor=floor,
                    rooms=rooms,
                    price=consumer_price
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    date_time_meet_again_fn,
                    consumer_id=consumer_id
                )
            else:
                role_text = ru.get('buyer_role_to_add_fn')
                mes_text = ru.get('add_consumer_buyer_get_date_time_meet_again').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    rooms=rooms
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    date_time_meet_again_fn,
                    consumer_id=consumer_id
                )


def date_time_meet_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        date_time = date_time_to_base_format(message.text)
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        rooms = str(cinfo.get('rooms'))
        if date_time:
            agent_id = message.from_user.id
            mgid = get_current_st(consumer_id, agent_id).get('id')
            if cinfo.get('role') == 'seller':
                upd_stadi(2, mgid)
                create_client_step(consumer_id, 'Назначена встреча', agent_id, 'seller')
                create_agent_task(agent_id, consumer_id, 2, date_time)
                client_in_stadi_detail_menu(consumer_id, 'Назначен показ', message=message)
            else:
                upd_stadi(11, mgid)
                create_client_step(consumer_id, 'Назначен показ', agent_id, 'buyer')
                create_agent_task(agent_id, consumer_id, 11, date_time)
                client_in_stadi_detail_menu(consumer_id, 'Назначен показ', message=message)
        else:
            if cinfo.get('role') == 'seller':
                consumer_address = cinfo.get('address')
                area = cinfo.get('area')
                house_floors = cinfo.get('info').get('house_floors')
                floor = cinfo.get('info').get('floor')
                role_text = ru.get('seller_role_to_add_fn')
                consumer_price = cinfo.get('price')
                mes_text = ru.get('add_consumer_seller_get_date_time_meet').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    address=consumer_address,
                    area=area,
                    house_floors=house_floors,
                    floor=floor,
                    rooms=rooms,
                    price=consumer_price
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    date_time_meet_fn,
                    consumer_id=consumer_id
                )
            else:
                role_text = ru.get('buyer_role_to_add_fn')
                mes_text = ru.get('add_consumer_buyer_get_date_time_meet_again').format(
                    role=role_text,
                    town=get_town_by_district_id(district_id).get('name'),
                    district=get_district_info(district_id).get('name'),
                    name=consumer_name,
                    phone=consumer_phone,
                    rooms=rooms
                )
                msg = bot.send_message(
                    message.chat.id,
                    text=mes_text,
                    parse_mode='html')
                bot.register_next_step_handler(
                    msg,
                    date_time_meet_fn,
                    consumer_id=consumer_id
                )


def create_seller_get_price_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_price = replacer(message.text).replace(' ', '').replace('-', '')
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        if consumer_price.isdigit():
            consumer_set_price(consumer_id, seller_price=consumer_price)
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_seller_get_rooms_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=consumer_price
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_get_rooms_fn,
                consumer_id=consumer_id
            )
        else:
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_seller_get_price_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_seller_get_price_again_fn,
                consumer_id=consumer_id
            )


def create_seller_get_price_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        consumer_price = replacer(message.text).replace(' ', '').replace('-', '')
        cinfo = get_consumer_info(consumer_id)
        district_id = cinfo.get('district_id')
        consumer_name = cinfo.get('name')
        consumer_phone = cinfo.get('phone')
        consumer_address = cinfo.get('address')
        if consumer_price.isdigit():
            consumer_set_price(consumer_id, seller_price=consumer_price)
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_seller_get_rooms_new_rel_again').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address,
                price=consumer_price
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_get_rooms_fn,
                consumer_id=consumer_id
            )
        else:
            role_text = ru.get('seller_role_to_add_fn')
            mes_text = ru.get('add_consumer_seller_get_price_new_rel').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone,
                address=consumer_address
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_seller_get_price_fn,
                consumer_id=consumer_id
            )


def create_buyer_price_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        buyer_price = replacer(message.text)
        chek = consumer_set_price(consumer_id, buyer_price=buyer_price)
        if chek:
            mes_text = add_consumer_get_rooms(consumer_id)
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_get_rooms_fn,
                consumer_id=consumer_id
            )
        else:
            cinfo = get_consumer_info(consumer_id)
            district_id = cinfo.get('district_id')
            consumer_name = cinfo.get('name')
            consumer_phone = cinfo.get('phone')
            role_text = ru.get('buyer_role_to_add_fn')
            mes_text = ru.get('add_consumer_buyer_get_price_diap').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_buyer_price_again_fn,
                consumer_id=consumer_id
            )


def create_buyer_price_again_fn(message, consumer_id=None):
    if message.text in cancel:
        keymenu(message)
    else:
        buyer_price = replacer(message.text)
        chek = consumer_set_price(consumer_id, buyer_price=buyer_price)
        if chek:
            mes_text = add_consumer_get_rooms(consumer_id)
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_get_rooms_fn,
                consumer_id=consumer_id
            )
        else:
            cinfo = get_consumer_info(consumer_id)
            district_id = cinfo.get('district_id')
            consumer_name = cinfo.get('name')
            consumer_phone = cinfo.get('phone')
            role_text = ru.get('buyer_role_to_add_fn')
            mes_text = ru.get('add_consumer_buyer_get_price_diap').format(
                role=role_text,
                town=get_town_by_district_id(district_id).get('name'),
                district=get_district_info(district_id).get('name'),
                name=consumer_name,
                phone=consumer_phone
            )
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_buyer_price_fn,
                consumer_id=consumer_id
            )


def get_task_date_time_fn(message, consumer_id=None, sid=None):
    if message.text in cancel:
        keymenu(message)
    else:
        date_time = date_time_to_base_format(message.text)
        if date_time:
            agent_id = message.from_user.id
            create_agent_task(agent_id, consumer_id, sid, date_time)
            agent_task_menu(message=message)
            sid = get_client_stepname(consumer_id)
            client_in_stadi_detail_menu(consumer_id, sid, message=message)
        else:
            mes_text = ru.get('task_get_time_again')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                get_task_date_time_again_fn,
                consumer_id=consumer_id,
                sid=sid)


def get_task_date_time_again_fn(message, consumer_id=None, sid=None):
    if message.text in cancel:
        keymenu(message)
    else:
        date_time = date_time_to_base_format(message.text)
        if date_time:
            agent_id = message.from_user.id
            create_agent_task(agent_id, consumer_id, sid, date_time)
            sid = get_client_stepname(consumer_id)
            client_in_stadi_detail_menu(consumer_id, sid, message=message)
        else:
            mes_text = ru.get('task_get_time_again')
            msg = bot.send_message(
                message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                get_task_date_time_fn,
                consumer_id=consumer_id,
                sid=sid)


def chek_phone(message):
    user_id = message.from_user.id
    phone = cheking_manager_phone(user_id, message.contact.phone_number)
    if phone:
        startmenu(message)
    else:
        mes_text = ru.get('no_match_phone').format(uid=user_id)
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html')


###################################################


# Регистрация
@bot.message_handler(commands=['start', 'Start'])
def start(message):
    startmenu(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'document'])
def menu(message):
    if message.text.startswith('79'):
        user = Manager.get_or_none(Manager.phone == message.text)
        if user is not None:
            user_id = message.from_user.id
            Manager.update(user_id=user_id, status=1).where(Manager.phone == message.text).execute()
            if user.role == 'admin':
                Admin.update(user_id=user_id).where(Admin.phone == message.text).execute()
    elif message.text in cancel:
        keymenu(message)
    else:
        pass


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if 'CPD=' in c.data:
        user_id = c.from_user.id
        consumer_id = int(c.data.split('=')[1])
        bprice = {
            'min': int(c.data.split('=')[2]),
            'max': int(c.data.split('=')[3])
        }
        edt = int(c.data.split('=')[4])
        consumer_set_price(consumer_id, buyer_price=bprice)
        if edt:
            consumer_update_price_diap(consumer_id, bprice)
            if get_user_info(user_id).get('role') == 'manager':
                consumer_details(consumer_id, c=c)
            else:
                sid = get_client_stepname(consumer_id)
                client_edit_menu(consumer_id, sid, c=c)
        else:
            mes_text = add_consumer_get_rooms(consumer_id)
            msg = bot.send_message(
                c.message.chat.id,
                text=mes_text,
                parse_mode='html')
            bot.register_next_step_handler(
                msg,
                create_consumer_get_rooms_fn,
                consumer_id=consumer_id
            )

    if 'AGS|' in c.data:
        agent_id = c.from_user.id
        consumer_id = int(c.data.split('|')[1])
        sid = int(c.data.split('|')[2])
        subsid = int(c.data.split('|')[3])
        subsubsid = int(c.data.split('|')[4])
        step = int(c.data.split('|')[5])
        agent_stadies(
            consumer_id,
            sid,
            subsid,
            subsubsid,
            step,
            c=c
        )

    if 'отчеты%' in c.data:
        diap = c.data.split('%')[1]
        agents_boss_list(c, diap)

    if 'OA+' in c.data:
        agent_id = int(c.data.split('+')[1])
        diap = c.data.split('+')[2]
        agent_otchet(c, agent_id, diap)

    if 'CLA#' in c.data:
        consumer_id = c.data.split('#')[1]
        sid = c.data.split('#')[2]
        uid = int(c.data.split('#')[3])
        boss_client_in_stadi_detail_menu(uid, consumer_id, sid, c=c)

    if 'AS!' in c.data:
        stadi = c.data.split('!')[1]
        consumer_role = c.data.split('!')[2]
        if consumer_role == 's':
            consumer_role = 'seller'
        else:
            consumer_role = 'buyer'
        agent_id = c.data.split('!')[3]
        boss_agent_client_list_in_stadi(agent_id, stadi, consumer_role, c=c)

    if 'агент=' in c.data:
        agent_id = int(c.data.split('=')[1])
        consumer_role = c.data.split('=')[2]
        boss_agent_clients_in_stadies(consumer_role, agent_id, c=c)

    if 'agents-' in c.data:
        consumer_role = c.data.split('-')[1]
        boss_agents_menu(consumer_role, c=c)

    if 'boss_' in c.data:
        consumer_role = c.data.split('_')[1]
        boss_sub_menu(consumer_role, c=c)

    if 'deltas>' in c.data:
        agent_id = c.from_user.id
        datastr = c.data.split('>')
        consumer_id = datastr[1]
        sid = datastr[2]
        date = datastr[3]
        tm = datastr[4]
        date_time = date + ' ' + tm
        date_time = Basedate().datestart_formatter(date_time)
        create_agent_task(agent_id, consumer_id, sid, date_time)
        sid = get_client_stepname(consumer_id)
        client_in_stadi_detail_menu(consumer_id, sid, c=c)

    if 'DAY' in c.data:
        task_time_menu(c.data, c=c)

    if '-MONTH' in c.data:
        medt = c.data.split(';')[0].split('-')[0]
        year = int(c.data.split(';')[1])
        month = int(c.data.split(';')[2])
        cbk = c.data.split(';')[4]
        if medt == 'NEXT':
            month = month + 1
            if month > 12:
                year = year + 1
                month = 1
        else:
            month = month - 1
            if month == 0:
                year = year - 1
                month = 12
        sid = int(cbk.split('-')[1])
        task_name = get_stadi_info(sid).get('name')
        mes_text = ru.get('task_get_time').format(
            task=task_name,
            date=Basedate().date_mdh_ru()
        )
        markup = create_calendar(year=year, month=month, cb=cbk)
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=markup)

    if 'AGT_' in c.data:
        task_id = int(c.data.split('_')[1])
        agent_task_detail_menu(task_id, c=c)

    if c.data == 'tasks':
        agent_task_menu(c=c)

    if 'ST|' in c.data:
        agent_id = c.from_user.id
        consumer_id = int(c.data.split('|')[1])
        sid = get_current_sid(consumer_id, agent_id)
        subsid = int(c.data.split('|')[3])
        subsubsid = int(c.data.split('|')[4])
        step = int(c.data.split('|')[5])
        stadies(
            consumer_id,
            sid,
            subsid,
            subsubsid,
            step,
            c
        )

    if 'getclient$' in c.data:
        consumer_id = int(c.data.split('$')[1])
        agent_id = c.from_user.id
        consumer_set_manager_id(consumer_id, agent_id)
        if get_consumer_info(consumer_id).get('role') == 'seller':
            create_client_step(consumer_id, 'Назначена встреча', agent_id, 'seller')
            seller_prep_to_meet(consumer_id, agent_id)
            agent_create_task(consumer_id, 2, c=c)
        else:
            create_client_step(consumer_id, 'Назначен показ', agent_id, 'buyer')
            seller_prep_to_meet(consumer_id, agent_id)
            agent_create_task(consumer_id, 11, c=c)

    if 'стадия!' in c.data:
        sid = c.data.split('!')[1]
        consumer_role = c.data.split('!')[2]
        agent_client_list_in_stadi(sid, consumer_role, c=c)

    if 'клагст#' in c.data:
        consumer_id = c.data.split('#')[1]
        sid = c.data.split('#')[2]
        client_in_stadi_detail_menu(consumer_id, sid, c=c)

    if 'редкл@' in c.data:
        consumer_id = int(c.data.split('@')[1])
        sid = c.data.split('@')[2]
        client_edit_menu(consumer_id, sid, c=c)

    if 'aC@' in c.data:
        user_id = c.from_user.id
        district_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        price_min = int(c.data.split('@')[3])
        price_max = int(c.data.split('@')[4])
        rooms = int(c.data.split('@')[5])
        consumer_id = int(c.data.split('@')[6])
        prices = {'min': price_min, 'max': price_max}
        if admininfo(user_id):
            boss_consumer_details(consumer_id, prices, c=c)
        else:
            try:
                fnd = int(c.data.split('@')[7])
                agent_client_fileterd_detail_menu_no_contacts(
                    consumer_role,
                    district_id,
                    prices,
                    rooms,
                    consumer_id,
                    c=c,
                    fnd=fnd
                )
            except:
                agent_client_fileterd_detail_menu_no_contacts(
                    consumer_role,
                    district_id,
                    prices,
                    rooms,
                    consumer_id,
                    c=c
                )

    if 'ClI@' in c.data:
        user_id = c.from_user.id
        district_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        price_min = int(c.data.split('@')[3])
        price_max = int(c.data.split('@')[4])
        rooms = int(c.data.split('@')[5])
        consumer_id = int(c.data.split('@')[6])
        prices = {'min': price_min, 'max': price_max}
        if admininfo(user_id):
            boss_consumer_details(consumer_id, prices, c=c)
        else:
            agent_client_fileterd_detail_menu(
                consumer_role,
                district_id,
                prices,
                rooms,
                consumer_id,
                c=c
            )

    if 'Ar@' in c.data:
        user_id = c.from_user.id
        district_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        price_min = int(c.data.split('@')[3])
        price_max = int(c.data.split('@')[4])
        rooms = int(c.data.split('@')[5])
        page = int(c.data.split('@')[6])
        prices = {'min': price_min, 'max': price_max}
        if admininfo(user_id):
            boss_filter_clients_menu(
                consumer_role,
                district_id,
                prices,
                rooms,
                c=c
            )
        else:
            try:
                fnd = int(c.data.split('@')[7])
                agent_filter_clients_menu(
                    consumer_role,
                    district_id,
                    prices,
                    rooms,
                    c=c,
                    fnd=fnd
                )
            except:
                agent_filter_clients_menu(
                    consumer_role,
                    district_id,
                    prices,
                    rooms,
                    c=c
                )

    if 'Fpr@' in c.data:
        user_id = c.from_user.id
        district_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        price_min = int(c.data.split('@')[3])
        price_max = int(c.data.split('@')[4])
        prices = {'min': price_min, 'max': price_max}
        if admininfo(user_id):
            boss_base_view_select_rooms(consumer_role, district_id, prices, c=c)
        else:
            try:
                fnd = int(c.data.split('@')[5])
                agent_base_view_select_rooms(consumer_role, district_id, prices, c=c, fnd=fnd)
            except:
                agent_base_view_select_rooms(consumer_role, district_id, prices, c=c)

    if 'agfbdistrict@' in c.data:
        user_id = c.from_user.id
        district_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        if admininfo(user_id):
            boss_base_view_select_prices_diap_menu(consumer_role, district_id, c=c)
        else:
            try:
                fnd = int(c.data.split('@')[3])
                agent_base_view_select_prices_diap_menu(consumer_role, district_id, c=c, fnd=fnd)
            except:
                agent_base_view_select_prices_diap_menu(consumer_role, district_id, c=c)

    if 'agbftown@' in c.data:
        user_id = c.from_user.id
        town_id = c.data.split('@')[1]
        consumer_role = c.data.split('@')[2]
        if admininfo(user_id):
            boss_base_view_select_district_menu(consumer_role, town_id, c=c)
        else:
            try:
                fnd = int(c.data.split('@')[3])
                agent_base_view_select_district_menu(consumer_role, town_id, c=c, fnd=fnd)
            except:
                agent_base_view_select_district_menu(consumer_role, town_id, c=c)

    if 'base@' in c.data:
        consumer_role = c.data.split('@')[1]
        agent_base_view_select_town_menu(consumer_role, c=c)

    if c.data == 'menu':
        user_id = c.from_user.id
        role = get_user_info(user_id).get('role')
        if role == 'manager':
            manager_menu(c=c)
        elif role == 'agent':
            agent_start_menu(c=c)
        else:
            boss_main_menu(c=c)

    if 'agentmenu*' in c.data:
        consumer_role = c.data.split('*')[1]
        agent_main_menu(consumer_role, c=c)

    if 'findseller/' in c.data:
        consumer_id = int(c.data.split('/')[1])
        find_seller(consumer_id, c=c)

    if 'FIND&' in c.data:
        consumer_id = int(c.data.split('&')[1])
        agent_find_seller(consumer_id, c=c)

    if 'ADD>S@B+' in c.data:
        consumer_id = int(c.data.split('+')[1])
        var_id = int(c.data.split('+')[1])
        agent_seller_finded_menu(consumer_id, var_id, c=c)

    if 'SELECT&' in c.data:
        buyer_id = int(c.data.split('&')[1])
        seller_id = int(c.data.split('&')[2])
        agent_selected_seller_to_buyer(buyer_id, seller_id, c=c)

    if 'NXTDO&' in c.data:
        consumer_id = int(c.data.split('&')[1])
        agent_create_task(consumer_id, 17, c=c)

    if 'FD-' in c.data:
        consumer_id = int(c.data.split('-')[1])
        agent_base_view_select_town_menu('seller', c=c, fnd=consumer_id)

    if 'addsellertobuyer+' in c.data:
        buyer_id = int(c.data.split('+')[1])
        seller_id = int(c.data.split('+')[2])
        buyer_update_seller_var(buyer_id, seller_id)
        consumer_details(buyer_id, c=c)

    if 'cons_ename=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_name')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_name_fn,
            consumer_id=consumer_id)

    if 'cons_ephone=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_phone')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_phone_fn,
            consumer_id=consumer_id)

    if 'cons_eaddress=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_address')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_address_fn,
            consumer_id=consumer_id)

    if 'cons_earea=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_area')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_area_fn,
            consumer_id=consumer_id)

    if 'cons_efloorshouse=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_floors_house')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_floors_house_fn,
            consumer_id=consumer_id)

    if 'cons_efloor=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_floor')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_floor_fn,
            consumer_id=consumer_id)

    if 'cons_eprice=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_price')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_price_fn,
            consumer_id=consumer_id)

    if 'cons_erooms=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        mes_text = ru.get('edit_consumer_rooms')
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            edit_consumer_rooms_fn,
            consumer_id=consumer_id)

    if 'cons_epricesdiap=' in c.data:
        consumer_id = int(c.data.split('=')[1])
        add_consumer_buyer_set_price(consumer_id, c=c, upd=True)

    if 'клиенты*' in c.data:
        page = int(c.data.split('*')[1])
        consumer_role = c.data.split('*')[2]
        user_id = c.from_user.id
        if get_user_info(user_id).get('role') == 'agent':
            #  agent_clients_menu(consumer_role, c=c, page=page)
            agent_clients_in_stadies(consumer_role, c=c)
        else:
            if admininfo(user_id):
                # boss_clients_menu(consumer_role, c=c, page=page)
                boss_base_view_select_town_menu(consumer_role, c=c)
            else:
                clients_menu(consumer_role, c=c, page=page)

    if 'клиент-' in c.data:
        user_id = c.from_user.id
        consumer_id = int(c.data.split('-')[1])
        if admininfo(user_id):
            # boss_consumer_details(consumer_id, c=c)
            pass
        else:
            consumer_details(consumer_id, c=c)

    if 'add_consumer%' in c.data:
        consumer_role = c.data.split('%')[1]
        add_consumer_select_town(consumer_role, c=c)

    if 'выбор_города%' in c.data:
        town_id = int(c.data.split('%')[1])
        consumer_role = c.data.split('%')[2]
        add_consumer_select_district(consumer_role, town_id, c=c)

    if 'выбор_района>' in c.data:
        district_id = int(c.data.split('>')[1])
        consumer_role = c.data.split('>')[2]
        if consumer_role == 'seller':
            role_text = ru.get('seller_role_to_add_fn')
        else:
            role_text = ru.get('buyer_role_to_add_fn')
        mes_text = ru.get('add_consumer_get_name').format(
            role=role_text,
            town=get_town_by_district_id(district_id).get('name'),
            district=get_district_info(district_id).get('name')
        )
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html')
        bot.register_next_step_handler(
            msg,
            create_consumer_name_fn,
            consumer_role=consumer_role,
            district_id=district_id)

    if 'consumers*' in c.data:
        page = int(c.data.split('*')[1])
        status = int(c.data.split('*')[2])
        consumers_menu(c=c, status=status, page=page)

    if 'users!' in c.data:
        page = int(c.data.split('!')[1])
        role = c.data.split('!')[2]
        users_menu(c=c, role=role, page=page)

    if c.data == 'usersmenu':
        choose_role_users_menu(c=c)

    if c.data == 'регистрация':
        mes_text = ru.get('chek_phone_mess')
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True)
        button_phone = types.KeyboardButton(
            text=ru.get('send_phone'),
            request_contact=True)
        keyboard.add(button_phone)
        msg = bot.send_message(
            c.message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
        bot.register_next_step_handler(msg, chek_phone)


###################################################

bot.remove_webhook()

bot.set_webhook(
    url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
