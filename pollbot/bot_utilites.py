# -*- coding: utf-8 -*-
import json
import sqlite3
from datetime import datetime

import pytz

from config import statuses, timezone
from crpusrpwd import decrypt, encrypt
from lang import ru


class Basedate(object):
    def __init__(self, tzone=timezone):
        self.tz = tzone

    def date_hms(self):
        """ Возвращает год месяц день час минута секунда """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

    def date_mdh(self):
        """ Возвращает месяц день час минута секунда """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%m-%d %H:%M:%S')

    def date(self):
        """ Возвращает год месяц день """
        dt = datetime.now(pytz.timezone(self.tz))
        return datetime.strftime(dt, '%Y-%m-%d')


def array_to_str(array):
    string = json.dumps(array, ensure_ascii=False)
    return string


def str_to_array(string):
    array = json.loads(string)
    return array


def base_connect():
    """
    Точка входа подключение к базе
    """
    connection = sqlite3.connect('db/base.db')
    return connection


def replacer(text, rep=None):
    """ Ломаем HTML теги в тексте
    функция принимает текст и список типа [['<', '|']] """
    if rep is None:
        rep = [
            ['<', '⬅️'],
            ['>', '➡️'],
            ['/', '|'],
            ["'", "`"],
            ['"', '`'],
            ['\\', '|']]
    for i, r in rep:
        text = text.replace(i, r)
    return text


