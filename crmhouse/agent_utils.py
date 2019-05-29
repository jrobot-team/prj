# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from bot_utils import Basedate, array_to_str, date_revers, str_to_array
from consumers_utils import get_consumer_info, get_prices_diap, get_town_by_district_id
from dbclasses import (AgentConsumerTask, ClientsSteps, ClientsStepsHistory,
                       Consumer, ManagerStadies, Stadies)
from user_utils import get_user_info


def get_agent_info(agent_id):
    return get_user_info(agent_id)


def get_agent_consumers(agent_id, role='seller'):
    consumers_query = Consumer.select().where(Consumer.manager_id == agent_id, Consumer.role == role)
    consumers = []
    for consumer in consumers_query:
        cinfo = get_consumer_info(consumer.id)
        consumers.append(
            cinfo
        )
    return consumers


def get_agent_base_consumers(agent_id, role='seller'):
    consumers_query = Consumer.select().where(Consumer.manager_id != agent_id, Consumer.role == role)
    consumers = []
    for consumer in consumers_query:
        cinfo = get_consumer_info(consumer.id)
        consumers.append(
            cinfo
        )
    return consumers


def filter_by_price_diap(agent_id, district_id, role, prices_diap):
    to_base_prices = []
    response = []
    srt_price = []
    if role == 'seller':
        for prices in prices_diap:
            query = Consumer.select().where(
                Consumer.manager_id != agent_id,
                Consumer.role == role,
                Consumer.district_id == district_id,
                Consumer.price.between(prices.get('min'), prices.get('max'))
            )
            for q in query:
                if q.id:
                    to_base_prices.append(prices)
    else:
        query = Consumer.select().where(
            Consumer.manager_id != agent_id,
            Consumer.role == role,
            Consumer.district_id == district_id
        )
        for cons in query:
            pr = get_prices_diap(get_consumer_info(cons.id).get('prices_id'))
            pmin = pr.get('price_min')
            srt_price.append(pmin)
        srt_price = sorted(set(srt_price))
        town_name = get_town_by_district_id(district_id).get('name')
        if town_name == 'Троицк':
            for price in srt_price:
                if price == 0:
                    response.append({
                        'min': 0,
                        'max': 4000000
                    })
                elif price == 9000000:
                    response.append({
                        'min': 9000000,
                        'max': 0
                    })
                else:
                    response.append({
                        'min': price,
                        'max': price + 1000000
                    })
        else:
            for price in srt_price:
                if price == 0:
                    response.append({
                        'min': 0,
                        'max': 1000000
                    })
                elif price == 1000000:
                    response.append({
                        'min': price,
                        'max': price + 1000000
                    })
                elif price == 4000000:
                    response.append({
                        'min': 4000000,
                        'max': 0
                    })
                else:
                    response.append({
                        'min': price,
                        'max': price + 500000
                    })
    if role == 'seller':
        if to_base_prices:
            first = to_base_prices[0].get('min')
            count = 0
            for pr in to_base_prices:
                if count:
                    if first == pr.get('min'):
                        pass
                    else:
                        response.append(pr)
                        first = pr.get('min')
                else:
                    response.append(pr)
                count += 1
    return response


def get_consumers_rooms(agent_id, role, district_id, prices):
    rooms = []
    if role == 'seller':
        query = Consumer.select(Consumer.rooms).where(
            Consumer.manager_id != agent_id,
            Consumer.role == role,
            Consumer.district_id == district_id,
            Consumer.price.between(prices.get('min'), prices.get('max'))
        )
        for r in query:
            rooms.append(
                int(r.rooms)
            )
    else:
        query = Consumer.select(Consumer.id).where(
            Consumer.manager_id != agent_id,
            Consumer.role == role,
            Consumer.district_id == district_id
        )
        for cons in query:
            pr = get_prices_diap(get_consumer_info(cons.id).get('prices_id'))
            if pr.get('price_min') == 0 and pr.get('price_max') > 0:
                midle_price = int(pr.get('price_max'))
            elif pr.get('price_max') == 0 and pr.get('price_min') > 0:
                midle_price = int(pr.get('price_min'))
            else:
                midle_price = int((pr.get('price_min') + pr.get('price_max')) / 2)
            if midle_price >= prices.get('min') and midle_price <= prices.get('max'):
                rooms.append(int(get_consumer_info(cons.id).get('rooms')))
    rooms = set(rooms)
    return rooms


