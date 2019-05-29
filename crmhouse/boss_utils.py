# -*- coding: utf-8 -*-
from datetime import datetime

from consumers_utils import get_consumers_by_role
from dbclasses import Admin, AdminConsumerStata, ClientsStepsHistory, Manager, ManagerStadies
from user_utils import get_user_info_by_id, get_user_info


def get_agents(user_id):
    admin_id = admininfo(user_id).get('id')
    group = get_user_info(user_id).get('description')
    query_agents = Manager.select().where(Manager.group_id == admin_id)
    agents = []
    for agent in query_agents:
        if agent.role == 'admin':
            pass
        elif agent.role == 'manager':
            pass
        else:
            agents.append(
                get_user_info_by_id(agent.id)
            )
    if agents:
        pass
    else:
        query_agents = Manager.select().where(Manager.description == group)
        for agent in query_agents:
            if agent.role == 'admin':
                pass
            elif agent.role == 'manager':
                pass
            else:
                agents.append(
                    get_user_info_by_id(agent.id)
                )
    return agents


def admininfo(user_id):
    try:
        admininfos = {
            'id': Admin.get(Admin.user_id == user_id).id,
            'user_id': Admin.get(Admin.user_id == user_id).user_id,
            'status': Admin.get(Admin.user_id == user_id).status
        }
    except:
        admininfos = None
    return admininfos


def get_admins():
    adm_query = Admin.select()
    admins = []
    for admin in adm_query:
        admins.append(
            {
                'id': admin.id,
                'user_id': admin.user_id,
                'status': admin.status
            }
        )
    return admins


def upd_admin_stat(user_id):
    now = datetime.now()
    AdminConsumerStata.update(
        sellers=len(get_consumers_by_role('seller')),
        buyers=len(get_consumers_by_role('buyer')),
        date=now).where(AdminConsumerStata.user_id == user_id).execute()


def get_consumer_stata(user_id):
    now = datetime.now()
    try:
        stats = {
            'sellers': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).sellers,
            'buyers': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).buyers,
            'date': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).date
        }
    except:
        AdminConsumerStata.create(
            user_id=user_id,
            sellers=len(get_consumers_by_role('seller')),
            buyers=len(get_consumers_by_role('buyer')),
            date=now
        )
        stats = {
            'sellers': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).sellers,
            'buyers': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).buyers,
            'date': AdminConsumerStata.get(AdminConsumerStata.user_id == user_id).date
        }
    adminstat = {
        'sellers': len(get_consumers_by_role('seller')),
        'new_sellers': len(get_consumers_by_role('seller')) - stats.get('sellers'),
        'buyers': len(get_consumers_by_role('buyer')),
        'new_buyers': len(get_consumers_by_role('buyer')) - stats.get('buyers'),
    }
    if stats.get('date') < now:
        upd_admin_stat(user_id)
    return adminstat


def get_client_history(consumer_id, agent_id):
    current_stadi_date = ManagerStadies.get(
        ManagerStadies.consumer_id == consumer_id,
        ManagerStadies.manager_id == agent_id).date_start
    history = ''
    query = ClientsStepsHistory.select().where(
        ClientsStepsHistory.consumer_id == consumer_id,
        ClientsStepsHistory.agent_id == agent_id)
    curr = str(current_stadi_date).split(' ')[0].split('-')
    tcurr = str(current_stadi_date).split(' ')[1].split(':')
    curr = datetime(
        int(curr[0]),
        int(curr[1]),
        int(curr[2]),
        int(tcurr[0]),
        int(tcurr[1]))
    for client in query:
        dt = str(client.date).split(' ')[0].split('-')
        tdt = str(client.date).split(' ')[1].split(':')
        dt = datetime(
            int(dt[0]),
            int(dt[1]),
            int(dt[2]),
            int(tdt[0]),
            int(tdt[1]))
        if curr != dt:
            history += client.step_name + '\n'
    return history