def temp_del(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        tmp_del_sql = 'DELETE FROM tmp WHERE user_id = ?'
        cursor.execute(tmp_del_sql, ([user_id]))
        connection.commit()
    connection.close()


def tmp_pollid(user_id, pollid):
    temp_del(user_id)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_tmp_poll_name_sql = 'INSERT INTO tmp (user_id, pollid) VALUES (?, ?)'
        cursor.execute(make_tmp_poll_name_sql, ([user_id, pollid]))
        connection.commit()
    connection.close()


def tmp_user_choised(user_id, pollid, choiseid):
    temp_del(user_id)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_tmp_poll_name_sql = 'INSERT INTO tmp (user_id, pollid, choiseid) VALUES (?, ?, ?)'
        cursor.execute(make_tmp_poll_name_sql, ([user_id, pollid, choiseid]))
        connection.commit()
    connection.close()


def get_tmp_pollid(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_pollid_sql = 'SELECT pollid FROM tmp WHERE user_id = ?'
        cursor.execute(get_pollid_sql, ([user_id]))
        pollid = cursor.fetchone()
    connection.close()
    temp_del(user_id)
    if pollid:
        return pollid[0]
    else:
        return False


def get_tmp_pollid_choiseid(user_id):
    """
    0-pollid, 1-choiseid
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_pollid_sql = 'SELECT pollid, choiseid FROM tmp WHERE user_id = ?'
        cursor.execute(get_pollid_sql, ([user_id]))
        pollid = cursor.fetchone()
    connection.close()
    temp_del(user_id)
    if pollid:
        return pollid
    else:
        return (0, 0)


def lastpollid():
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getid_sql = 'SELECT pollid FROM polls ORDER BY rowid DESC LIMIT 1'
        cursor.execute(getid_sql)
        pollid = cursor.fetchone()
        if pollid:
            return pollid[0]
        else:
            return 0


def make_temp_choiseid(user_id, pollid, choiseid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_tmp_sql = 'INSERT INTO tmp (user_id, pollid, choiseid) VALUES (?, ?, ?)'
        cursor.execute(make_tmp_sql, ([user_id, pollid, choiseid]))
        connection.commit()
    connection.close()


def get_tmp_choiseid(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_sql = 'SELECT pollid, choiseid FROM tmp WHERE user_id = ?'
        cursor.execute(get_sql, ([user_id]))
        getids = cursor.fetchone()
    connection.close()
    temp_del(user_id)
    if getids:
        return getids
    else:
        return False


def make_tmp_uid(user_id, uid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_tmp_sql = 'INSERT INTO tmp (user_id, uid) VALUES (?, ?)'
        cursor.execute(make_tmp_sql, ([user_id, uid]))
        connection.commit()
    connection.close()


def make_tmp_change_fio(user_id, uid):
    make_tmp_uid(user_id, uid)


def make_tmp_replay_to(user_id, uid):
    make_tmp_uid(user_id, uid)


def get_tmp_uid(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_sql = 'SELECT uid FROM tmp WHERE user_id = ?'
        cursor.execute(get_sql, ([user_id]))
        getuid = cursor.fetchone()
    connection.close()
    temp_del(user_id)
    if getuid:
        return getuid[0]
    else:
        return 0


def tmp_groupid(user_id, groupid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_tmp_sql = 'INSERT INTO tmp (user_id, groupid) VALUES (?, ?)'
        cursor.execute(make_tmp_sql, ([user_id, groupid]))
        connection.commit()
    connection.close()


def get_tmp_groupid(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_sql = 'SELECT groupid FROM tmp WHERE user_id = ?'
        cursor.execute(get_sql, ([user_id]))
        getuid = cursor.fetchone()
    connection.close()
    temp_del(user_id)
    if getuid:
        return getuid[0]
    else:
        return 0


def edit_choise(pollid, choiseid, choise):
    pollchoises = get_poll_info(pollid)[2]
    tobase = []
    count = 0
    for row in pollchoises:
        count += 1
        if row.get('num') == choiseid:
            old_choise = row.get('var')
            tobase.append({'num': count, 'var': choise})
        else:
            tobase.append({'num': count, 'var': row.get('var')})
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_choise_sql = 'UPDATE polls SET choises = ? WHERE pollid = ?'
        cursor.execute(add_choise_sql, ([
            array_to_str(tobase),
            pollid]))
        connection.commit()
    connection.close()
    return old_choise


def make_poll_name_fn(poll_name):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_poll_name_sql = 'INSERT INTO polls (pollname,  date) VALUES (?, ?)'
        cursor.execute(make_poll_name_sql, ([
            poll_name,
            date]))
        connection.commit()
        get_pollid_sql = 'SELECT pollid FROM polls WHERE date = ?'
        cursor.execute(get_pollid_sql, ([date]))
        pollid = cursor.fetchone()
    connection.close()
    if pollid:
        pollid = pollid[0]
    else:
        pollid = 0
    return pollid


def edit_pollname(pollid, name):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        edit_pollname_sql = 'UPDATE polls SET pollname = ? WHERE pollid = ?'
        cursor.execute(edit_pollname_sql, ([name, pollid]))
        connection.commit()
    connection.close()


def make_poll_text_fn(pollid, polltext):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_polltext_sql = 'UPDATE polls SET polltext = ? WHERE pollid = ?'
        cursor.execute(make_polltext_sql, ([polltext, pollid]))
        connection.commit()
    connection.close()


def find_double_choises(tobase):
    d = []
    res = []
    count = 0
    for row in tobase:
        var = row.get('var')
        while True:
            if var[-1:] == ' ':
                var = var[:-1]
            else:
                break
        d.append(var)
    for row in set(d):
        count += 1
        res.append({'num': count, 'var': row})
    return res


def add_poll_choise_fn(pollid, pollchoises):
    tobase = get_poll_info(pollid)[2]
    count = len(tobase)
    if '/' in pollchoises:
        pollchoises = pollchoises.split('/')
        for choise in pollchoises:
            if len(choise) == 0:
                pass
            else:
                if choise[0] == '':
                    choise = choise[:1]
                count += 1
                choise = {'num': count, 'var': choise}
                tobase.append(choise)
    else:
        tobase.append({'num': count + 1, 'var': pollchoises})
    tobase = find_double_choises(tobase)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_choise_sql = 'UPDATE polls SET choises = ? WHERE pollid = ?'
        cursor.execute(add_choise_sql, ([
            array_to_str(tobase),
            pollid]))
        connection.commit()
    connection.close()


def user_counts():
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_last_user_sql = 'SELECT rowid FROM users ORDER BY rowid DESC LIMIT 1'
        cursor.execute(get_last_user_sql)
        last_user = cursor.fetchone()
    connection.close()
    if last_user:
        return last_user[0]
    else:
        return 0


def reg_user(user_id, username):
    """
    Регистрация пользователя
    """
    date_reg = Basedate().date()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        reg_user_sql = 'INSERT INTO users (uid, username, date_reg) VALUES (?, ?, ?)'
        cursor.execute(reg_user_sql, ([user_id, username, date_reg]))
        connection.commit()
    connection.close()


def user_info(user_id):
    """
    0-username, 1-fio, 2-role, 3-pollcount, 4-registered, 5-interviewed, 6-pwd, 7-groupid, 8-firststep, 9-date_reg
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_user_sql = 'SELECT username, fio, role, pollcount, registered, interviewed, pwd, groupid, firststep, date_reg FROM users WHERE uid = ?'
        cursor.execute(get_user_sql, ([user_id]))
        userinfo = cursor.fetchone()
    connection.close()
    if userinfo:
        return userinfo
    else:
        return 0


def get_poll_info(pollid):
    """
    0-pollname, 1-polltext, 2-choises, 3-open, 4-posted, 5-date, 6-doc, 7-doc_name
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_poll_info_sql = 'SELECT pollname, polltext, choises, open, posted, date, doc, doc_name FROM polls WHERE pollid = ?'
        cursor.execute(get_poll_info_sql, ([pollid]))
        poll_info = cursor.fetchone()
    connection.close()
    if poll_info:
        pollname = poll_info[0]
        polltext = poll_info[1]
        choises = str_to_array(poll_info[2])
        pollopen = poll_info[3]
        posted = poll_info[4]
        date = poll_info[5]
        doc = poll_info[6]
        doc_name = poll_info[7]
        poll_info = (pollname, polltext, choises, pollopen, posted, date, doc, doc_name)
        return poll_info
    else:
        return False


def get_polls(status):
    """
    Возвращает множественный список с информацией по опросам
    в качестве аргумента принимает 0 (закрытые) или 1 (открытые)
    0-pollid, 1-pollname, 2-polltext, 3-choises, 4-posted, 5-date
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_polls_sql = 'SELECT pollid, pollname, polltext, choises, posted, date FROM polls WHERE open = ?'
        cursor.execute(get_polls_sql, ([status]))
        polls = cursor.fetchall()
    connection.close()
    return polls


def get_draft_polls():
    """
    0-pollid, 1-pollname, 2-polltext, 3-choises, 4-posted, 5-date
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_draft_polls_sql = 'SELECT pollid, pollname, polltext, choises, posted, date \
            FROM polls WHERE draft = 1 ORDER BY pollid DESC'
        cursor.execute(get_draft_polls_sql)
        polls = cursor.fetchall()
    connection.close()
    return polls


def get_open_polls():
    """
    Информация по открытым опросам
    0-pollid, 1-pollname, 2-polltext, 3-choises, 4-posted, 5-date
    """
    return get_polls(1)


def get_closed_polls():
    """
    Информация по закрытым опросам
    0-pollid, 1-pollname, 2-polltext, 3-choises, 4-posted, 5-date
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_polls_sql = 'SELECT pollid, pollname, polltext, choises, posted, date FROM polls WHERE open = 0 AND draft = 0'
        cursor.execute(get_polls_sql)
        polls = cursor.fetchall()
    connection.close()
    return polls


def get_arch_polls():
    """
    0-pollid, 1-pollname, 2-polltext, 3-choises, 4-posted, 5-date
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_arch_polls_sql = 'SELECT pollid, pollname, polltext, choises, posted, date \
            FROM polls WHERE arch = 1 ORDER BY pollid DESC'
        cursor.execute(get_arch_polls_sql)
        polls = cursor.fetchall()
    connection.close()
    return polls


def copy_poll(pollid):
    date = Basedate().date_hms()
    pollinfo = get_poll_info(pollid)
    pollname = ru.get('copy_name') + pollinfo[0]
    polltext = pollinfo[1]
    choises = pollinfo[2]
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_poll_sql = 'INSERT INTO polls (pollname, polltext, choises, date) VALUES (?, ?, ?, ?)'
        cursor.execute(make_poll_sql, ([
            pollname,
            polltext,
            array_to_str(choises),
            date]))
        connection.commit()
        get_pollid_sql = 'SELECT pollid FROM polls WHERE date = ?'
        cursor.execute(get_pollid_sql, ([date]))
        pollid = cursor.fetchone()
    connection.close()
    if pollid:
        return pollid[0]
    else:
        return 0


def open_poll(pollid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        open_poll_sql = 'UPDATE polls SET open = 1 WHERE pollid = ?'
        cursor.execute(open_poll_sql, ([pollid]))
        connection.commit()
    connection.close()


def close_poll(pollid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        close_poll_sql = 'UPDATE polls SET open = 0, arch = 1 WHERE pollid = ?'
        cursor.execute(close_poll_sql, ([pollid]))
        connection.commit()
    connection.close()


def do_public_poll(pollid):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        public_poll_sql = 'UPDATE polls SET open = 1, posted = 1, draft = 0, date = ? WHERE pollid = ?'
        cursor.execute(public_poll_sql, ([
            date,
            pollid]))
        connection.commit()
    connection.close()


def del_poll_choise(pollid, poll_choiseid):
    pollchoises = get_poll_info(pollid)[2]
    tobase = []
    for choise in pollchoises:
        if choise.get('num') != int(poll_choiseid):
            tobase.append(choise)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_choise_sql = 'UPDATE polls SET choises = ? WHERE pollid = ?'
        cursor.execute(add_choise_sql, ([
            array_to_str(tobase),
            pollid]))
        connection.commit()
    connection.close()


def delpoll_fn(pollid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        del_sql = 'DELETE FROM polls WHERE pollid = ?'
        cursor.execute(del_sql, ([pollid]))
        connection.commit()
    connection.close()


def get_poll_users():
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        users_sql = 'SELECT uid FROM users WHERE registered = 1'
        cursor.execute(users_sql)
        users = cursor.fetchall()
    connection.close()
    if len(users) == 0:
        users = []
        return users
    else:
        uids = []
        for user in users:
            if chk_admin(user[0]):
                pass
            else:
                uids.append(user[0])
        return uids


def get_poll_stats(pollid, choise):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_poll_stats_sql = 'SELECT user_id FROM stats WHERE pollid = ? AND choise = ?'
        cursor.execute(get_poll_stats_sql, ([
            pollid,
            choise]))
        choise_count = cursor.fetchall()
    connection.close()
    if choise_count:
        return len(choise_count)
    else:
        return 0


def get_poll_user_stat(pollid):
    """
    0-user_id, 1-choise(int)
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_poll_stats_sql = 'SELECT user_id, choise FROM stats WHERE pollid = ?'
        cursor.execute(get_poll_stats_sql, ([
            pollid]))
        stata = cursor.fetchall()
    connection.close()
    if stata:
        return stata
    else:
        return []


def chek_user_polled(user_id, pollid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_user_in_poll_sql = 'SELECT user_id FROM stats WHERE pollid = ? AND user_id = ?'
        cursor.execute(get_user_in_poll_sql, ([pollid, user_id]))
        user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False


def pollstat_sorter(pollid):
    """
    0-stata dict(var, num, count, percent), 1-public_date, 2-poll_all_answers, 3-message
    """
    message = ''
    cubik = 10
    poll_all_answers = 0
    stata = []
    pollchoises = get_poll_info(pollid)[2]
    public_date = get_poll_info(pollid)[5]
    for choise in pollchoises:
        num = choise.get('num')
        count = get_poll_stats(pollid, num)
        poll_all_answers = count + poll_all_answers
    for choise in pollchoises:
        num = choise.get('num')
        var = choise.get('var')
        count = get_poll_stats(pollid, num)
        if count:
            percent = round((count / poll_all_answers * 100), 2)
        else:
            percent = 0
        stata.append({
            'var': var,
            'num': num,
            'count': count,
            'percent': percent})
    for choise in stata:
        var = choise.get('var')
        prc = choise.get('percent')
        pcount = choise.get('count')
        if prc:
            visual = round((prc / 100 * cubik), 0)
            visual = '◻️' * int(visual)
        else:
            visual = ''
        message = message + ru.get('pollstat_text').format(
            var=var,
            visual=visual,
            prc=prc,
            pcount=pcount)
    poll = (stata, public_date, poll_all_answers, message)
    return poll


def get_poll_user_choise(pollid):
    message = ''
    poll_user_stat = get_poll_user_stat(pollid)
    choises = pollstat_sorter(pollid)[0]
    for user in poll_user_stat:
        user_id = user[0]
        var = ''
        for choise in choises:
            if choise.get('num') == user[1]:
                var = choise.get('var')
        userinfo = user_info(user_id)
        if userinfo:
            if len(userinfo[1]) == 0:
                username = userinfo[0]
            else:
                username = userinfo[1]
        else:
            username = ru.get('super_admin')
        message = message + ru.get('polldetailtxt').format(
            uid=user_id,
            user=username,
            choise=var)
    if len(message) == 0:
        return ru.get('nopollers_users')
    else:
        return message


def plus_user_polled(user_id):
    pollcount = user_info(user_id)[3] + 1
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        pollcount_sql = 'UPDATE users SET pollcount = ? WHERE uid = ?'
        cursor.execute(pollcount_sql, ([pollcount, user_id]))
        connection.commit()
    connection.close()


def user_select_choise(user_id, pollid, choise):
    connection = base_connect()
    with connection:
        userinfo = user_info(user_id)
        cursor = connection.cursor()
        user_select_choise_sql = 'INSERT INTO stats (pollid, user_id, choise) VALUES (?, ?, ?)'
        if userinfo:
            groupid = userinfo[7]
            admin = get_group_info(groupid)
            if admin:
                admin = admin[1]
                users = get_group_users(groupid)
                for user in users:
                    uid = user[7]
                    if uid != user_id:
                        plus_user_polled(uid)
                        cursor.execute(user_select_choise_sql, ([
                            pollid,
                            uid,
                            choise]))
        cursor.execute(user_select_choise_sql, ([
            pollid,
            user_id,
            choise]))
        if userinfo:
            pollcount = userinfo[3] + 1
            pollcount_sql = 'UPDATE users SET pollcount = ? WHERE uid = ?'
            cursor.execute(pollcount_sql, ([pollcount, user_id]))
        connection.commit()
    connection.close()


def make_password(user_id, pwd):
    pwd = encrypt(pwd)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        user_pwd_sql = 'UPDATE users SET pwd = ?, firststep = 1 WHERE uid = ?'
        cursor.execute(user_pwd_sql, ([
            pwd,
            user_id]))
        connection.commit()
    connection.close()


def chek_user_password(user_id, pwd):
    chek = False
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_user_pwd_sql = 'SELECT pwd FROM users WHERE uid = ?'
        cursor.execute(get_user_pwd_sql, ([user_id]))
        user_pwd = cursor.fetchone()
    connection.close()
    if user_pwd:
        user_pwd = decrypt(user_pwd[0])
        if user_pwd == pwd:
            chek = True
        else:
            chek = False
    else:
        chek = False
    return chek


def get_users(reg=1):
    """
    0-uid, 1-username, 2-fio, 3-role, 4-pollcount, 5-registered, 6-interviewed
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_users_sql = 'SELECT uid, username, fio, role, pollcount, registered, interviewed FROM users WHERE registered = ? ORDER BY fio'
        cursor.execute(get_users_sql, ([reg]))
        users = cursor.fetchall()
    connection.close()
    if len(users) > 0:
        return users
    else:
        return False


def change_activation(user_id, activ=1):
    if activ == 0:
        groupid = user_info(user_id)[7]
        if groupid:
            groupadminid = get_group_info(groupid)[1]
            if groupadminid == user_id:
                del_group(groupid)
        remove_user_from_group(user_id)
        change_user_status(user_id, statuses[1])
    else:
        change_user_status(user_id, statuses[0])
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        candidate_to_user_sql = 'UPDATE users SET registered = ?, interviewed = ? WHERE uid = ?'
        cursor.execute(candidate_to_user_sql, ([
            activ,
            activ,
            user_id]))
        connection.commit()
    connection.close()


def reset_password(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        reset_pwd_sql = 'UPDATE users SET pwd = ? WHERE uid = ?'
        cursor.execute(reset_pwd_sql, ([
            '',
            user_id]))
        connection.commit()
    connection.close()


def make_fio(uid, fio):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        reset_pwd_sql = 'UPDATE users SET fio = ? WHERE uid = ?'
        cursor.execute(reset_pwd_sql, ([
            fio,
            uid]))
        connection.commit()
    connection.close()


def change_user_status(uid, role):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        if role != statuses[1]:
            change_st_sql = 'UPDATE users SET role = ?, interviewed = 1 WHERE uid = ?'
            cursor.execute(change_st_sql, ([
                role,
                uid]))
        else:
            change_to_nopoller_sql = 'UPDATE users SET role = ?, interviewed = 0 WHERE uid = ?'
            cursor.execute(change_to_nopoller_sql, ([
                role,
                uid]))
        connection.commit()
    connection.close()
    return role


def remove_user_from_group(uid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        change_st_sql = 'UPDATE users SET groupid = 0, role = ?, interviewed = 1 WHERE uid = ?'
        cursor.execute(change_st_sql, ([
            statuses[0],
            uid]))
        connection.commit()
    connection.close()


def get_groups(admin=1):
    """
    admin=0 без Модератора
    admin=1 с Модератором
    admin=2 все
    0-groupid, 1-adminid, 2-name
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        if admin == 2:
            get_groups_sql = 'SELECT groupid, adminid, name FROM groups'
            cursor.execute(get_groups_sql)
        else:
            get_groups_sql = 'SELECT groupid, adminid, name FROM groups WHERE adminid = ?'
            cursor.execute(get_groups_sql, ([admin]))
        groups = cursor.fetchall()
    connection.close()
    return groups


def add_group_and_set_admin_fn(groupname, uid):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_group_sql = 'INSERT INTO groups (adminid, name, date_added) VALUES (?, ?, ?)'
        cursor.execute(add_group_sql, ([
            uid,
            groupname,
            date]))
        connection.commit()
        get_groupid_sql = 'SELECT groupid FROM groups WHERE date_added = ?'
        cursor.execute(get_groupid_sql, ([date]))
        groupid = cursor.fetchone()
    connection.close()
    return groupid[0]


def add_group_fn(groupname):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_group_sql = 'INSERT INTO groups (name, date_added) VALUES (?, ?)'
        cursor.execute(add_group_sql, ([
            groupname,
            date]))
        connection.commit()
        get_groupid_sql = 'SELECT groupid FROM groups WHERE date_added = ?'
        cursor.execute(get_groupid_sql, ([date]))
        groupid = cursor.fetchone()
    connection.close()
    return groupid[0]


def change_group_admin(uid, groupid):
    old_adminid = get_group_info(groupid)[1]
    if old_adminid:
        remove_user_from_group(old_adminid)
        change_user_status(old_adminid, statuses[0])
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_to_group_sql = 'UPDATE groups SET adminid = ? WHERE groupid = ?'
        cursor.execute(add_to_group_sql, ([
            uid,
            groupid]))
        connection.commit()
    connection.close()


def add_to_group(groupid, uid):
    """
    Добавляет в группу и если это не админ то меняет статус пользователя на без права голоса
    """
    role = user_info(uid)[2]
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        add_to_group_sql = 'UPDATE users SET groupid = ? WHERE uid = ?'
        cursor.execute(add_to_group_sql, ([
            groupid,
            uid]))
        if role != statuses[2]:
            change_to_nopoller_sql = 'UPDATE users SET role = ?, interviewed = 0 WHERE uid = ?'
            cursor.execute(change_to_nopoller_sql, ([
                statuses[1],
                uid]))
        connection.commit()
    connection.close()


def get_group_info(groupid):
    """
    0-groupid, 1-adminid, 2-name
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_groups_sql = 'SELECT groupid, adminid, name FROM groups WHERE groupid = ?'
        cursor.execute(get_groups_sql, ([groupid]))
        groupinfo = cursor.fetchone()
    connection.close()
    return groupinfo


def get_groupid_from_admin(uid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_admin_sql = 'SELECT groupid FROM groups WHERE adminid = ?'
        cursor.execute(get_admin_sql, ([uid]))
        groupinfo = cursor.fetchone()
    connection.close()
    if groupinfo:
        return groupinfo[0]
    else:
        return 0


def get_group_users(groupid):
    """
    0-username, 1-fio, 2-role, 3-pollcount, 4-registered, 5-interviewed, 6-pwd, 7-uid
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_group_users_sql = 'SELECT username, fio, role, pollcount, registered, interviewed, pwd, uid FROM users WHERE groupid = ? AND registered = 1'
        cursor.execute(get_group_users_sql, ([groupid]))
        groupusers = cursor.fetchall()
    connection.close()
    return groupusers


def get_noadmin_users():
    """
    0-username, 1-fio, 2-role, 3-pollcount, 4-registered, 5-interviewed, 6-pwd, 7-uid
    """
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_noadmin_users_sql = 'SELECT \
            username, fio, role, pollcount, registered, \
            interviewed, pwd, uid FROM users \
            WHERE groupid = 0 AND registered = 1'
        cursor.execute(get_noadmin_users_sql)
        noadminusers = cursor.fetchall()
    connection.close()
    return noadminusers


def del_group(groupid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        del_sql = 'DELETE FROM groups WHERE groupid = ?'
        cursor.execute(del_sql, ([groupid]))
        change_role_sql = 'UPDATE users SET role = ?, groupid = 0 WHERE groupid = ?'
        cursor.execute(change_role_sql, ([
            statuses[0],
            groupid]))
        connection.commit()
    connection.close()


def rename_group(groupid, groupname):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        rename_group_sql = 'UPDATE groups SET name = ? WHERE groupid = ?'
        cursor.execute(rename_group_sql, ([
            groupname,
            groupid]))
        connection.commit()
    connection.close()


def chk_admin(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        select_admin_sql = 'SELECT user_id FROM admins WHERE user_id = ?'
        cursor.execute(select_admin_sql, ([user_id]))
        admin_id = cursor.fetchone()
    connection.close()
    if admin_id:
        return True
    else:
        return False


def make_admin(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        make_admin_sql = 'INSERT INTO admins (user_id) VALUES (?)'
        cursor.execute(make_admin_sql, ([user_id]))
        connection.commit()
    connection.close()


def remove_admin(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        remove_admin_sql = 'DELETE FROM admins WHERE user_id = ?'
        cursor.execute(remove_admin_sql, ([user_id]))
        connection.commit()
    connection.close()


def getadmins_ids():
    adminsids = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_admins_sql = 'SELECT user_id FROM admins'
        cursor.execute(get_admins_sql)
        admins_id = cursor.fetchall()
    connection.close()
    if len(admins_id) > 0:
        for aid in admins_id:
            adminsids.append(aid[0])
    return adminsids


def get_chats(status='new'):
    chats_dict = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_chats = """
        SELECT chatid, chat_name, chat_url, date_create,
        date_start, status, catid FROM chats WHERE status = ? ORDER BY chatid DESC
        """
        cursor.execute(get_chats, ([status]))
        chats = cursor.fetchall()
    connection.close()
    if len(chats) > 0:
        for chat in chats:
            chats_dict.append(
                {
                    'chatid': chat[0],
                    'chat_name': chat[1],
                    'chat_url': chat[2],
                    'date_create': chat[3],
                    'date_start': chat[4],
                    'status': chat[5],
                    'catid': chat[6]
                }
            )
    return chats_dict


def new_chat_name_fn(chat_name):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'INSERT INTO chats (chat_name, date_create) VALUES (?, ?)'
        cursor.execute(sql, ([chat_name, date]))
        connection.commit()
        get_id_sql = 'SELECT chatid FROM chats WHERE date_create = ?'
        cursor.execute(get_id_sql, ([date]))
        chat_id = cursor.fetchone()
        chat_id = chat_id[0]
    connection.close()
    return chat_id


def make_chat_url(chatid, chat_url):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'UPDATE chats SET chat_url = ? WHERE chatid = ?'
        cursor.execute(sql, ([chat_url, chatid]))
        connection.commit()
    connection.close()


def get_chat_info(chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_chats = 'SELECT chatid, chat_name, chat_url, date_create, date_start, status, catid FROM chats WHERE chatid = ?'
        cursor.execute(get_chats, ([chatid]))
        chat = cursor.fetchone()
    connection.close()
    if chat:
        ch = {
            'chatid': chat[0],
            'chat_name': chat[1],
            'chat_url': chat[2],
            'date_create': chat[3],
            'date_start': chat[4],
            'status': chat[5],
            'catid': chat[6]
        }
    return ch


def get_chat_counts(chatid, user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_count = 'SELECT message FROM chat_record WHERE chatid = ? AND user_id != ?'
        cursor.execute(get_count, ([chatid, user_id]))
        count = cursor.fetchall()
    connection.close()
    if count:
        ln = len(count)
    else:
        ln = 0
    return ln


def date_start_updater(date_start, chatid):
    try:
        date_time = date_start.split(' ')
        date = date_time[0].split('.')
        time = date_time[1]
        day = date[0]
        month = date[1]
        year = date[2].replace(' ', '')
        hour = time.split(':')[0]
        minutes = time.split(':')[1]
        to_base_date_time = '{year}-{month}-{day} {hour}:{minutes}:00'.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minutes=minutes
        )
        connection = base_connect()
        with connection:
            cursor = connection.cursor()
            sql = 'UPDATE chats SET date_start = ?, status = ? WHERE chatid = ?'
            cursor.execute(sql, ([to_base_date_time, 'wait', chatid]))
            connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        to_base_date_time = None
    return to_base_date_time


def delete_open_chat(chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        del_sql = 'DELETE FROM open_chat WHERE chatid = ?'
        cursor.execute(del_sql, ([chatid]))
        connection.commit()
    connection.close()


def get_chat_appended_to_user(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        get_open_sql = 'SELECT chatid FROM on_chat WHERE user_id = ?'
        cursor.execute(get_open_sql, ([user_id]))
        chatid = cursor.fetchone()
    connection.close()
    if chatid:
        chatid = chatid[0]
    return chatid


def open_chat(chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        open_chat_sql = 'INSERT INTO open_chat (chatid) VALUES (?)'
        cursor.execute(open_chat_sql, ([chatid]))
        connection.commit()
    connection.close()


def upd_chat_status(chatid, status):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        upd_sql = 'UPDATE chats SET status = ? WHERE chatid = ?'
        cursor.execute(upd_sql, ([
            status,
            chatid
        ]))
        connection.commit()
    connection.close()


def record_chat_story(user_id, chatid, msg, mtype):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        if mtype == 'doc' or mtype == 'photo':
            msg = {
                'fileid': msg,
                'type': mtype
            }
            msg = array_to_str([msg])
        sql = 'INSERT INTO chat_record (user_id, chatid, message) VALUES  (?, ?, ?)'
        cursor.execute(sql, ([
            user_id,
            chatid,
            msg]))
        connection.commit()
    connection.close()


def chek_on_chat_user(user_id, chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'SELECT user_id FROM on_chat WHERE user_id = ? AND chatid != ?'
        cursor.execute(sql, (
            [
                user_id,
                chatid
            ]
        ))
        user_id = cursor.fetchone()
    connection.close()
    if user_id:
        user_id = user_id[0]
    return user_id


def make_on_chat_user(user_id, chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        if chek_on_chat_user(user_id, chatid):
            dsql = 'DELETE FROM on_chat WHERE user_id = ?'
            cursor.execute(dsql, ([user_id]))
            sql = 'INSERT INTO on_chat (user_id, chatid) VALUES  (?, ?)'
            cursor.execute(sql, ([
                user_id,
                chatid]))
            connection.commit()
        else:
            sql = 'INSERT INTO on_chat (user_id, chatid) VALUES  (?, ?)'
            cursor.execute(sql, ([
                user_id,
                chatid]))
            connection.commit()
    connection.close()


def user_on_chat(user_id, chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'SELECT user_id FROM on_chat WHERE user_id = ? AND chatid = ?'
        cursor.execute(sql, (
            [
                user_id,
                chatid
            ]
        ))
        user_id = cursor.fetchone()
    connection.close()
    if user_id:
        user_id = user_id[0]
    return user_id


def get_on_chat_users(chatid):
    usr = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'SELECT user_id FROM on_chat WHERE chatid = ?'
        cursor.execute(sql, ([chatid]))
        users = cursor.fetchall()
    connection.close()
    if len(users) > 0:
        for uid in users:
            usr.append(
                {
                    'user_id': uid[0]
                }
            )
    return usr


def delete_user(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        del_sql = 'DELETE FROM users WHERE uid = ?'
        cursor.execute(del_sql, ([user_id]))
        connection.commit()
    connection.close()


def get_chat_arch_messages(chatid):
    msgs = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'SELECT user_id, message FROM chat_record WHERE chatid = ?'
        cursor.execute(sql, ([chatid]))
        msgs_base = cursor.fetchall()
    connection.close()
    if len(msgs_base) > 0:
        for msg in msgs_base:
            try:
                fileid = str_to_array(msg[1])
            except:
                fileid = None
            if fileid:
                msgs.append(
                    {
                        'user_id': msg[0],
                        'message': fileid[0].get('fileid'),
                        'type': fileid[0].get('type')
                    }
                )
            else:
                msgs.append(
                    {
                        'user_id': msg[0],
                        'message': msg[1],
                        'type': 'text'
                    }
                )
    return msgs


def upd_poll_doc(pollid, doc, doc_name):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'UPDATE polls SET doc = ?, doc_name = ? WHERE pollid = ?'
        cursor.execute(
            sql,
            ([
                doc,
                doc_name,
                pollid
            ])
        )
        connection.commit()
    connection.close()


def get_chat_user_count(user_id, chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        chk_user_sql = 'SELECT count FROM chat_count WHERE user_id = ? AND chatid = ?'
        cursor.execute(chk_user_sql, ([
            user_id,
            chatid
        ]))
        count = cursor.fetchone()
        if count:
            count = count[0]
        else:
            count = 0
            sql_ins = 'INSERT INTO chat_count (user_id, chatid, count) VALUES (?, ?, ?)'
            cursor.execute(sql_ins, ([
                user_id,
                chatid,
                count
            ]))
            connection.commit()
    connection.close()
    return count


def upd_chat_count(user_id, chatid, count):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        sql = 'UPDATE chat_count SET count = ? WHERE user_id = ? AND chatid = ?'
        cursor.execute(
            sql,
            ([
                count,
                user_id,
                chatid
            ])
        )
        connection.commit()
    connection.close()


def unset_chats(user_id):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        dsql = 'DELETE FROM on_chat WHERE user_id = ?'
        cursor.execute(dsql, ([user_id]))
        connection.commit()
    connection.close()


def get_chat_cats():
    category = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getsql = 'SELECT catid, catname FROM chat_cat'
        cursor.execute(getsql)
        cats = cursor.fetchall()
    connection.close()
    if len(cats) > 0:
        for cat in cats:
            category.append(
                {
                    'id': cat[0],
                    'catname': cat[1]
                }
            )
    return category


def add_cat(catname):
    date = Basedate().date_hms()
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        addsql = 'INSERT INTO chat_cat (catname, date) VALUES (?, ?)'
        cursor.execute(addsql, ([catname, date]))
        connection.commit()
        getidsql = 'SELECT catid FROM chat_cat WHERE date = ?'
        cursor.execute(getidsql, ([date]))
        catid = cursor.fetchone()
        if catid:
            catid = catid[0]
        else:
            catid = 0
    connection.close()
    return catid


def append_chat_to_cat(catid, chatid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        appendsql = 'UPDATE chats SET catid = ? WHERE chatid = ?'
        cursor.execute(appendsql, ([catid, chatid]))
        connection.commit()
    connection.close()


def get_chats_in_cat(catid, status=False):
    chats = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        if status:
            getsql = 'SELECT chatid, chat_name, status FROM chats WHERE catid = ? AND status = ?'
            cursor.execute(getsql, ([catid, status]))
        else:
            getsql = 'SELECT chatid, chat_name, status FROM chats WHERE catid = ?'
            cursor.execute(getsql, ([catid]))
        chats_db = cursor.fetchall()
    connection.close()
    if len(chats_db) > 0:
        for chat in chats_db:
            chats.append(
                {
                    'id': chat[0],
                    'chatname': chat[1],
                    'status': chat[2]
                }
            )
    return chats


def get_active_chats_in_cat(catid):
    chats = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getsql = 'SELECT chatid, chat_name FROM chats WHERE catid = ? AND status = ?'
        cursor.execute(getsql, ([catid, 'active']))
        chats_db = cursor.fetchall()
    connection.close()
    if len(chats_db) > 0:
        for chat in chats_db:
            chats.append(
                {
                    'id': chat[0],
                    'chatname': chat[1]
                }
            )
    return chats


def cat_info(catid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getinfosql = 'SELECT catid, catname FROM chat_cat WHERE catid = ?'
        cursor.execute(getinfosql, ([catid]))
        catinfo = cursor.fetchone()
    connection.close()
    if catinfo:
        response = {
            'id': catid,
            'catname': catinfo[1]
        }
    else:
        response = {
            'id': catid,
            'catname': 'Архив'
        }
    return response


def edit_cat_name(catid, catname):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        editsql = 'UPDATE chat_cat SET catname = ? WHERE catid = ?'
        cursor.execute(editsql, ([catname, catid]))
        connection.commit()
    connection.close()


def delete_cat(catid):
    chats = get_chats_in_cat(catid)
    for chat in chats:
        upd_chat_status(chat.get('id'), 'arch')
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        dsql = 'DELETE FROM chat_cat WHERE catid = ?'
        cursor.execute(dsql, ([catid]))
        connection.commit()
    connection.close()


def get_arch_chat_for_user(catid):
    response = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getinfosql = 'SELECT chatid, chat_name, chat_url, catid FROM chats WHERE catid = ? AND status = ?'
        cursor.execute(getinfosql, ([catid, 'arch']))
        chatinfo = cursor.fetchall()
    connection.close()
    if len(chatinfo) > 0:
        for chat in chatinfo:
            response.append(
                {
                    'id': chat[0],
                    'chat_name': chat[1],
                    'chat_url': chat[2],
                    'catid': chat[3],
                }
            )
    return response


def get_no_cats_chats():
    response = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getinfosql = 'SELECT chatid, chat_name, chat_url, catid FROM chats WHERE status = ?'
        cursor.execute(getinfosql, (['arch']))
        chatinfo = cursor.fetchall()
    connection.close()
    if len(chatinfo) > 0:
        for chat in chatinfo:
            chek_cat = cat_info(chat[3])
            if chek_cat.get('catname') == 'Архив':
                response.append(
                    {
                        'id': chat[0],
                        'chat_name': chat[1],
                        'chat_url': chat[2],
                        'catid': chat[3],
                    }
                )
    return response


def get_users_seen_cat(catid):
    response = []
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getsql = 'SELECT user_id FROM access WHERE catid = ?'
        cursor.execute(getsql, ([catid]))
        uids = cursor.fetchall()
    connection.close()
    if len(uids) > 0:
        for uid in uids:
            response.append(
                {
                    'catid': catid,
                    'user_id': uid[0]
                }
            )
    return response


def chek_cat_accessing(catid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getsql = 'SELECT access FROM chat_cat WHERE catid = ?'
        cursor.execute(getsql, ([catid]))
        chk = cursor.fetchone()
    connection.close()
    if chk:
        if chk[0]:
            return True
        else:
            return False
    else:
        return False


def upd_accessing_status(catid, status=0):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        editsql = 'UPDATE chat_cat SET access = ? WHERE catid = ?'
        cursor.execute(editsql, ([status, catid]))
        connection.commit()
    connection.close()


def chek_user_seen_cat(user_id, catid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        getsql = 'SELECT user_id FROM access WHERE catid = ? AND user_id = ?'
        cursor.execute(getsql, ([catid, user_id]))
        uid = cursor.fetchone()
    connection.close()
    if uid:
        return True
    else:
        return False


def append_user_seen_cat(user_id, catid):
    chek_accesing = chek_cat_accessing(catid)
    if chek_accesing:
        pass
    else:
        upd_accessing_status(catid, status=1)
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        inssql = 'INSERT INTO access (user_id, catid) VALUES (?, ?)'
        cursor.execute(inssql, ([user_id, catid]))
        connection.commit()
    connection.close()


def remove_user_seen_cat(user_id, catid):
    connection = base_connect()
    with connection:
        cursor = connection.cursor()
        remsql = 'DELETE FROM access WHERE catid = ? AND user_id = ?'
        cursor.execute(remsql, ([catid, user_id]))
        connection.commit()
    connection.close()
    chekusers = get_users_seen_cat(catid)
    if chekusers:
        pass
    else:
        upd_accessing_status(catid, status=0)


def users_seen_cat_usernames(catid):
    text = ''
    users = get_users_seen_cat(catid)
    for user in users:
        userinfo = user_info(user.get('user_id'))
        if userinfo:
            if userinfo[1]:
                username = userinfo[1]
            else:
                username = userinfo[0]
        else:
            username = 'Администратор'
        text = text + username + '\n'
    if text:
        return text
    else:
        return 'Доступ предоставлен всем пользователям'
