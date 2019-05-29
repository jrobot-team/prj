# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, CharField, DateField, DateTimeField,
                    IntegerField, Model, TextField)
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase(
    'database/jrobotbase.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)))


class User(Model):
    user_id = BigIntegerField()
    name = CharField(default='noname')
    role = CharField(default='newuser')
    info = TextField(default='{}')
    status = IntegerField(default=0)
    refer = BigIntegerField(default=0)

    class Meta:
        database = db


class Lang(Model):
    user_id = BigIntegerField()
    lang = IntegerField(default=0)

    class Meta:
        database = db


class Group(Model):
    name = CharField()
    owner_id = BigIntegerField()
    info = TextField(default='{}')

    class Meta:
        database = db


class GroupUsers(Model):
    group_id = IntegerField()
    user_id = BigIntegerField()

    class Meta:
        database = db


class Task(Model):
    name = CharField(default='noname')
    creator_id = BigIntegerField()
    date_create = DateField()
    date_start = DateTimeField()
    date_end = DateTimeField()
    info = TextField(default='{}')
    status = IntegerField(default=1)
    send = IntegerField(default=0)

    class Meta:
        database = db


class UserTask(Model):
    user_id = BigIntegerField()
    task_id = IntegerField()

    class Meta:
        database = db


class Question(Model):
    category = CharField(default='Без категории')
    paragraph = TextField(default=' ')
    question = TextField(default=' ')
    right_answer = TextField(default=' ')
    right_true = IntegerField(default=1)
    whrong_answers = TextField(default='[]')

    class Meta:
        database = db


class LastQuestion(Model):
    user_id = BigIntegerField()
    question_id = IntegerField()

    class Meta:
        database = db


class QuestionUserRec(Model):
    user_id = BigIntegerField()
    question_id = IntegerField()
    answers = TextField()

    class Meta:
        database = db


class UserAnswers(Model):
    user_id = BigIntegerField()
    question_id = IntegerField()
    answers = TextField()

    class Meta:
        database = db


class Answers(Model):
    user_id = BigIntegerField()
    question_id = IntegerField()
    result = IntegerField(default=0)

    class Meta:
        database = db


class TestHistory(Model):
    user_id = BigIntegerField()
    question_id = IntegerField()
    answers = TextField()

    class Meta:
        database = db


class Forum(Model):
    name = CharField(default='Без названия')
    creator_id = BigIntegerField()
    group_id = IntegerField()
    date_create = DateField()
    date_start = DateTimeField()
    date_end = DateTimeField()
    forum_theme = TextField()
    status = IntegerField(default=0)
    info = TextField(default='{}')
    send = IntegerField(default=0)

    class Meta:
        database = db


class ForumUsers(Model):
    forum_id = IntegerField()
    user_id = BigIntegerField()

    class Meta:
        database = db


class ForumPrepareUsers(Model):
    creator_id = IntegerField()
    user_id = BigIntegerField()

    class Meta:
        database = db


class Poll(Model):
    group_id = IntegerField()
    name = CharField(max_length=512)
    polltext = TextField()
    creator_id = BigIntegerField()
    date_create = DateField()
    date_start = DateTimeField()
    date_end = DateTimeField()
    status = IntegerField(default=1)

    class Meta:
        database = db


class PollQuestion(Model):
    poll_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class Userpoll(Model):
    user_id = BigIntegerField()
    poll_id = IntegerField()
    question_id = IntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables(
    [
        User,
        Lang,
        Group,
        GroupUsers,
        Task,
        UserTask,
        Question,
        QuestionUserRec,
        LastQuestion,
        UserAnswers,
        Answers,
        TestHistory,
        Forum,
        ForumUsers,
        ForumPrepareUsers,
        Poll,
        PollQuestion,
        Userpoll
    ]
)
db.close()
