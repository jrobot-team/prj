# -*- coding: utf-8 -*-
from datetime import datetime as _datetime
from dbclasses import Poll, PollQuestion, Userpoll
from bot_utils import Basedate, date_revers, to_base_date_cheker
from users_utils import is_user_owner, is_user_in_group, get_all_group_users_by_group_id


def create_poll(creator_id, pollname, polltext, chooses, date_end):
    to_base = []
    if '/' in chooses:
        pollchooses = chooses.split('/')
        for choose in pollchooses:
            if len(choose) == 0:
                pass
            else:
                if choose[0] == '':
                    choose = choose[:1]
                to_base.append(choose)
    else:
        to_base.append(chooses)
    group_id = is_user_owner(creator_id)
    if group_id:
        pass
    else:
        group_id = is_user_in_group(creator_id)
        if group_id:
            pass
        else:
            group_id = 0
    date_start = Basedate().date_hms()
    Poll.create(
        group_id=group_id,
        name=pollname,
        polltext=polltext,
        creator_id=creator_id,
        date_create=Basedate().date(),
        date_start=date_start,
        date_end=to_base_date_cheker(date_end),
        status=1
    )
    poll_id = Poll.get(Poll.date_start == date_start, Poll.creator_id == creator_id).id
    for choose in to_base:
        PollQuestion.create(
            poll_id=poll_id,
            name=choose
        )
    return poll_id


def get_poll_info(poll_id):
    choose_query = PollQuestion.select().where(PollQuestion.poll_id == poll_id)
    chooses = []
    for choose in choose_query:
        chooses.append(
            {
                'id': choose.id,
                'choose': choose.name
            }
        )
    try:
        pollinfo = {
            'id': Poll.get(Poll.id == poll_id).id,
            'group_id': Poll.get(Poll.id == poll_id).group_id,
            'name': Poll.get(Poll.id == poll_id).name,
            'polltext': Poll.get(Poll.id == poll_id).polltext,
            'creator_id': Poll.get(Poll.id == poll_id).creator_id,
            'date_create': date_revers(Poll.get(Poll.id == poll_id).date_create),
            'date_start': date_revers(Poll.get(Poll.id == poll_id).date_start),
            'date_end': date_revers(Poll.get(Poll.id == poll_id).date_end),
            'status': Poll.get(Poll.id == poll_id).status,
            'chooses': chooses
        }
    except:
        pollinfo = None
    return pollinfo


def update_poll_date_end(poll_id, date_end):
    datas = date_end.split(' ')
    dt = datas[0]
    tms = datas[1]
    year = int(dt.split('-')[0])
    month = int(dt.split('-')[1])
    day = int(dt.split('-')[2])
    hour = int(tms.split(':')[0])
    minutes = int(tms.split(':')[1])
    dtend = _datetime(
        year,
        month,
        day,
        hour,
        minutes
    )
    Poll.update(date_end=dtend).where(Poll.id == poll_id).execute()


def get_poll_users_by_poll_id(poll_id):
    group_id = get_poll_info(poll_id).get('group_id')
    pollusers = get_all_group_users_by_group_id(group_id)
    return pollusers


def get_polls_by_user_id(user_id, status='all'):
    polls = []
    group_id = is_user_owner(user_id)
    if group_id:
        pass
    else:
        group_id = is_user_in_group(user_id)
        if group_id:
            pass
        else:
            group_id = 0
    query = Poll.select().where(Poll.group_id == group_id)
    for poll in query:
        pollinfo = get_poll_info(poll.id)
        if status == 'all':
            polls.append(pollinfo)
        else:
            if status == 1:
                if pollinfo.get('status'):
                    polls.append(pollinfo)
            else:
                if pollinfo.get('status') == 0:
                    polls.append(pollinfo)
    return polls


def rec_user_choosed(user_id, poll_id, choose_id):
    Userpoll.create(
        user_id=user_id,
        poll_id=poll_id,
        question_id=choose_id
    )


def get_poll_all_chooses(poll_id):
    choose_query = Userpoll.select().where(Userpoll.poll_id == poll_id)
    chooses = []
    for choose in choose_query:
        chooses.append(
            {
                'id': choose.id,
                'user_id': choose.user_id,
                'poll_id': choose.poll_id,
                'choose_id': choose.question_id,
            }
        )
    return chooses


def is_user_polled(user_id, poll_id):
    try:
        user_choose = Userpoll.get(
            Userpoll.user_id == user_id,
            Userpoll.poll_id == poll_id).question_id
    except:
        user_choose = None
    return user_choose


def get_user_choose_var_name(user_id, poll_id):
    variants = get_poll_info(poll_id).get('chooses')
    var_id = is_user_polled(user_id, poll_id)
    varname = ''
    for var in variants:
        if var_id == var.get('id'):
            varname = var.get('choose')
    return varname


def count_choose(poll_id, choose_id):
    count = 0
    user_polled = get_poll_all_chooses(poll_id)
    for choose in user_polled:
        if choose.get('choose_id') == choose_id:
            count += 1
    return count


def poll_stata(poll_id):
    stats = []
    pollinfo = get_poll_info(poll_id)
    pollchooses = pollinfo.get('chooses')
    all_chooses_count = len(get_poll_all_chooses(poll_id))
    cubik = 10
    for choose in pollchooses:
        choosecheked_count = count_choose(poll_id, choose.get('id'))
        if choosecheked_count:
            percent = round(
                (choosecheked_count / all_chooses_count * 100),
                2
            )
        else:
            percent = 0.0
        if percent:
            visual = round((percent / 100 * cubik), 0)
            visual = '◼️' * int(visual)
        else:
            visual = ''
        stats.append(
            {
                'choose_id': choose.get('id'),
                'percent': percent,
                'visual': visual
            }
        )
    return stats


def poll_stata_formatter(poll_id):
    pollstata = poll_stata(poll_id)
    variants = get_poll_info(poll_id).get('chooses')
    text = ''
    for var in pollstata:
        var_id = var.get('choose_id')
        for pollvar in variants:
            if var_id == pollvar.get('id'):
                text += pollvar.get('choose') + '\n' + var.get('visual') + str(var.get('percent')) + '%\n'
    return text


def date_end_cheker(date_end):
    try:
        date_end = date_end.split(' ')
        date = date_end[0]
        time = date_end[1]
        day = date.split('-')[0]
        month = date.split('-')[1]
        year = date.split('-')[2].replace(' ', '')
        hour = time.split(':')[0]
        minutes = time.split(':')[1]
        to_base_date_time = _datetime(
            int(year),
            int(month),
            int(day),
            int(hour),
            int(minutes)
        )
    except:
        try:
            date = date_end.split('.')
            day = date[0]
            month = date[1]
            year = date[2]
            to_base_date_time = _datetime(
                int(year),
                int(month),
                int(day)
            )
        except:
            to_base_date_time = None
    return str(to_base_date_time)
