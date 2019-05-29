# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from lng_fn import lng
from tester_utils import (answers_getter, chek_answer, delete_chek_answers,
                          delete_rec_question_user, delete_test_history,
                          get_all_questions, get_answer_status,
                          get_chek_answers, get_last_user_question_id,
                          get_question, rec_last_question, rec_test_history,
                          revision_answers, revision_test_answers,
                          upd_chek_answers, view_result)

# telegram bot api
bot = telebot.TeleBot(config.token)


def tester_menu(message=None, c=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('questions_hi_text')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('learn_mnu_btn'),
            callback_data='learn)1'
        ),
        types.InlineKeyboardButton(
            text=lng(user_id).get('test_mnu_btn'),
            callback_data='test)1)0'
        )
    )
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def test(c, question_number=1, answer_id=None):
    user_id = c.from_user.id
    if question_number > len(get_all_questions()):
        result = revision_test_answers(user_id)
        ans_text = lng(user_id).get('test_end_text').format(
            rcount=result.get('right'),
            wcount=result.get('whrong')
        )
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True)
        tester_menu(c=c)
    else:
        question = get_question(question_number)
        answers = answers_getter(user_id, question_number)
        answers_text = ''
        count = 1
        for answer in answers:
            answers_text += '<b>' + str(count) + '</b> - ' + answer.get('question') + '\n'
            count += 1
        mes_text = lng(user_id).get('learn_question').format(
            qnum=question_number,
            question=question.get('question'),
            answers=answers_text
        )
        if answer_id:
            status = get_answer_status(user_id, question_number, answer_id)
            if status == 'nocheked':
                upd_chek_answers(
                    user_id,
                    question_number,
                    answer_id,
                    'cheked')
            else:
                upd_chek_answers(
                    user_id,
                    question_number,
                    answer_id,
                    'nocheked')
        answer_list = get_chek_answers(user_id, question_number)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(
            text=lng(user_id).get('answer_btn').format(
                number=answer.get('answer_number'),
                chk=lng(user_id).get(answer.get('cheked'))),
            callback_data='test)' + str(question_number) + ')' + str(answer.get('answer_id'))) for answer in answer_list])
        if answer_id:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='testmenu'),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('next_learn_question_btn'),
                    callback_data='rec_test_answer-' + str(question_number))
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='testmenu')
            )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def rec_test_answer(c, question_id):
    user_id = c.from_user.id
    result = revision_answers(user_id, question_id)
    rec_test_history(user_id, question_id, result)


def learn(c, question_number=1, toret=None):
    user_id = c.from_user.id
    delete_rec_question_user(user_id)
    delete_chek_answers(user_id)
    question = get_question(question_number)
    mes_text = lng(user_id).get('question_learn').format(
        qnum=question_number,
        category=question.get('category'),
        paragraph=question.get('paragraph')
    )
    keyboard = types.InlineKeyboardMarkup()
    if question_number > len(get_all_questions()):
        ans_text = lng(user_id).get('learn_end_text')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True)
        tester_menu(c=c)
    else:
        if toret:
            question_number += 1
            if question_number > len(get_all_questions()):
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='testmenu'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('test_question'),
                        callback_data='lquestion)' + str(question_number) + ')0)nocheked'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('end_learn_question_btn'),
                        callback_data='testmenu'
                    )
                )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('back_p'),
                        callback_data='testmenu'
                    ),
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('test_question'),
                        callback_data='lquestion)' + str(question_number) + ')0)nocheked'
                    )
                )
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lng(user_id).get('next_learn_question_btn'),
                        callback_data='learn)' + str(question_number)
                    )
                )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='testmenu'
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('test_question'),
                    callback_data='lquestion)' + str(question_number) + ')0)nocheked'
                )
            )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def learn_question(c, question_number=1, answer_id=None):
    user_id = c.from_user.id
    question = get_question(question_number)
    answers = answers_getter(user_id, question_number)
    answers_text = ''
    count = 1
    for answer in answers:
        answers_text += '<b>' + str(count) + '</b> - ' + answer.get('question') + '\n'
        count += 1
    mes_text = lng(user_id).get('learn_question').format(
        qnum=question_number,
        question=question.get('question'),
        answers=answers_text
    )
    if answer_id:
        status = get_answer_status(user_id, question_number, answer_id)
        if status == 'nocheked':
            upd_chek_answers(
                user_id,
                question_number,
                answer_id,
                'cheked')
        else:
            upd_chek_answers(
                user_id,
                question_number,
                answer_id,
                'nocheked')
    answer_list = get_chek_answers(user_id, question_number)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(
        text=lng(user_id).get('answer_btn').format(
            number=answer.get('answer_number'),
            chk=lng(user_id).get(answer.get('cheked'))),
        callback_data='lquestion)' + str(question_number) + ')' + str(answer.get('answer_id'))) for answer in answer_list])
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('test_chek_answer_btn'),
            callback_data='chek_learn_answer-' + str(question_number)
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('back_p'),
            callback_data='testmenu'
        )
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def chek_learn_answer(c, question_number):
    user_id = c.from_user.id
    result = revision_answers(user_id, question_number)
    right_answers = result[0].get('right_answers')
    whrong_answers = result[0].get('whrong_answers')
    if len(right_answers):
        if len(whrong_answers):
            if len(whrong_answers) < 2:
                chk_question_number = question_number + 1
                if chk_question_number > len(get_all_questions()):
                    ans_text = lng(user_id).get('soso_learn_text_no_next_question')
                else:
                    ans_text = lng(user_id).get('soso_learn_text')
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                learn(c, question_number=question_number, toret=1)
            else:
                ans_text = lng(user_id).get('whrong_learn_text')
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                learn(c, question_number=question_number)
        else:
            question_number += 1
            if question_number > len(get_all_questions()):
                ans_text = lng(user_id).get('right_learn_text_learn_end')
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                tester_menu(c=c)
            else:
                ans_text = lng(user_id).get('right_learn_text')
                bot.answer_callback_query(
                    c.id,
                    text=ans_text,
                    show_alert=True)
                learn(c, question_number=question_number)
    else:
        ans_text = lng(user_id).get('whrong_learn_text')
        bot.answer_callback_query(
            c.id,
            text=ans_text,
            show_alert=True)
        learn(c, question_number=question_number)


