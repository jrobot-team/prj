# -*- coding: utf-8 -*-
from dbclasses import Consumer, District, TownDistricts, Town, Prices
from bot_utils import str_to_array, Basedate, array_to_str


def get_consumers_by_role(role, status=None):
    consumers = []
    if role == 'all':
        if status is not None:
            query = Consumer.select().where(Consumer.status == status)
        else:
            query = Consumer.select()
    else:
        if status is not None:
            query = Consumer.select().where(Consumer.role == role, Consumer.status == status)
        else:
            query = Consumer.select().where(Consumer.role == role)
    for consumer in query:
        consumers.append(
            {
                'id': consumer.id,
                'name': consumer.name,
                'phone': consumer.phone,
                'role': consumer.role,
                'group_id': consumer.group_id,
                'district_id': consumer.district_id,
                'price': int(consumer.price),
                'prices_id': consumer.prices_id,
                'address': consumer.address,
                'area': consumer.area,
                'rooms': consumer.rooms,
                'manager_id': consumer.manager_id,
                'info': str_to_array(consumer.info),
                'status': consumer.status,
                'var_id': consumer.var_id
            }
        )
    return consumers


def create_consumer(role, name, district_id, phone, agent_id=0):
    date_create = Basedate().date_hms()
    info = {
        'floor': 1,
        'house_floors': 10,
        'seller_id': 0
    }
    Consumer.create(
        date_create=date_create,
        name=name,
        role=role,
        phone=phone,
        district_id=district_id,
        manager_id=agent_id,
        info=array_to_str(info)
    )
    consumer_id = Consumer.get(Consumer.date_create == date_create, Consumer.name == name).id
    return consumer_id


def consumer_update_name(consumer_id, name):
    Consumer.update(name=name).where(Consumer.id == consumer_id).execute()


def consumer_update_phone(consumer_id, phone):
    Consumer.update(phone=phone).where(Consumer.id == consumer_id).execute()


def consumer_update_role(consumer_id, role):
    Consumer.update(role=role).where(Consumer.id == consumer_id).execute()


def consumer_put_to_group(consumer_id, group_id):
    Consumer.update(group_id=int(group_id)).where(Consumer.id == consumer_id).execute()


def consumer_update_district(consumer_id, district_id):
    Consumer.update(district_id=int(district_id)).where(Consumer.id == consumer_id).execute()


def consumer_set_price(consumer_id, buyer_price=None, seller_price=None):
    if seller_price:
        Consumer.update(price=float(seller_price)).where(Consumer.id == consumer_id).execute()
    else:
        Prices.create(
            name=consumer_id,
            price_min=float(buyer_price.get('min')),
            price_max=float(buyer_price.get('max'))
        )
        prices_id = Prices.get(Prices.name == consumer_id).id
        Consumer.update(prices_id=prices_id).where(Consumer.id == consumer_id).execute()
    return consumer_id


def consumer_update_price_diap(consumer_id, prices):
    prices_id = get_consumer_info(consumer_id).get('prices_id')
    pmin = float(prices.get('min'))
    pmax = float(prices.get('max'))
    Prices.update(price_min=pmin, price_max=pmax).where(Prices.id == prices_id).execute()


def consumer_set_address(consumer_id, address):
    Consumer.update(address=address).where(Consumer.id == consumer_id).execute()


def consumer_set_area(consumer_id, area):
    area = area.replace(',', '.')
    try:
        Consumer.update(area=float(area)).where(Consumer.id == consumer_id).execute()
    except:
        consumer_id = None
    return consumer_id


def consumer_set_rooms(consumer_id, rooms):
    Consumer.update(rooms=int(rooms)).where(Consumer.id == consumer_id).execute()


def consumer_set_floor(consumer_id, floor, house_floors):
    old_info = str_to_array(Consumer.get(Consumer.id == consumer_id).info)
    info = {
        'floor': int(floor),
        'house_floors': int(house_floors),
        'seller_id': old_info.get('seller_id')
    }
    Consumer.update(info=array_to_str(info)).where(Consumer.id == consumer_id).execute()


def consumer_update_floors_house(consumer_id, floors):
    info = get_consumer_info(consumer_id).get('info')
    floor = info.get('floor')
    house_floors = int(floors)
    to_base = {
        'floor': int(floor),
        'house_floors': int(house_floors),
        'seller_id': info.get('seller_id')
    }
    Consumer.update(info=array_to_str(to_base)).where(Consumer.id == consumer_id).execute()


def consumer_update_floor(consumer_id, floor):
    info = get_consumer_info(consumer_id).get('info')
    floor = floor
    house_floors = info.get('house_floors')
    to_base = {
        'floor': int(floor),
        'house_floors': int(house_floors),
        'seller_id': info.get('seller_id')
    }
    Consumer.update(info=array_to_str(to_base)).where(Consumer.id == consumer_id).execute()


def consumer_set_manager_id(consumer_id, manager_id):
    Consumer.update(manager_id=int(manager_id)).where(Consumer.id == consumer_id).execute()


def consumer_set_status(consumer_id, status):
    Consumer.update(status=int(status)).where(Consumer.id == consumer_id).execute()