def get_consumers_by_filter(agent_id, role, district_id, prices, rooms, fnd=None):
    consumers = []
    if role == 'seller':
        if fnd:
            query = Consumer.select().where(
                Consumer.manager_id != agent_id,
                Consumer.role == role,
                Consumer.district_id == district_id,
                Consumer.price.between(prices.get('min'), prices.get('max')),
                Consumer.rooms == rooms,
                Consumer.var_id == 0
            )
        else:
            query = Consumer.select().where(
                Consumer.manager_id != agent_id,
                Consumer.role == role,
                Consumer.district_id == district_id,
                Consumer.price.between(prices.get('min'), prices.get('max')),
                Consumer.rooms == rooms
            )
        for consumer in query:
            consumers.append(
                get_consumer_info(consumer.id)
            )
    else:
        query = Consumer.select(Consumer.id).where(
            Consumer.manager_id != agent_id,
            Consumer.role == role,
            Consumer.district_id == district_id,
            Consumer.rooms == rooms
        )
        for cons in query:
            pr = get_prices_diap(get_consumer_info(cons.id).get('prices_id'))
            if pr.get('price_min') == 0 and pr.get('price_max') > 0:
                midle_price = int(pr.get('price_max'))
            elif pr.get('price_max') == 0 and pr.get('price_min') > 0:
                midle_price = int(pr.get('price_min'))
            else:
                midle_price = int((pr.get('price_min') + pr.get('price_max')) / 2)
            if midle_price >= prices.get('min') and midle_price <= prices.get('max'):
                consumers.append(
                    get_consumer_info(cons.id)
                )
    return consumers


def addstad(role, name, tb, tp, details):
    Stadies.create(
        to_role=role,
        name=name,
        time_before=tb,
        time_past=tp,
        details=array_to_str(details)
    )


def get_consumer_stadies(consumer_id, agent_id, status=None):
    stadies = []
    if status is not None:
        query = ManagerStadies.select().where(
            ManagerStadies.manager_id == agent_id,
            ManagerStadies.consumer_id == consumer_id,
            ManagerStadies.status == status
        )
    else:
        query = ManagerStadies.select().where(
            ManagerStadies.manager_id == agent_id,
            ManagerStadies.consumer_id == consumer_id
        )
    for stadi in query:
        stadies.append(
            {
                'id': stadi.id,
                'stadies_id': stadi.stadies_id,
                'manager_id': stadi.manager_id,
                'consumer_id': stadi.consumer_id,
                'sub_stadies_id': stadi.sub_stadies_id,
                'sub_sub_stadies_id': stadi.sub_sub_stadies_id,
                'status': stadi.status
            }
        )
    return stadies


def get_stadi_info(stid):
    try:
        stinfo = {
            'id': Stadies.get(Stadies.id == stid).id,
            'to_role': Stadies.get(Stadies.id == stid).to_role,
            'name': Stadies.get(Stadies.id == stid).name,
            'time_before': Stadies.get(Stadies.id == stid).time_before,
            'time_past': Stadies.get(Stadies.id == stid).time_past,
            'details': str_to_array(Stadies.get(Stadies.id == stid).details),
            'steps': Stadies.get(Stadies.id == stid).steps
        }
    except:
        stinfo = None
    return stinfo


def chek_st(sid, consumer_id):
    try:
        chek_mst_id = ManagerStadies.get(
            ManagerStadies.stadies_id == sid,
            ManagerStadies.consumer_id == consumer_id).id
    except:
        chek_mst_id = None
    return chek_mst_id


def upd_st(sid, consumer_id, agent_id):
    ManagerStadies.update(
        date_start=Basedate().date_hm(),
        manager_id=agent_id,
        status=1).where(
            ManagerStadies.stadies_id == sid,
            ManagerStadies.consumer_id == consumer_id).execute()


def create_st(sid, consumer_id, agent_id):
    date_start = Basedate().date_hms()
    ManagerStadies.create(
        date_start=date_start,
        stadies_id=sid,
        manager_id=agent_id,
        consumer_id=consumer_id
    )
    stid = ManagerStadies.get(
        ManagerStadies.date_start == date_start,
        ManagerStadies.consumer_id == consumer_id,
        ManagerStadies.manager_id == agent_id).id
    return stid


def prep_stadi(sid, consumer_id, agent_id):
    chek_st_id = chek_st(sid, consumer_id)
    if chek_st_id:
        upd_st(sid, consumer_id, agent_id)
        ManagerStadies.update(status=0).where(
            ManagerStadies.consumer_id == consumer_id,
            ManagerStadies.id != chek_st_id).execute()
        return chek_st_id
    else:
        stid = create_st(sid, consumer_id, agent_id)
        return stid


