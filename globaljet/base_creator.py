# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, CharField, DateField, DateTimeField,
                    FloatField, IntegerField, Model,
                    TextField)
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase(
    'database/jg_base.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)))


class Admin(Model):
    user_id = BigIntegerField()
    role = CharField(default='manager')
    status = IntegerField(default=1)
    lang = IntegerField(default=0)

    class Meta:
        database = db


class User(Model):
    user_id = BigIntegerField()
    username = CharField()
    fio = CharField(max_length=512, default='')
    phone = CharField(default='')
    register = IntegerField(default=1)
    lang = IntegerField(default=0)

    class Meta:
        database = db


class Plane(Model):
    plane = CharField()
    producer = CharField()
    seats_in = IntegerField(default=10)
    picture = CharField(default='')
    description = TextField(default='')
    producer_url = CharField(max_length=512, default='')
    flight_time = CharField(default='')
    fltime = IntegerField()

    class Meta:
        database = db


class BookingBase(Model):
    date = DateTimeField()
    plane_id = IntegerField()
    seats_off = IntegerField()
    direction_out = CharField(max_length=512, default='')
    direction = CharField(max_length=512, default='')
    price = FloatField(default=0.0)
    flight_time = CharField(default='')
    status = IntegerField(default=0)

    class Meta:
        database = db


class Booking(Model):
    user_id = BigIntegerField()
    price = FloatField(default=0.0)
    seats = IntegerField(default=1)
    day_to_flight = DateField()
    dtf_set = IntegerField(default=0)
    date = DateTimeField()
    plane_id = IntegerField(default=0)
    direction_out = CharField(max_length=512, default='')
    direction = CharField(max_length=512, default='')
    flight_time = CharField(default='')
    status = CharField(default='ask')
    alerted = IntegerField(default=0)
    hours_alert = IntegerField(default=0)
    date_fly = CharField(max_length=512, default='')
    date_sync = IntegerField(default=0)
    comment = TextField(default='')
    plane_model = TextField(default='')
    company = TextField(default='')
    price_char = CharField(default='0.0')
    hard_reise = TextField(default='no_hard')

    class Meta:
        database = db


class TempUserCatPlanes(Model):
    user_id = BigIntegerField()
    seats = IntegerField(default=0)
    flight_time = CharField(default='1-2')
    plane_id = IntegerField(default=0)
    booking_id = IntegerField(default=0)

    class Meta:
        database = db


class MsgCount(Model):
    user_id = BigIntegerField()
    chat_id = BigIntegerField()
    message_id = IntegerField()

    class Meta:
        database = db


class Temper(Model):
    user_id = BigIntegerField()
    temp_id = IntegerField()
    temp = TextField(default='')

    class Meta:
        database = db


db.connect()
db.create_tables(
    [
        Admin,
        User,
        Plane,
        BookingBase,
        Booking,
        TempUserCatPlanes,
        MsgCount,
        Temper
    ]
)
db.close()
