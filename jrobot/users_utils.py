# -*- coding: utf-8 -*-
from bot_utils import str_to_array, array_to_str
from dbclasses import User, Group, GroupUsers, Lang
from bot_utils import Basedate
from alerter import alert_new_user


def username_getter(message=None, c=None):
    if c:
        name = c.from_user.first_name
        fam = c.from_user.last_name
        username = c.from_user.username
        if fam and name:
            username = name + ' ' + fam
        else:
            if name:
                username = name
    else:
        name = message.from_user.first_name
        fam = message.from_user.last_name
        username = message.from_user.username
        if fam and name:
            username = name + ' ' + fam
        else:
            if name:
                username = name
    return username


def reg_user(user_id, username, refer_id=0):
    if refer_id:
        status = 0
    else:
        refer_id = 0
        status = 1
    info = {
        'date_reg': Basedate().date(),
        'refer_id': refer_id
    }
    User.create(
        user_id=user_id,
        name=username,
        info=array_to_str(info),
        status=status,
        refer=refer_id
    )
    if refer_id:
        groupinfo = get_group_info_by_owner(refer_id)
        put_user_to_group(groupinfo.get('id'), user_id)
        alert_new_user(user_id, refer_id)


def get_user_status(user_id):
    status = User.get(User.user_id == user_id).status
    return status


def remove_user_from_group(user_id):
    GroupUsers.delete().where(GroupUsers.user_id == user_id).execute()
    User.update(refer=0).where(User.user_id == user_id).execute()


def isuser(user_id):
    try:
        user_id = User.get(
            User.user_id == user_id
        ).user_id
    except:
        user_id = None
    return user_id


def get_user_info(user_id):
    try:
        userinfo = {
            'id': User.get(User.user_id == user_id).id,
            'user_id': user_id,
            'name': User.get(User.user_id == user_id).name,
            'role': User.get(User.user_id == user_id).role,
            'info': str_to_array(User.get(User.user_id == user_id).info),
            'status': User.get(User.user_id == user_id).status,
            'refer_id': User.get(User.user_id == user_id).refer,
        }
    except:
        userinfo = None
    return userinfo


def upd_user_lang(user_id, lang):
    Lang.update(lang=lang).where(User.user_id == user_id).execute()


def get_group_info_by_owner(user_id):
    try:
        groupinfo = {
            'id': Group.get(Group.owner_id == user_id).id,
            'owner_id': user_id,
            'name': Group.get(Group.owner_id == user_id).name,
            'info': str_to_array(Group.get(Group.owner_id == user_id).info),
        }
    except:
        groupinfo = None
    return groupinfo


def get_group_info_by_id(group_id):
    try:
        groupinfo = {
            'id': Group.get(Group.id == group_id).id,
            'owner_id': Group.get(Group.id == group_id).owner_id,
            'name': Group.get(Group.id == group_id).name,
            'info': str_to_array(Group.get(Group.id == group_id).info),
        }
    except:
        groupinfo = None
    return groupinfo


def put_user_to_group(group_id, user_id):
    try:
        old_group_id = GroupUsers.get(GroupUsers.user_id == user_id).group_id
        if old_group_id == group_id:
            pass
        else:
            GroupUsers.update(
                group_id=group_id
            ).where(GroupUsers.user_id == user_id).execute()
    except:
        GroupUsers.create(
            group_id=group_id,
            user_id=user_id
        )


def is_user_owner(user_id):
    try:
        group_id = Group.get(Group.owner_id == user_id).id
    except:
        group_id = None
    return group_id


def is_user_in_group(user_id):
    try:
        group_id = GroupUsers.get(GroupUsers.user_id == user_id).group_id
    except:
        group_id = None
    return group_id


def update_user_info(user_id, info):
    User.update(
        info=array_to_str(info)
    ).where(User.user_id == user_id).execute()


def update_username(user_id, username):
    User.update(
        name=username
    ).where(User.user_id == user_id).execute()


def update_role(user_id, role):
    User.update(
        role=role
    ).where(User.user_id == user_id).execute()


def update_user_status(user_id, status):
    User.update(
        status=status
    ).where(User.user_id == user_id).execute()


def get_all_users():
    users = []
    query = User.select()
    for user in query:
        users.append(
            {
                'id': user.id,
                'user_id': user.user_id,
                'name': user.name,
                'role': user.role,
                'info': str_to_array(user.info),
                'status': user.status,
                'refer_id': user.refer
            }
        )
    return users


def get_refer_users(user_id):
    users = User.select().where(User.refer == user_id)
    refer_users = []
    for user in users:
        refer_users.append(
            {
                'id': user.id,
                'user_id': user.user_id,
                'name': user.name,
                'role': user.role,
                'info': str_to_array(user.info),
                'status': user.status,
                'refre_id': user.refer
            }
        )
    return users


def get_all_groups():
    groups = []
    query = Group.select()
    for group in query:
        groups.append(
            {
                'name': group.name,
                'owner_id': group.owner_id,
                'info': str_to_array(group.info)
            }
        )
    return groups


def get_owner_group_users(user_id):
    group = []
    group_id = Group.get(
        Group.owner_id == user_id
    ).id
    query = GroupUsers.select().where(GroupUsers.group_id == group_id)
    for user in query:
        group.append(
            {
                'id': user.id,
                'group_id': user.group_id,
                'user_id': user.user_id
            }
        )
    return group


def create_group(user_id, group_name):
    usergroup = get_group_info_by_owner(user_id)
    if usergroup:
        Group.update(
            name=group_name
        ).where(Group.owner_id == user_id).execute()
    else:
        Group.create(
            name=group_name,
            owner_id=user_id
        )


def get_all_group_users_by_group_id(group_id):
    owner_id = get_group_info_by_id(group_id).get('owner_id')
    ownerinfo = get_user_info(owner_id)
    group_users = get_owner_group_users(owner_id)
    group_users.append(
        {
            'id': ownerinfo.get('id'),
            'group_id': group_id,
            'user_id': ownerinfo.get('user_id')
        }
    )
    return group_users


def user_on_group_chek(user_id):
    group_id = is_user_owner(user_id)
    if group_id:
        return group_id
    else:
        group_id = is_user_in_group(user_id)
        if group_id:
            return group_id
        else:
            return None
