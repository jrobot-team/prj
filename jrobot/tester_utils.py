# -*- coding: utf-8 -*-
import random

from bot_utils import array_to_str, str_to_array
from dbclasses import (LastQuestion, Question, QuestionUserRec, TestHistory,
                       UserAnswers)


def get_question(question_id):
    try:
        question = {
            'id': question_id,
            'category': Question.get(Question.id == question_id).category,
            'paragraph': Question.get(Question.id == question_id).paragraph,
            'question': Question.get(Question.id == question_id).question,
            'right_answer': Question.get(Question.id == question_id).right_answer,
            'right_true': Question.get(Question.id == question_id).right_true,
            'whrong_answers': str_to_array(Question.get(Question.id == question_id).whrong_answers),
        }
    except:
        question = None
    return question


def chek_answer(question_id, answer_id):
    question_id = question_id - 1
    question = get_question(question_id)
    whrong_answers = question.get('whrong_answers')
    wids = []
    for ans in whrong_answers:
        wids.append(
            ans.get('id')
        )
    if answer_id in wids:
        response = {
            'right_answers': [],
            'whrong_answers': [answer_id]
        }
    else:
        response = {
            'right_answers': [answer_id],
            'whrong_answers': []
        }
    return response


def get_all_questions():
    quesions = []
    query = Question.select()
    for question in query:
        quesions.append(
            {
                'category': question.category,
                'paragraph': question.paragraph,
                'question': question.question,
                'right_answer': question.right_answer,
                'right_true': question.right_true,
                'whrong_answers': question.whrong_answers
            }
        )
    return quesions


def get_question_user_rec(user_id, question_id):
    try:
        question = {
            'answers': str_to_array(
                QuestionUserRec.get(
                    QuestionUserRec.user_id == user_id,
                    QuestionUserRec.question_id == question_id).answers)
        }
    except:
        question = None
    return question


def rec_question_user(user_id, question_id, answers):
    QuestionUserRec.create(
        user_id=user_id,
        question_id=question_id,
        answers=array_to_str(answers)
    )


def get_last_user_question_id(user_id):
    try:
        last_question_id = LastQuestion.get(
            LastQuestion.user_id == user_id
        ).question_id
    except:
        last_question_id = 1
    return last_question_id


def rec_last_question(user_id, question_id):
    last_question_id = get_last_user_question_id(user_id)
    if last_question_id:
        LastQuestion.update(
            question_id=question_id
        ).where(LastQuestion.user_id == user_id).execute()
    else:
        LastQuestion.create(
            user_id=user_id,
            question_id=question_id
        )


def delete_rec_question_user(user_id):
    QuestionUserRec.delete().where(QuestionUserRec.user_id == user_id).execute()


def answers_getter(user_id, question_id):
    answers_record = get_question_user_rec(user_id, question_id)
    if answers_record:
        return answers_record.get('answers')
    else:
        question = get_question(question_id)
        answers = question.get('whrong_answers')
        answers.append(
            {
                'id': len(answers) + 1,
                'question': question.get('right_answer'),
                'status': 1
            }
        )
        ans_list = []
        for answer in answers:
            ans_list.append(
                {
                    'question_id': question_id,
                    'question': answer.get('question'),
                    'answer_id': answer.get('id'),
                    'status': answer.get('status'),
                }
            )
        random.shuffle(ans_list)
        rec_question_user(user_id, question_id, ans_list)
        answers_record = get_question_user_rec(user_id, question_id).get('answers')
        return answers_record


def make_chek_answers(user_id, question_id, answers):
    delete_chek_answers(user_id)
    UserAnswers.create(
        user_id=user_id,
        question_id=question_id,
        answers=answers
    )


