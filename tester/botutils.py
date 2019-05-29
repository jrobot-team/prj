# -*- coding: utf-8 -*-
import random
import json
from datetime import datetime

import pytz

from config import TIMEZONE
from dbexec import sql_delete, sql_insert, sql_select, sql_update
from lang import ru


class Basedate(object):
    def __init__(self, tzone=TIMEZONE):
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


def reg_user(user_id, username):
    query_dict = {
        'table': 'users',
        'user_id': user_id,
        'username': username,
        'date_reg': Basedate().date()
    }
    sql_insert(query_dict)


def make_fio_fn(user_id, fio):
    query_dict = {
        'table': 'users',
        'fio': fio
    }
    sql_update(query_dict, argument='user_id', arg_val=user_id)


def make_agency_fn(user_id, agency):
    query_dict = {
        'table': 'users',
        'agency': agency
    }
    sql_update(query_dict, argument='user_id', arg_val=user_id)


def make_town_fn(user_id, town):
    query_dict = {
        'table': 'users',
        'town': town,
        'register': 1
    }
    sql_update(query_dict, argument='user_id', arg_val=user_id)


def get_user_info(user_id):
    query_dict = {
        'table': 'users',
        'rows': [
            'id',
            'user_id',
            'username',
            'fio',
            'phone',
            'agency',
            'town',
            'date_reg',
            'register',
            'test_count',
            'learn_count',
            'test_question_id',
            'learn_question_id'
        ]
    }
    userinfo = sql_select(
        query_dict,
        fetch='one',
        argument='user_id',
        arg_val=user_id)
    return userinfo


def get_users():
    query_dict = {
        'table': 'users',
        'rows': [
            'id',
            'user_id',
            'username',
            'fio',
            'phone',
            'agency',
            'town',
            'date_reg'
        ]
    }
    users = sql_select(query_dict, fetch='all')
    return users


def get_question(question_id):
    """
    return question, answers
    """
    query_dict = {
        'table': 'questions',
        'rows': [
            'id',
            'category',
            'paragraf',
            'question'
        ]
    }
    question = sql_select(
        query_dict,
        fetch='one',
        argument='id',
        arg_val=question_id)
    answers_query = {
        'table': 'answers',
        'rows': [
            'id',
            'question_id',
            'answer',
            'is_true'
        ]
    }
    answers = sql_select(
        answers_query,
        fetch='all',
        argument='question_id',
        arg_val=question_id)
    return question, answers


def questions_count():
    query_dict = {
        'table': 'questions',
        'rows': [
            'id'
        ]
    }
    q_count = sql_select(
        query_dict,
        fetch='all')
    return len(q_count)


def upd_user_learn_question_id(user_id, question_id):
    learn_question_id = get_user_info(user_id)[0].get('learn_question_id')
    if question_id:
        query_dict = {
            'table': 'users',
            'learn_question_id': learn_question_id + 1
        }
    else:
        query_dict = {
            'table': 'users',
            'learn_question_id': 1
        }
    sql_update(
        query_dict,
        argument='user_id',
        arg_val=user_id)


def upd_user_test_question_id(user_id, question_id):
    test_question_id = get_user_info(user_id)[0].get('test_question_id')
    if question_id:
        query_dict = {
            'table': 'users',
            'test_question_id': test_question_id + 1
        }
    else:
        query_dict = {
            'table': 'users',
            'test_question_id': 1
        }
    sql_update(
        query_dict,
        argument='user_id',
        arg_val=user_id)


def answers_formatter(user_id, question_id, rnd=True):
    """
    return text, answer_list
    """
    if rnd:
        del_answers_list(user_id)
        answers = get_question(question_id)[1]
        random.shuffle(answers)
        query_make_ans_list = {
            'table': 'ans_list',
            'user_id': user_id,
            'answers': array_to_str(answers)
        }
        sql_insert(query_make_ans_list)
    else:
        get_answers_query = {
            'table': 'ans_list',
            'rows': [
                'answers'
            ]
        }
        answers = sql_select(
            get_answers_query,
            fetch='one',
            argument='user_id',
            arg_val=user_id)[0].get('answers')
        answers = str_to_array(answers)
    text = ''
    answer_list = []
    count = 0
    for ans in answers:
        count += 1
        text = text + ru.get('answers').format(
            answer_number=count,
            answer=ans.get('answer'))
        answer_list.append([count, ans.get('id'), 'nocheked'])
    return text, answer_list


def del_answers_list(user_id):
    sql_delete(
        'ans_list',
        argument='user_id',
        arg_val=user_id)


def chek_answer(user_id, question_id, answer_id):
    query_dict = {
        'table': 'user_test',
        'rows': [
            'user_id',
            'question_id',
            'answer_cheked'
        ]
    }
    answer_cheked = sql_select(
        query_dict,
        fetch='one',
        argument='user_id',
        arg_val=user_id
    )
    if answer_cheked[0]:
        answer_cheked_list = str_to_array(answer_cheked[0].get('answer_cheked'))
        if answer_id not in answer_cheked_list:
            answer_cheked_list.append(answer_id)
            answer_cheked_str = array_to_str(answer_cheked_list)
        else:
            to_str = []
            for ans in answer_cheked_list:
                if ans != answer_id:
                    to_str.append(ans)
            answer_cheked_str = array_to_str(to_str)
        query = {
            'table': 'user_test',
            'answer_cheked': answer_cheked_str,
            'question_id': question_id
        }
        sql_update(
            query,
            argument='user_id',
            arg_val=user_id)
    else:
        answer_cheked_str = array_to_str([answer_id])
        query_dict = {
            'table': 'user_test',
            'user_id': user_id,
            'question_id': question_id,
            'answer_cheked': answer_cheked_str,
        }
        sql_insert(query_dict)


