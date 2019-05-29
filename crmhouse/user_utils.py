# -*- coding: utf-8 -*-
import csv
import pytz
from config import TIMEZONE
from datetime import datetime
from dbclasses import Manager, Group, Admin
from bot_utils import str_to_array


def get_users_by_role(role='manager'):
    managers = []
    if role == 'all':
        query = Manager.select()
    else:
        query = Manager.select().where(Manager.role == role)
    for manager in query:
        managers.append(
            {
                'id': manager.id,
                'date_create': manager.date_create,
                'user_id': manager.user_id,
                'name': manager.name,
                'phone': manager.phone,
                'role': manager.role,
                'group_id': manager.group_id,
                'description': manager.description,
                'info': str_to_array(manager.info),
                'status': manager.status
            }
        )
    return managers


def get_user_info(user_id):
    try:
        userinfo = {
            'id': Manager.get(Manager.user_id == user_id).id,
            'user_id': Manager.get(Manager.user_id == user_id).user_id,
            'name': Manager.get(Manager.user_id == user_id).name,
            'phone': Manager.get(Manager.user_id == user_id).phone,
            'role': Manager.get(Manager.user_id == user_id).role,
            'group_id': Manager.get(Manager.user_id == user_id).group_id,
            'description': Manager.get(Manager.user_id == user_id).description,
            'info': str_to_array(Manager.get(Manager.user_id == user_id).info),
            'status': Manager.get(Manager.user_id == user_id).status
        }
    except:
        userinfo = None
    return userinfo


def get_user_info_by_id(uid):
    try:
        userinfo = {
            'id': Manager.get(Manager.id == uid).id,
            'user_id': Manager.get(Manager.id == uid).user_id,
            'name': Manager.get(Manager.id == uid).name,
            'phone': Manager.get(Manager.id == uid).phone,
            'role': Manager.get(Manager.id == uid).role,
            'group_id': Manager.get(Manager.id == uid).group_id,
            'description': Manager.get(Manager.id == uid).description,
            'info': str_to_array(Manager.get(Manager.id == uid).info),
            'status': Manager.get(Manager.id == uid).status
        }
    except:
        userinfo = None
    return userinfo


def reg_user(user_id, name):
    date_create = datetime.now(pytz.timezone(TIMEZONE))
    Manager.create(
        date_create=date_create,
        user_id=user_id,
        name=name,
        phone='+79001112233',
        role='agent',
        status=1
    )


def cheking_manager_phone(user_id, phone):
    phone = phone.replace('+', '')
    try:
        phone = Manager.get(Manager.phone == int(phone)).phone
    except:
        phone = False
    if phone:
        Manager.update(user_id=user_id, status=1).where(Manager.phone == int(phone)).execute()
        role = get_user_info(user_id).get('role')
        if role == 'admin':
            Admin.update(user_id=user_id).where(Admin.phone == int(phone)).execute()
    return phone


def csv_reader():
    with open('managers_.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        fline = 0
        for row in spamreader:
            if fline:
                if row:
                    name = row[0]
                    group = row[1]
                    role = row[2]
                    phone = row[3]
                    if role == 'Руководитель':
                        dbrole = 'admin'
                        Group.create(
                            owner_id=-1,
                            name=group
                        )
                        Admin.create(
                            user_id=-1,
                            phone=phone
                        )
                    elif role == 'Агент':
                        dbrole = 'agent'
                    else:
                        dbrole = 'manager'
                    date_create = datetime.now(pytz.timezone(TIMEZONE))
                    Manager.create(
                        date_create=date_create,
                        user_id=-1,
                        name=name,
                        phone=phone,
                        role=dbrole,
                        description=group,
                        status=0
                    )
            fline += 1
    admins_query = Manager.select().where(Manager.role == 'admin')
    for admin in admins_query:
        phone = admin.phone
        group = admin.description
        aid = Admin.get(Admin.phone == phone).id
        Manager.update(group_id=aid).where(Manager.description == group).execute()