def get_chek_answers(user_id, question_id):
    try:
        answers = UserAnswers.get(
            UserAnswers.user_id == user_id,
            UserAnswers.question_id == question_id).answers
        answers = str_to_array(answers)
    except:
        answers = []
        resp_answers = answers_getter(user_id, question_id)
        count = 1
        for ans in resp_answers:
            answers.append(
                {
                    'answer_number': count,
                    'answer_id': ans.get('answer_id'),
                    'cheked': 'nocheked'
                }
            )
            count += 1
        answers = array_to_str(answers)
        make_chek_answers(user_id, question_id, answers)
        try:
            answers = UserAnswers.get(
                UserAnswers.user_id == user_id,
                UserAnswers.question_id == question_id).answers
            answers = str_to_array(answers)
        except:
            answers = None
    return answers


def upd_chek_answers(user_id, question_id, answer_id, status):
    answers = get_chek_answers(user_id, question_id)
    newlist = []
    for answer in answers:
        if answer.get('answer_id') == answer_id:
            newlist.append(
                {
                    'answer_number': answer.get('answer_number'),
                    'answer_id': answer_id,
                    'cheked': status
                }
            )
        else:
            newlist.append(
                answer
            )
    newlist = array_to_str(newlist)
    UserAnswers.update(answers=newlist).where(
        UserAnswers.user_id == user_id,
        UserAnswers.question_id == question_id).execute()


def get_answer_status(user_id, question_id, answer_id):
    answers = get_chek_answers(user_id, question_id)
    status = 'nocheked'
    for answer in answers:
        if answer.get('answer_id') == answer_id:
            status = answer.get('cheked')
    return status


def delete_chek_answers(user_id):
    UserAnswers.delete().where(UserAnswers.user_id == user_id).execute()


def revision_answers(user_id, question_id):
    answers_cheked = get_chek_answers(user_id, question_id)
    answers = answers_getter(user_id, question_id)
    right_answers = []
    whrong_answers = []
    result = []
    for answer in answers:
        for ans in answers_cheked:
            if answer.get('answer_id') == ans.get('answer_id'):
                if answer.get('status'):
                    if ans.get('cheked') == 'cheked':
                        right_answers.append(answer.get('answer_id'))
                else:
                    if ans.get('cheked') == 'cheked':
                        whrong_answers.append(answer.get('answer_id'))
    result.append(
        {
            'right_answers': right_answers,
            'whrong_answers': whrong_answers
        }
    )
    return result


def rec_test_history(user_id, question_id, answer):
    try:
        answers = TestHistory.get(
            TestHistory.user_id == user_id,
            TestHistory.question_id == question_id).answers
    except:
        answers = None
    answer = array_to_str(answer)
    if answers:
        TestHistory.update(answers=answer).where(
            TestHistory.user_id == user_id,
            TestHistory.question_id == question_id
        ).execute()
    else:
        TestHistory.create(
            user_id=user_id,
            question_id=question_id,
            answers=answer
        )


def delete_test_history(user_id):
    TestHistory.delete().where(TestHistory.user_id == user_id).execute()


def revision_test_answers(user_id):
    query = TestHistory.select().where(TestHistory.user_id == user_id)
    answers = []
    for answer in query:
        answers.append(
            {
                'question_id': answer.question_id,
                'answers': answer.answers
            }
        )
    right = []
    whrong = []
    rcount = 0
    wcount = 0
    for answer in answers:
        result = str_to_array(answer.get('answers'))
        right.append(result.get('right_answers'))
        whrong.append(result.get('whrong_answers'))
    for rans in right:
        if rans:
            rcount += 1
    for wans in whrong:
        if wans:
            wcount += 1
    res = {
        'right': rcount,
        'whrong': wcount
    }
    return res


def view_result(user_id):
    query = TestHistory.select().where(TestHistory.user_id == user_id)
    answers = []
    for answer in query:
        answers.append(
            {
                'question_id': answer.question_id - 1,
                'answers': answer.answers
            }
        )
    result = 'Неправильные ответы в вопросах:\n---------------------\n'
    count = 0
    for ans in answers:
        question = get_question(ans.get('question_id'))
        if str_to_array(ans.get('answers')).get('whrong_answers'):
            result += '<b>' + question.get('question') + '</b>\n'
            count += 1
    if count:
        return {'result': result, 'wcount': count}
    else:
        return {'result': 'Вы успешно прошли тестирование, и ответили на все вопросы правильно', 'wcount': count}