def get_chek_answers(user_id):
    query_dict = {
        'table': 'user_test',
        'rows': [
            'user_id',
            'question_id',
            'answer_cheked'
        ]
    }
    answer_cheked = sql_select(
        query_dict,
        fetch='one',
        argument='user_id',
        arg_val=user_id
    )
    if answer_cheked[0]:
        answer_cheked_list = str_to_array(
            answer_cheked[0].get('answer_cheked'))
        return answer_cheked_list
    else:
        return []


def del_chek_answers(user_id):
    sql_delete('user_test', argument='user_id', arg_val=user_id)


def validate_answers(user_id, test=True):
    answers_cheked = get_chek_answers(user_id)
    valid_val = 'valid'
    if test:
        qid = get_user_info(user_id)[0].get('test_question_id')
    else:
        qid = get_user_info(user_id)[0].get('learn_question_id')
    if answers_cheked:
        if answers_cheked[0]:
            query_valid = {
                'table': 'answers',
                'rows': [
                    'is_true'
                ]
            }
            true_answers_query = {
                'table': 'answers',
                'rows': [
                    'id',
                ]
            }
            strarg = 'question_id = {qid} AND is_true = 1'.format(qid=qid)
            true_answers = sql_select(true_answers_query, fetch='all', str_argument=strarg)
            true_answers_list = []
            for answer in true_answers:
                true_answers_list.append(answer.get('id'))
            if len(answers_cheked) != len(true_answers_list):
                valid_val = 'invalid'
            else:
                for answer in answers_cheked:
                    is_true = sql_select(
                        query_valid,
                        fetch='one',
                        argument='id',
                        arg_val=answer)
                    if is_true[0]:
                        if is_true[0].get('is_true') == 0:
                            valid_val = 'invalid'
                            break
        else:
            valid_val = 'invalid'
    else:
        valid_val = 'error'
    return valid_val


def record_answer_story(user_id, question_id, valid):
    if valid == 'valid':
        valid = 1
    else:
        valid = 0
    cat_query_dict = {
        'table': 'questions',
        'rows': [
            'category'
        ]
    }
    cat = sql_select(
        cat_query_dict,
        fetch='one',
        argument='id',
        arg_val=question_id
    )
    if cat[0]:
        cat = cat[0].get('category')
    else:
        cat = 'Без категории'
    query_dict = {
        'table': 'main_test',
        'user_id': user_id,
        'question_id': question_id,
        'valid': valid,
        'category': cat
    }
    sql_insert(query_dict)


def del_answers_story(user_id):
    sql_delete(
        'main_test',
        argument='user_id',
        arg_val=user_id)


def chek_user_testing(user_id):
    chek_res_record = {
        'table': 'results',
        'rows': ['user_id']
    }
    chek_user = sql_select(
        chek_res_record,
        fetch='one',
        argument='user_id',
        arg_val=user_id)
    return chek_user


def result_formatter(user_id):
    get_answers = {
        'table': 'main_test',
        'rows': [
            'valid'
        ]
    }
    arg = 'user_id = {user_id} AND valid = 1'.format(
        user_id=user_id
    )
    all_valid_answers = sql_select(
        get_answers,
        fetch='all',
        str_argument=arg
    )
    all_answers = sql_select(
        get_answers,
        fetch='all',
        argument='user_id',
        arg_val=user_id
    )
    all_answers = len(all_answers)
    if all_valid_answers:
        all_valid_answers = len(all_valid_answers)
        percent_valid = round((100 / (all_answers / all_valid_answers)), 2)
        percent_valid = 100.0 - percent_valid
    else:
        percent_valid = 100.0
    get_cats_dict = {
        'table': 'questions',
        'rows': [
            'category'
        ]
    }
    cats = sql_select(get_cats_dict, fetch='all')
    cats_list = []
    for category in cats:
        cats_list.append(category.get('category'))
    cats_list = list(set(cats_list))
    query_dict = {
        'table': 'main_test',
        'rows': [
            'question_id',
            'valid',
        ]
    }
    result = [{'percent_valid': percent_valid}]
    for cat in cats_list:
        answer = sql_select(
            query_dict,
            fetch='all',
            argument='category',
            arg_val=cat)
        if answer:
            answer_count = len(answer)
            valid = 0
            for ans in answer:
                valid = valid + ans.get('valid')
            if valid:
                prc = round((100 / (answer_count / valid)), 2)
                prc = 100.0 - prc
            else:
                prc = 100.0
            result.append(
                {
                    'category': cat,
                    'answer_count': answer_count,
                    'valid': valid,
                    'valid_percent': prc
                }
            )
    chek_user = chek_user_testing(user_id)
    sres = array_to_str(result)
    if chek_user[0]:
        record_upd_query = {
            'table': 'results',
            'results': sres
        }
        sql_update(
            record_upd_query,
            argument='user_id',
            arg_val=user_id)
    else:
        record_result_query = {
            'table': 'results',
            'user_id': user_id,
            'results': sres
        }
        sql_insert(record_result_query)
    del_answers_story(user_id)
    return result


def get_user_results(user_id):
    query_dict = {
        'table': 'results',
        'rows': [
            'results'
        ]
    }
    results = sql_select(
        query_dict,
        fetch='one',
        argument='user_id',
        arg_val=user_id
    )
    results = str_to_array(results[0].get('results'))
    return results
