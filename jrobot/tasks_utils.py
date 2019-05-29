# -*- coding: utf-8 -*-
from datetime import datetime as _datetime
from bot_utils import Basedate, str_to_array, array_to_str
from dbclasses import Task, UserTask


def create_task(creator_id, user_id, task_name, task_text, date_end):
    """
    Статусы:
    - 0: завершена
    - 1: активна, отправлена
    - 2: принята к исполнению
    - 3: отклонена
    - 4: неопубликованно
    """
    if creator_id == user_id:
        status = 2
    else:
        status = 1
    date_create = Basedate().date()
    date_start = Basedate().date_hms()
    info = {
        'task_text': task_text,
        'comment': ''
    }
    Task.create(
        name=task_name,
        creator_id=creator_id,
        date_create=date_create,
        date_start=date_start,
        date_end=date_end,
        info=array_to_str(info),
        status=status
    )
    task_id = Task.get(Task.date_start == date_start, Task.creator_id == creator_id).id
    UserTask.create(
        user_id=user_id,
        task_id=task_id
    )
    return task_id


def get_tasks_by_creator_id(creator_id):
    query = Task.select().where(Task.creator_id == creator_id)
    tasks = []
    for task in query:
        tasks.append(
            {
                'task_id': task.id,
                'task_name': task.name,
                'creator_id': creator_id,
                'date_create': task.date_create,
                'date_start': task.date_start,
                'date_end': task.date_end,
                'info': str_to_array(task.info),
                'status': task.status
            }
        )
    return tasks


def get_task_info(task_id):
    try:
        taskinfo = {
            'task_id': Task.get(Task.id == task_id).id,
            'task_name': Task.get(Task.id == task_id).name,
            'creator_id': Task.get(Task.id == task_id).creator_id,
            'date_create': Task.get(Task.id == task_id).date_create,
            'date_start': Task.get(Task.id == task_id).date_start,
            'date_end': Task.get(Task.id == task_id).date_end,
            'info': str_to_array(Task.get(Task.id == task_id).info),
            'status': Task.get(Task.id == task_id).status
        }
    except:
        taskinfo = None
    return taskinfo


def get_tasks_by_user_id(user_id):
    query_task_ids = UserTask.select().where(UserTask.user_id == user_id)
    tasks = []
    for task in query_task_ids:
        taskinfo = get_task_info(task.id)
        tasks.append(
            taskinfo
        )
    return tasks


def get_user_tasks_by_status(user_id, status=1):
    tasks = get_tasks_by_user_id(user_id)
    response = []
    for task in tasks:
        if task.get('status') == status:
            response.append(
                task
            )
    return response


def get_creator_tasks_by_status(creator_id, status=1):
    tasks = get_tasks_by_creator_id(creator_id)
    response = []
    for task in tasks:
        if task.get('status') == status:
            response.append(
                task
            )
    return response


def update_task_status(task_id, status=0, comment=''):
    """
    Статусы:
    - 0: завершена
    - 1: активна, отправлена
    - 2: принята к исполнению
    - 3: отклонена
    - 4: неопубликованно
    """
    if status == 0:
        taskinfo = get_task_info(task_id).get('info')
        info = {
            'task_text': taskinfo.get('task_text'),
            'comment': comment
        }
        Task.update(
            status=status,
            info=array_to_str(info)
        ).where(Task.id == task_id).execute()
    else:
        Task.update(
            status=status
        ).where(Task.id == task_id).execute()


def update_task_date_end(task_id, date_end):
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
    Task.update(date_end=dtend).where(Task.id == task_id).execute()


def get_uid_by_task_id(task_id):
    uid = UserTask.get(UserTask.task_id == task_id).user_id
    return uid
