# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, CharField, DateField, DateTimeField,
                    FloatField, IntegerField, Model,
                    TextField)
from playhouse.sqlite_ext import SqliteExtDatabase
from bot_utils import Basedate

db = SqliteExtDatabase(
    'database/crmhouse.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)))


class Manager(Model):
    """
    Общая таблица пользователей role (manager, agent, admin)
    info содржит json с дополнительными полями
    """
    date_create = DateTimeField()
    user_id = BigIntegerField()
    name = CharField(default='noname')
    phone = CharField(default='no_phone')
    role = CharField(default='manager')
    group_id = IntegerField(default=0)
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=0)

    class Meta:
        database = db


class Report(Model):
    manager_id = BigIntegerField()
    report_text = TextField(default='')
    status = IntegerField(default=0)
    send = IntegerField(default=0)

    class Meta:
        database = db


class Group(Model):
    owner_id = BigIntegerField()
    name = CharField(default='noname')
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class ManagerGroup(Model):
    user_id = BigIntegerField()
    group_id = IntegerField()

    class Meta:
        database = db


class Task(Model):
    creator_id = BigIntegerField()
    name = CharField(default='noname')
    task_text = TextField(default='noname')
    description = TextField(default='')
    date_create = DateField(default=Basedate().date())
    date_start = DateTimeField(default=Basedate().date_hm())
    date_end = DateTimeField(default=Basedate().plus_one_day())
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class ManagerTask(Model):
    user_id = BigIntegerField()
    task_id = IntegerField()

    class Meta:
        database = db


class Note(Model):
    name = CharField()
    note_text = TextField(default='')
    description = TextField(default='')
    group_id = IntegerField(default=0)
    info = TextField(default='{}')

    class Meta:
        database = db


class NoteGroup(Model):
    name = CharField()
    description = TextField(default='')
    info = TextField(default='{}')

    class Meta:
        database = db


class ManagerChekNote(Model):
    user_id = BigIntegerField()
    note_id = IntegerField()
    status = IntegerField(default=0)

    class Meta:
        database = db


class Consumer(Model):
    """
    роли role (buyer, seller) --> покупатель, продавец
    info содржит json с дополнительными полями
    """
    date_create = DateTimeField()
    name = CharField(default='noname')
    phone = CharField(default='no_phone')
    role = CharField(default='buyer')
    group_id = IntegerField(default=0)
    district_id = IntegerField(default=0)
    price = FloatField(default=0.0)
    prices_id = IntegerField(default=0)
    address = TextField(default='no_address')
    area = FloatField(default=0.0)
    rooms = FloatField(default=1.0)
    manager_id = BigIntegerField(default=0)
    info = TextField(default='{}')
    status = IntegerField(default=0)
    var_id = IntegerField(default=0)

    class Meta:
        database = db


class ConsumerStatuses(Model):
    """
    Таблица со статусами (
        ■	Продавец
            ●	Назначена встреча
            ●	Проведена встреча
            ●	Подписан договор
            ●	Запущена реклама
            ●	Объект продан
        ■	Покупатель
            ●	Назначен показ
            ●	Проведен показ
            ●	Подобран объект
            ●	Получен аванс
            ●	Сделка завершена
    )
    """
    name = CharField()
    status_number = IntegerField()
    info = TextField(default='{}')

    class Meta:
        database = db


class ConsumerGroup(Model):
    name = CharField()
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class District(Model):
    date_create = DateTimeField()
    name = CharField()
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class Town(Model):
    date_create = DateTimeField()
    name = CharField()
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class TownDistricts(Model):
    town_id = IntegerField()
    district_id = IntegerField()

    class Meta:
        database = db


class Prices(Model):
    name = CharField()
    price_min = FloatField(default=0.0)
    price_max = FloatField(default=0.0)
    description = TextField(default='')
    info = TextField(default='{}')
    status = IntegerField(default=1)

    class Meta:
        database = db


class TempConsumers(Model):
    consumer_id = IntegerField()
    agent_id = IntegerField()

    class Meta:
        database = db


class Stadies(Model):
    to_role = CharField()
    name = CharField()
    time_before = IntegerField(default=0)
    time_past = IntegerField(default=0)
    details = TextField(default='{}')
    steps = IntegerField(default=0)

    class Meta:
        database = db


class ManagerStadies(Model):
    date_start = DateTimeField()
    stadies_id = IntegerField()
    manager_id = IntegerField()
    consumer_id = IntegerField()
    sub_stadies_id = IntegerField(default=0)
    sub_sub_stadies_id = IntegerField(default=0)
    status = IntegerField(default=1)

    class Meta:
        database = db


class AgentConsumerTask(Model):
    date_create = DateTimeField()
    date_start = DateTimeField()
    name = CharField()
    consumer_id = IntegerField()
    agent_id = IntegerField()
    sid = IntegerField()
    description = TextField(default='{}')
    date_alert = DateTimeField()
    sended = IntegerField(default=0)

    class Meta:
        database = db


class ClientsSteps(Model):
    role = CharField()
    consumer_id = IntegerField()
    agent_id = IntegerField()
    step_name = CharField()

    class Meta:
        database = db


class ClientsStepsHistory(Model):
    consumer_id = IntegerField()
    agent_id = IntegerField()
    step_name = CharField()
    date = DateTimeField()
    date_end = DateTimeField()

    class Meta:
        database = db


class Admin(Model):
    user_id = BigIntegerField()
    status = IntegerField(default=1)
    phone = CharField()

    class Meta:
        database = db


class AdminConsumerStata(Model):
    user_id = BigIntegerField()
    sellers = IntegerField(default=0)
    buyers = IntegerField(default=0)
    date = DateTimeField()

    class Meta:
        database = db


db.connect()
db.create_tables(
    [
        Manager,
        Report,
        Group,
        ManagerGroup,
        Task,
        ManagerTask,
        Note,
        NoteGroup,
        ManagerChekNote,
        Consumer,
        ConsumerStatuses,
        ConsumerGroup,
        District,
        Town,
        TownDistricts,
        Prices,
        TempConsumers,
        Stadies,
        ManagerStadies,
        AgentConsumerTask,
        ClientsSteps,
        ClientsStepsHistory,
        Admin,
        AdminConsumerStata
    ]
)
db.close()
