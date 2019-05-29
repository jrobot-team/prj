# -*- coding: utf-8 -*-
from datetime import datetime as _datetime
from bot_utils import Basedate, str_to_array, array_to_str, to_base_date_cheker
from dbclasses import Forum, ForumUsers, ForumPrepareUsers
from users_utils import is_user_in_group, is_user_owner, get_all_group_users_by_group_id, get_user_info


def chek_delta(delta):
    """
    Принимает часы минуты в формате 1:35 или 01:35
    """
    try:
        hours = int(delta.split(':')[0])
        minutes = int(delta.split(':')[1])
        date_end = Basedate().plus_hours(hours=hours, minutes=minutes)
        dt = str(date_end).split(' ')[0]
        hrs = str(date_end).split(' ')[1]
        year = dt.split('-')[2]
        month = dt.split('-')[1]
        day = dt.split('-')[0]
        hours = hrs.split(':')[0]
        minutes = hrs.split(':')[1]
        chek = _datetime(
            int(year),
            int(month),
            int(day),
            int(hours),
            int(minutes)
        )
    except:
        chek = None
    return chek


def chek_date(date):
    try:
        data = date.split('.')
        day = data[0]
        month = data[1]
        year = data[2]
        chek = _datetime(
            int(year),
            int(month),
            int(day)
        )
    except:
        chek = None
    return chek


def create_forum(forum_name, creator_id, forum_theme, delta, users='all'):
    """
    users = [user_id, user_id, ...] или all
    Статусы:
    - 0: завершен
    - 1: активен
    - 2: неопубликован
    """
    info = {
        'delta': delta,
        'comment': ''
    }
    date_end = chek_delta(delta)
    if date_end:
        pass
    else:
        date_end = Basedate().plus_hours(hours='01', minutes='00')
    group_id = is_user_owner(creator_id)
    if group_id:
        pass
    else:
        group_id = is_user_in_group(creator_id)
    date_create = Basedate().date()
    date_start = Basedate().date_hms()
    Forum.create(
        name=forum_name,
        creator_id=creator_id,
        group_id=group_id,
        date_create=date_create,
        date_start=date_start,
        date_end=to_base_date_cheker(date_end),
        forum_theme=forum_theme,
        status=2,
        info=array_to_str(info)
    )
    forum_id = Forum.get(Forum.date_start == date_start, Forum.creator_id == creator_id).id
    if users == 'all':
        group_users = get_all_group_users_by_group_id(group_id)
        for user in group_users:
            ForumUsers.create(
                forum_id=forum_id,
                user_id=user.get('user_id')
            )
    else:
        for user in users:
            ForumUsers.create(
                forum_id=forum_id,
                user_id=user
            )
    return forum_id


def update_forum_date_start(forum_id, date_start):
    datas = date_start.split(' ')
    dt = datas[0]
    tms = datas[1]
    year = int(dt.split('-')[0])
    month = int(dt.split('-')[1])
    day = int(dt.split('-')[2])
    hour = int(tms.split(':')[0])
    minutes = int(tms.split(':')[1])
    dstart = _datetime(
        year,
        month,
        day,
        hour,
        minutes
    )
    Forum.update(date_start=dstart).where(Forum.id == forum_id).execute()


def update_forum_delta(forum_id, delta):
    dt = delta.split(':')
    hours = dt[0]
    minutes = dt[1]
    finfo = get_forum_info(forum_id).get('info')
    info = {
        'delta': delta,
        'comment': finfo.get('comment')
    }
    date_start = get_forum_info(forum_id).get('date_start')
    date_end = Basedate().delta_time_start_to_end(date_start, hours=hours, minutes=minutes)
    Forum.update(date_end=date_end, info=array_to_str(info)).where(Forum.id == forum_id).execute()


def update_forum_comment(forum_id, comment):
    finfo = get_forum_info(forum_id).get('info')
    info = {
        'delta': finfo.get('delta'),
        'comment': comment
    }
    Forum.update(info=array_to_str(info)).where(Forum.id == forum_id).execute()


def update_forum_name(forum_id, forum_name):
    Forum.update(name=forum_name).where(Forum.id == forum_id).execute()


def update_forum_theme(forum_id, forum_theme):
    Forum.update(forum_theme=forum_theme).where(Forum.id == forum_id).execute()


def get_forum_info(forum_id):
    try:
        foruminfo = {
            'forum_id': Forum.get(Forum.id == forum_id).id,
            'forum_name': Forum.get(Forum.id == forum_id).name,
            'creator_id': Forum.get(Forum.id == forum_id).creator_id,
            'group_id': Forum.get(Forum.id == forum_id).group_id,
            'date_create': Forum.get(Forum.id == forum_id).date_create,
            'date_start': Forum.get(Forum.id == forum_id).date_start,
            'date_end': Forum.get(Forum.id == forum_id).date_end,
            'forum_theme': Forum.get(Forum.id == forum_id).forum_theme,
            'status': Forum.get(Forum.id == forum_id).status,
            'info': str_to_array(Forum.get(Forum.id == forum_id).info),
        }
    except:
        foruminfo = {}
    return foruminfo


def update_forum_status(forum_id, status=0):
    Forum.update(status=status).where(Forum.id == forum_id).execute()


def get_forums_by_group_id(group_id):
    query = Forum.select().where(Forum.group_id == group_id)
    forums = []
    for forum in query:
        foruminfo = get_forum_info(forum.id)
        forums.append(
            foruminfo
        )
    return forums


def get_forums_by_user_id(user_id):
    group_id = is_user_owner(user_id)
    if group_id:
        pass
    else:
        group_id = is_user_in_group(user_id)
    forums = get_forums_by_group_id(group_id)
    return forums


def get_forums_by_user_id_and_status(user_id, status=1):
    forums = get_forums_by_user_id(user_id)
    response = []
    for forum in forums:
        if forum.get('status') == status:
            response.append(
                forum
            )
    return response


def get_forum_users(forum_id):
    query = ForumUsers.select().where(ForumUsers.forum_id == forum_id)
    users = []
    for user in query:
        userinfo = get_user_info(user.user_id)
        users.append(
            userinfo
        )
    return users


def append_user_to_forum_prepare(creator_id, user_id):
    ForumPrepareUsers.create(
        creator_id=creator_id,
        user_id=user_id
    )


def remove_user_from_forum_prepare(creator_id, user_id):
    ForumPrepareUsers.delete().where(
        ForumPrepareUsers.creator_id == creator_id,
        ForumPrepareUsers.user_id == user_id).execute()


def append_user_to_forum(forum_id, user_id):
    ForumUsers.create(
        forum_id=forum_id,
        user_id=user_id
    )


def remove_user_from_forum(forum_id, user_id):
    ForumUsers.delete().where(
        ForumUsers.forum_id == forum_id,
        ForumUsers.user_id == user_id
    ).execute()


def user_on_forum(forum_id, user_id):
    try:
        uid = ForumUsers.get(
            ForumUsers.user_id == user_id,
            ForumUsers.forum_id == forum_id).user_id
    except:
        uid = None
    return uid
