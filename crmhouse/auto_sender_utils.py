# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dbclasses import Consumer, ClientsStepsHistory, Manager, AgentConsumerTask
from consumers_utils import get_consumers_by_role, get_consumer_info
from bot_utils import str_to_array
from agent_utils import get_stadi_info
from user_utils import get_user_info


def get_consumers_count(diap):
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    query_cons = Consumer.select().where(Consumer.date_create.between(dstart, dend))
    sellers_week = []
    buyers_week = []
    for cons in query_cons:
        if cons.role == 'seller':
            sellers_week.append(
                cons.id
            )
        else:
            buyers_week.append(
                cons.id
            )
    response = {
        'sellers': len(get_consumers_by_role('seller')),
        'new_sellers': len(sellers_week),
        'buyers': len(get_consumers_by_role('buyer')),
        'new_buyers': len(buyers_week)
    }
    return response


def get_clients_meets(uid, diap, agent_id=None):
    now = datetime.now()
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    meets = []
    meets_done = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Встреча',
            ClientsStepsHistory.date.between(dstart, dend))
        done_query = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Встреча',
            ClientsStepsHistory.date_end < now,
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            meets.append(
                consumer.id
            )
        for consumer in done_query:
            meets_done.append(
                consumer.id
            )
    response = {
        'meets': len(meets),
        'meets_done': len(meets_done)
    }
    return response


def get_clients_dog_do(uid, diap, agent_id=None):
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    bdogs = []
    sdogs = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Подписан договор',
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            if get_consumer_info(consumer.id).get('role') == 'seller':
                sdogs.append(
                    consumer.id
                )
            else:
                bdogs.append(
                    consumer.id
                )
    response = {
        'bdogs': len(bdogs),
        'sdogs': len(sdogs)
    }
    return response


def get_clients_rek(uid, diap, agent_id=None):
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    reks = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Реклама',
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            reks.append(
                consumer.id
            )
    response = {
        'reks': len(reks)
    }
    return response


def get_clients_pokaz(uid, diap, agent_id=None):
    now = datetime.now()
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    meets = []
    meets_done = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Показ',
            ClientsStepsHistory.date.between(dstart, dend))
        done_query = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Показ',
            ClientsStepsHistory.date_end < now,
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            meets.append(
                consumer.id
            )
        for consumer in done_query:
            meets_done.append(
                consumer.id
            )
    response = {
        'pokaz': len(meets),
        'pokaz_done': len(meets_done)
    }
    return response


def get_clients_avans(uid, diap, agent_id=None):
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    avans = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Внесён аванс',
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            avans.append(
                consumer.id
            )
    response = {
        'avans': len(avans)
    }
    return response


def get_clients_sdelka(uid, diap, agent_id=None):
    if diap == 'week':
        dstart = datetime.now() - timedelta(days=7)
    else:
        dstart = datetime.now() - timedelta(days=1)
    dend = datetime.now()
    manager_query = Manager.select().where(Manager.group_id == uid)
    managers_ids = []
    sdelka = []
    for manager in manager_query:
        managers_ids.append(
            manager.user_id
        )
    if managers_ids:
        pass
    else:
        group = get_user_info(uid).get('description')
        manager_query = Manager.select().where(Manager.description == group)
        for manager in manager_query:
            managers_ids.append(
                manager.user_id
            )
    if agent_id is not None:
        managers_ids = [agent_id]
    for uid in managers_ids:
        mquery = ClientsStepsHistory.select().where(
            ClientsStepsHistory.agent_id == uid,
            ClientsStepsHistory.step_name == 'Сделка',
            ClientsStepsHistory.date.between(dstart, dend))
        for consumer in mquery:
            sdelka.append(
                consumer.id
            )
    response = {
        'sdelka': len(sdelka)
    }
    return response


def get_agent_task(agent_id):
    now = datetime.now() + timedelta(hours=1)
    dstart = now - timedelta(minutes=1)
    dend = now + timedelta(minutes=1)
    act = AgentConsumerTask
    task_query = act.select().where(
        act.agent_id == agent_id,
        act.date_alert.between(dstart, dend),
        act.sended == 1)
    tasks = []
    for task in task_query:
        sinfo = get_stadi_info(task.sid)
        tasks.append(
            {
                'id': task.id,
                'date_create': task.date_create,
                'date_start': task.date_start,
                'name': task.name,
                'consumer_id': task.consumer_id,
                'agent_id': task.agent_id,
                'sid': task.sid,
                'description': str_to_array(task.description),
                'date_alert': task.date_alert,
                'sended': task.sended,
                'to_role': sinfo.get('to_role'),
                'sname': sinfo.get('name'),
                'time_before': sinfo.get('time_before'),
                'time_past': sinfo.get('time_past'),
                'details': sinfo.get('details'),
                'steps': sinfo.get('steps')
            }
        )
    return tasks


def get_agent_prepares(agent_id):
    now = datetime.now() + timedelta(hours=3)
    dstart = now - timedelta(minutes=1)
    dend = now + timedelta(minutes=1)
    act = AgentConsumerTask
    task_query = act.select().where(
        act.agent_id == agent_id,
        act.date_start.between(dstart, dend),
        act.sended == 0)
    ret = []
    for task in task_query:
        if task.sid == 2:
            sinfo = get_stadi_info(1)
            ret.append(
                {
                    'consumer_id': task.consumer_id,
                    'task_id': task.id,
                    'sid': 1,
                    'agent_id': agent_id,
                    'sinfo': sinfo
                }
            )
        if task.sid == 4:
            sinfo = get_stadi_info(3)
            ret.append(
                {
                    'consumer_id': task.consumer_id,
                    'task_id': task.id,
                    'sid': 3,
                    'agent_id': agent_id,
                    'sinfo': sinfo
                }
            )
        if task.sid == 11:
            sinfo = get_stadi_info(10)
            ret.append(
                {
                    'consumer_id': task.consumer_id,
                    'task_id': task.id,
                    'sid': 10,
                    'agent_id': agent_id,
                    'sinfo': sinfo
                }
            )
        if task.sid == 13:
            sinfo = get_stadi_info(12)
            ret.append(
                {
                    'consumer_id': task.consumer_id,
                    'task_id': task.id,
                    'sid': 12,
                    'agent_id': agent_id,
                    'sinfo': sinfo
                }
            )
        if task.sid == 15:
            sinfo = get_stadi_info(14)
            ret.append(
                {
                    'consumer_id': task.consumer_id,
                    'task_id': task.id,
                    'sid': 14,
                    'agent_id': agent_id,
                    'sinfo': sinfo
                }
            )
    return ret


def set_sended_agent_task(task_id, sended=1):
    AgentConsumerTask.update(sended=sended).where(AgentConsumerTask.id == task_id).execute()