def upd_stadi_status(sid, consumer_id, agent_id, status=0):
    ManagerStadies.update(status=status).where(
        ManagerStadies.stadies_id == sid,
        ManagerStadies.manager_id == agent_id,
        ManagerStadies.consumer_id == consumer_id).execute()


def get_last_consumer_stadi(consumer_id, agent_id):
    stadies = get_consumer_stadies(
        consumer_id,
        agent_id,
        status=1
    )
    if stadies:
        count_id = stadies[0].get('stadies_id')
        for st in stadies:
            if count_id <= st.get('stadies_id'):
                count_id = st.get('stadies_id')
    else:
        prep_stadi(1, consumer_id, agent_id)
        count_id = 1
    return count_id


def seller_prep_to_meet(consumer_id, agent_id, sid=1):
    prep_stadi(sid, consumer_id, agent_id)
    stinfo = get_stadi_info(sid)
    return stinfo


def buyer_prep_to_view(consumer_id, agent_id, sid=10):
    prep_stadi(sid, consumer_id, agent_id)
    stinfo = get_stadi_info(sid)
    return stinfo


def get_agent_client_stadies(agent_id, role):
    stadies_names = []
    query = ClientsSteps.select().where(
        ClientsSteps.agent_id == agent_id, ClientsSteps.role == role)
    for st in query:
        stadies_names.append(
            st.step_name
        )
    stadies_names = set(stadies_names)
    return stadies_names


def get_clients_in_stadi(sid, agent_id):
    query = ClientsSteps.select().where(ClientsSteps.step_name == sid, ClientsSteps.agent_id == agent_id)
    clients = []
    for client in query:
        clients.append(
            get_consumer_info(client.consumer_id)
        )
    return clients


def get_stadi_history(sid, role):
    query = Stadies.select().where(Stadies.to_role == role, Stadies.steps == 0)
    history = []
    count = 0
    for st in query:
        if st.id < sid:
            history.append(
                (
                    st.id,
                    st.name
                )
            )
            count += 1
    return history


def get_current_st(consumer_id, agent_id):
    mg = ManagerStadies
    try:
        current_st = {
            'id': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).id,
            'date_start': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).date_start,
            'sid': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).stadies_id,
            'agent_id': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).manager_id,
            'consumer_id': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).consumer_id,
            'sub_stadies_id': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).sub_stadies_id,
            'sub_sub_stadies_id': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).sub_sub_stadies_id,
            'status': mg.get(
                mg.manager_id == agent_id,
                mg.consumer_id == consumer_id,
                mg.status == 1).status,
        }
    except:
        current_st = None
    return current_st


def upd_sub_stadies(mgid, substid=None, subsubstid=None):
    mg = ManagerStadies
    if substid:
        mg.update(sub_stadies_id=substid).where(mg.id == mgid).execute()
    if subsubstid:
        mg.update(sub_sub_stadies_id=subsubstid).where(mg.id == mgid).execute()


def upd_stadi(stadies_id, mgid):
    mg = ManagerStadies
    mg.update(stadies_id=stadies_id, sub_stadies_id=0, sub_sub_stadies_id=0).where(mg.id == mgid).execute()


def consumer_move_to_base(consumer_id):
    del_consumer_tasks(consumer_id)
    mg = ManagerStadies
    mg.delete().where(mg.consumer_id == consumer_id).execute()
    ClientsSteps.delete().where(ClientsSteps.consumer_id == consumer_id).execute()
    Consumer.update(manager_id=0).where(Consumer.id == consumer_id).execute()


def get_current_sid(consumer_id, agent_id):
    mg = ManagerStadies
    sid = mg.get(mg.consumer_id == consumer_id, mg.manager_id == agent_id).stadies_id
    return sid


def create_agent_task(agent_id, consumer_id, sid, date_start):
    ManagerStadies.delete().where(ManagerStadies.consumer_id == consumer_id).execute()
    create_st(sid, consumer_id, agent_id)
    del_consumer_tasks(consumer_id)
    agtask = AgentConsumerTask
    dtnow = datetime.now() + timedelta(hours=5)
    sinfo = get_stadi_info(sid)
    name = sinfo.get('name')
    time_before = sinfo.get('time_before')
    time_past = sinfo.get('time_past')
    if time_before:
        date_alert = date_start - timedelta(hours=time_before)
    else:
        date_alert = date_start + timedelta(hours=time_past)
    agtask.create(
        date_create=dtnow,
        date_start=date_start,
        name=name,
        consumer_id=consumer_id,
        agent_id=agent_id,
        sid=sid,
        date_alert=date_alert
    )
    ClientsStepsHistory.create(
        consumer_id=consumer_id,
        step_name=name,
        agent_id=agent_id,
        date=dtnow,
        date_end=date_alert)