def get_consumer_info(consumer_id):
    try:
        consumerinfo = {
            'id': Consumer.get(Consumer.id == consumer_id).id,
            'name': Consumer.get(Consumer.id == consumer_id).name,
            'phone': Consumer.get(Consumer.id == consumer_id).phone,
            'role': Consumer.get(Consumer.id == consumer_id).role,
            'group_id': Consumer.get(Consumer.id == consumer_id).group_id,
            'district_id': Consumer.get(Consumer.id == consumer_id).district_id,
            'price': int(Consumer.get(Consumer.id == consumer_id).price),
            'prices_id': Consumer.get(Consumer.id == consumer_id).prices_id,
            'address': Consumer.get(Consumer.id == consumer_id).address,
            'area': Consumer.get(Consumer.id == consumer_id).area,
            'rooms': Consumer.get(Consumer.id == consumer_id).rooms,
            'manager_id': Consumer.get(Consumer.id == consumer_id).manager_id,
            'info': str_to_array(Consumer.get(Consumer.id == consumer_id).info),
            'status': Consumer.get(Consumer.id == consumer_id).status,
            'var_id': Consumer.get(Consumer.id == consumer_id).var_id
        }
    except:
        consumerinfo = None
    return consumerinfo


def get_consumers_by_district_id(district_id):
    query = Consumer.select().where(Consumer.district_id == district_id)
    consumers = []
    for consumer in query:
        consumerinfo = get_consumer_info(consumer.id)
        consumers.append(
            consumerinfo
        )
    return consumers


def create_district(name, town_id):
    date_create = Basedate().date_hms()
    District.create(
        date_create=date_create,
        name=name
    )
    district_id = District.get(District.date_create == date_create, District.name == name).id
    TownDistricts.create(
        town_id=town_id,
        district_id=district_id
    )
    return district_id


def get_district_info(district_id):
    try:
        dinfo = {
            'id': District.get(District.id == district_id).id,
            'name': District.get(District.id == district_id).name,
            'description': District.get(District.id == district_id).description,
            'info': str_to_array(District.get(District.id == district_id).info),
            'status': District.get(District.id == district_id).status,
        }
    except:
        dinfo = None
    return dinfo


def get_districts_by_town_id(town_id):
    query = TownDistricts.select().where(TownDistricts.town_id == town_id)
    dids = []
    districts = []
    for did in query:
        dids.append(
            did.id
        )
    for district_id in dids:
        dinfo = get_district_info(district_id)
        districts.append(
            dinfo
        )
    return districts


def get_town_by_district_id(district_id):
    town_id = TownDistricts.get(TownDistricts.district_id == district_id).town_id
    return get_town_info(town_id)


def get_all_towns_info():
    query = Town.select()
    towns = []
    for town in query:
        districts = get_districts_by_town_id(town.id)
        towns.append(
            {
                'id': town.id,
                'name': town.name,
                'description': town.description,
                'info': str_to_array(town.info),
                'status': town.status,
                'districts': districts
            }
        )
    return towns


def get_town_info(town_id):
    try:
        districts = get_districts_by_town_id(town_id)
        towninfo = {
            'id': Town.get(Town.id == town_id).id,
            'name': Town.get(Town.id == town_id).name,
            'description': Town.get(Town.id == town_id).description,
            'info': str_to_array(Town.get(Town.id == town_id).info),
            'status': Town.get(Town.id == town_id).status,
            'districts': districts
        }
    except:
        towninfo = None
    return towninfo


def create_town(name):
    date_create = Basedate().date_hms()
    Town.create(
        date_create=date_create,
        name=name
    )
    town_id = Town.get(Town.date_create == date_create, Town.name == name).id
    return town_id


def get_prices_diap(prices_id):
    try:
        prices_diap = {
            'price_min': int(Prices.get(Prices.id == prices_id).price_min),
            'price_max': int(Prices.get(Prices.id == prices_id).price_max),
        }
    except:
        prices_diap = {
            'price_min': 0.0,
            'price_max': 0.0,
        }
    return prices_diap


def find_sellers_to_buyers(consumer_id):
    cinfo = get_consumer_info(consumer_id)
    rooms = cinfo.get('rooms')
    district_id = cinfo.get('district_id')
    sellers_query = Consumer.select().where(
        Consumer.district_id == district_id,
        Consumer.rooms == rooms,
        Consumer.role == 'seller',
        Consumer.var_id == 0
    )
    sellers = []
    for seller in sellers_query:
        sinfo = get_consumer_info(seller.id)
        sellers.append(
            sinfo
        )
    return sellers


def buyer_update_seller_var(buyer_id, seller_id):
    """
    Здесь надо бобавить проверку на наличие менеджера и отправки менеджеру уведомления
    """
    seller_info = get_consumer_info(seller_id).get('info')
    buyer_info = {
        'floor': seller_info.get('floor'),
        'house_floors': seller_info.get('house_floors'),
        'seller_id': seller_id
    }
    Consumer.update(info=array_to_str(buyer_info), var_id=seller_id).where(Consumer.id == buyer_id).execute()
    Consumer.update(var_id=buyer_id).where(Consumer.id == seller_id).execute()