def user_tester_menu(message=None, c=None):
    if c:
        user_id = c.from_user.id
    else:
        user_id = message.from_user.id
    mes_text = lng(user_id).get('user_tester_menu_text')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Вводный курс',
            callback_data='обучение_приветствие'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=lng(user_id).get('to_menu_btn'),
            callback_data='MENU'
        )
    )
    if message:
        bot.send_message(
            message.chat.id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def user_choose_learn_curs(c, curs_id=None):
    user_id = c.from_user.id
    delete_rec_question_user(user_id)
    delete_chek_answers(user_id)
    delete_test_history(user_id)
    if curs_id:
        pass
    else:
        mes_text = lng(user_id).get('questions_hi_text')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('back_p'),
                callback_data='обучение'
            ),
            types.InlineKeyboardButton(
                text=lng(user_id).get('letsgo_btn'),
                callback_data='обучалка-0-0'
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=lng(user_id).get('to_menu_btn'),
                callback_data='MENU'
            )
        )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)


def user_learn(c, question_id, answer_id=None):
    user_id = c.from_user.id
    if question_id:
        rec_last_question(user_id, question_id)
    else:
        question_id = get_last_user_question_id(user_id)
    question = get_question(question_id)
    keyboard = types.InlineKeyboardMarkup()
    if question_id > len(get_all_questions()):
        chek = True
        if answer_id:
            cheked = chek_answer(question_id, answer_id)
            if cheked.get('right_answers'):
                chek = True
            else:
                chek = False
            rec_test_history(user_id, question_id, cheked)
        if chek:
            mes_text = lng(user_id).get('end_lerning_message').format(
                result_text=lng(user_id).get('good_learn_text')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('test_mnu_btn'),
                    callback_data='тестирование*1*0'
                )
            )
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            question = get_question(question_id - 1)
            ans_text = lng(user_id).get('whrong_learn_text')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            mes_text = lng(user_id).get('learn_paragraph_text').format(
                paragraph=question.get('paragraph')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('test_question'),
                    callback_data='проверка=' + str(question_id - 1)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                )
            )
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
    else:
        chek = True
        if answer_id:
            cheked = chek_answer(question_id, answer_id)
            if cheked.get('right_answers'):
                chek = True
            else:
                chek = False
            rec_test_history(user_id, question_id, cheked)
        if chek:
            mes_text = lng(user_id).get('learn_paragraph_text').format(
                paragraph=question.get('paragraph')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('test_question'),
                    callback_data='проверка=' + str(question_id)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                )
            )
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            question = get_question(question_id - 1)
            ans_text = lng(user_id).get('whrong_learn_text')
            bot.answer_callback_query(
                c.id,
                text=ans_text,
                show_alert=True)
            mes_text = lng(user_id).get('learn_paragraph_text').format(
                paragraph=question.get('paragraph')
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('test_question'),
                    callback_data='проверка=' + str(question_id - 1)
                )
            )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                )
            )
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)


def chek_user_learn(c, question_id):
    user_id = c.from_user.id
    answers = answers_getter(user_id, question_id)
    question = get_question(question_id)
    mes_text = lng(user_id).get('test_question_menu_text').format(
        question=question.get('question')
    )
    keyboard = types.InlineKeyboardMarkup()
    for answer in answers:
        keyboard.add(
            types.InlineKeyboardButton(
                text=answer.get('question'),
                callback_data='обучалка-' + str(question_id + 1) + '-' + str(answer.get('answer_id'))
            )
        )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def user_get_test(c, question_id=1, answer_id=None):
    user_id = c.from_user.id
    if question_id > len(get_all_questions()):
        result = view_result(user_id)
        mes_text = lng(user_id).get('end_test_and_results_text').format(
            results=result.get('result')
        )
        keyboard = types.InlineKeyboardMarkup()
        if result.get('wcount') > 1:
            mes_text = mes_text + lng(user_id).get('bad_test_text')
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('relearn_btn'),
                    callback_data='learn)1'
                ),
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                )
            )
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=lng(user_id).get('back_p'),
                    callback_data='обучение_приветствие'
                )
            )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        user_id = c.from_user.id
        if answer_id:
            cheked = chek_answer(question_id, answer_id)
            rec_test_history(user_id, question_id, cheked)
        answers = answers_getter(user_id, question_id)
        question = get_question(question_id)
        mes_text = lng(user_id).get('test_question_menu_text').format(
            question=question.get('question')
        )
        keyboard = types.InlineKeyboardMarkup()
        for answer in answers:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=answer.get('question'),
                    callback_data='тестирование*' + str(question_id + 1) + '*' + str(answer.get('answer_id'))
                )
            )
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