def del_agent_task(task_id):
    AgentConsumerTask.delete().where(AgentConsumerTask.id == task_id).execute()


def del_consumer_tasks(consumer_id):
    AgentConsumerTask.delete().where(AgentConsumerTask.consumer_id == consumer_id).execute()


def get_agent_tasks(agent_id):
    tasks = []
    query = AgentConsumerTask.select().where(AgentConsumerTask.agent_id == agent_id)
    for task in query:
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
                'sended': task.sended
            }
        )
    return tasks


def get_agent_task_info(task_id):
    agt = AgentConsumerTask
    try:
        task = {
            'id': agt.get(agt.id == task_id).id,
            'date_create': agt.get(agt.id == task_id).date_create,
            'date_start': agt.get(agt.id == task_id).date_start,
            'name': agt.get(agt.id == task_id).name,
            'consumer_id': agt.get(agt.id == task_id).consumer_id,
            'agent_id': agt.get(agt.id == task_id).agent_id,
            'sid': agt.get(agt.id == task_id).sid,
            'description': str_to_array(agt.get(agt.id == task_id).description),
            'date_alert': agt.get(agt.id == task_id).date_alert,
            'sended': agt.get(agt.id == task_id).sended
        }
    except:
        task = None
    return task


def get_current_task_name(consumer_id, agent_id):
    agt = AgentConsumerTask
    try:
        name = agt.get(agt.consumer_id == consumer_id, agt.agent_id == agent_id).name
    except:
        name = 'Не определено'
    date_end = agt.get(agt.consumer_id == consumer_id, agt.agent_id == agent_id).date_alert
    response = {
        'name': name,
        'date_end': date_revers(date_end)
    }
    return response


def create_client_step(consumer_id, step_name, agent_id, role):
    dtnow = datetime.now() + timedelta(hours=5)
    date_alert = datetime.now() + timedelta(hours=5)
    ClientsSteps.delete().where(ClientsSteps.consumer_id == consumer_id).execute()
    if step_name == 'Реклама':
        ClientsStepsHistory.create(
            consumer_id=consumer_id,
            step_name=step_name,
            agent_id=agent_id,
            date=dtnow,
            date_end=date_alert)
    else:
        ClientsSteps.create(
            consumer_id=consumer_id,
            step_name=step_name,
            agent_id=agent_id,
            role=role)
        if step_name == 'Внесён аванс':
            ClientsStepsHistory.create(
                consumer_id=consumer_id,
                step_name=step_name,
                agent_id=agent_id,
                date=dtnow,
                date_end=date_alert)


def get_client_stepname(consumer_id):
    step_name = ClientsSteps.get(ClientsSteps.consumer_id == consumer_id).step_name
    return step_name


def price_formatter(price):
    plen = len(str(price))
    if plen == 6:
        pstr = str(price)
        reprice = '{f}.{e}'.format(
            f=pstr[:3],
            e=pstr[3:]
        )
        return reprice
    elif plen == 7:
        pstr = str(price)
        endprice = pstr[-6:]
        reprice = '{s}.{f}.{e}'.format(
            s=pstr[:1],
            f=endprice[:3],
            e=endprice[3:]
        )
        return reprice
    elif plen == 8:
        pstr = str(price)
        endprice = pstr[-6:]
        reprice = '{s}.{f}.{e}'.format(
            s=pstr[:2],
            f=endprice[:3],
            e=endprice[3:]
        )
        return reprice
    elif plen == 9:
        pstr = str(price)
        endprice = pstr[-6:]
        reprice = '{s}.{f}.{e}'.format(
            s=pstr[:3],
            f=endprice[:3],
            e=endprice[3:]
        )
        return reprice
    elif plen == 10:
        pstr = str(price)
        endprice = pstr[-6:]
        reprice = '{s}.{f}.{e}'.format(
            s=pstr[:3],
            f=endprice[:3],
            e=endprice[3:]
        )
        return reprice
    else:
        return price
