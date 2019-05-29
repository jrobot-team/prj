# -*- coding: utf-8 -*-
import telebot
from telebot import types

import config
from botutils import (Basedate, answers_formatter, chek_answer,
                      chek_user_testing, del_answers_list, del_chek_answers,
                      get_chek_answers, get_question, get_user_info,
                      get_user_results, questions_count, reg_user,
                      result_formatter, upd_user_learn_question_id,
                      upd_user_test_question_id)
from lang import ru

# telegram bot api
bot = telebot.TeleBot(config.TOKEN)


def start_menu(message=False, c=False):
    if message:
        user_id = message.from_user.id
        username = message.from_user.first_name
    else:
        user_id = c.from_user.id
        username = c.from_user.first_name
    keyboard = types.InlineKeyboardMarkup()
    userinfo = get_user_info(user_id)
    if userinfo[0]:
        if userinfo[0].get('register'):
            test_count = get_user_info(user_id)[0].get('test_count')
            del_answers_list(user_id)
            del_chek_answers(user_id)
            if chek_user_testing(user_id)[0]:
                res = get_user_results(user_id)
                test_prc = res[0].get('percent_valid')
                res = res[1:]
                catres = ''
                for test in res:
                    catres = catres + ru.get('cat_res').format(
                        cat=test.get('category'),
                        prc=test.get('valid_percent'))
                mes_text = ru.get('res_test_message').format(
                    result_prc=test_prc,
                    cat_res=catres)
            else:
                mes_text = ru.get('menu_message').format(
                    test_count=test_count)
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('learn_btn'),
                    callback_data='learn'),
                types.InlineKeyboardButton(
                    text=ru.get('test_btn'),
                    callback_data='prepare_your_anus'))
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('reg_btn'),
                    callback_data='register'))
            mes_text = ru.get('hi_message').format(
                username=username)
    else:
        reg_user(user_id, username)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('reg_btn'),
                callback_data='register'))
        mes_text = ru.get('hi_message').format(
            username=username)
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


def start_learn_menu(c):
    user_id = c.from_user.id
    del_chek_answers(user_id)
    del_answers_list(user_id)
    q_count = questions_count()
    question_id = get_user_info(user_id)[0].get('learn_question_id')
    if question_id > q_count:
        upd_user_learn_question_id(user_id, 0)
        mes_text = ru.get('learn_end')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('re_learn_btn'),
                callback_data='learn'),
            types.InlineKeyboardButton(
                text=ru.get('test_btn'),
                callback_data='prepare_your_anus'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_to_menu_btn'),
                callback_data='menu'))
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text=mes_text,
            parse_mode='html',
            reply_markup=keyboard)
    else:
        question = get_question(question_id)[0]
        if question[0].get('paragraf'):
            mes_text = ru.get('learn_question_message').format(
                num_q=question[0].get('id'),
                q_count=q_count,
                paragraf=question[0].get('paragraf'))
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=ru.get('test_question_btn'),
                    callback_data='learn_test_question-0'),
                types.InlineKeyboardButton(
                    text=ru.get('back_to_menu_btn'),
                    callback_data='menu'))
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=mes_text,
                parse_mode='html',
                reply_markup=keyboard)
        else:
            learn_test_question(c, 0)


def learn_test_question(c, answer_id):
    date = Basedate().date_hms()
    user_id = c.from_user.id
    question_id = get_user_info(user_id)[0].get('learn_question_id')
    question = get_question(question_id)[0][0].get('question')
    if answer_id:
        ans_text, ans_list = answers_formatter(user_id, question_id, rnd=False)
    else:
        ans_text, ans_list = answers_formatter(user_id, question_id)
    chek_answers_list = get_chek_answers(user_id)
    if answer_id:
        for ans in ans_list:
            if ans[1] == answer_id:
                if ans[1] not in chek_answers_list:
                    ans[2] = 'cheked'
                    chek_answer(
                        user_id,
                        question_id,
                        answer_id)
                    chek_answers_list = get_chek_answers(user_id)
                else:
                    chek_answer(
                        user_id,
                        question_id,
                        answer_id)
                    chek_answers_list = get_chek_answers(user_id)
    for ans in ans_list:
        if ans[1] in chek_answers_list:
            ans[2] = 'cheked'
    mes_text = ru.get('learn_question_test').format(
        date=date,
        num_q=get_question(question_id)[0][0].get('id'),
        q_count=questions_count(),
        question=question,
        answers=ans_text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(
        text=ru.get('answer_btn').format(
            number=answer[0],
            chk=ru.get(answer[2])),
        callback_data='learn_test_question-' + str(answer[1])) for answer in ans_list])
    keyboard.add(
        types.InlineKeyboardButton(
            text=ru.get('test_chek_answer_btn'),
            callback_data='chek_answer'),
        types.InlineKeyboardButton(
            text=ru.get('back_to_menu_btn'),
            callback_data='menu'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)


def test_question(c, answer_id):
    user_id = c.from_user.id
    q_count = questions_count()
    question_id = get_user_info(user_id)[0].get('test_question_id')
    keyboard = types.InlineKeyboardMarkup()
    if question_id > q_count:
        upd_user_test_question_id(user_id, 0)
        res = result_formatter(user_id)
        test_prc = res[0].get('percent_valid')
        res = res[1:]
        catres = ''
        for test in res:
            catres = catres + ru.get('cat_res').format(
                cat=test.get('category'),
                prc=test.get('valid_percent'))
        if test_prc < 75.0:
            end_message = ru.get('no_good_test')
        else:
            end_message = ru.get('good_test')
        mes_text = ru.get('end_test_message').format(
            result_prc=test_prc,
            cat_res=catres,
            end_message=end_message)
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('re_learn_btn'),
                callback_data='learn'),
            types.InlineKeyboardButton(
                text=ru.get('retest_btn'),
                callback_data='prepare_your_anus'))
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('back_to_menu_btn'),
                callback_data='menu'))
    else:
        date = Basedate().date_hms()
        question = get_question(question_id)[0][0].get('question')
        if answer_id:
            ans_text, ans_list = answers_formatter(user_id, question_id, rnd=False)
        else:
            ans_text, ans_list = answers_formatter(user_id, question_id)
        chek_answers_list = get_chek_answers(user_id)
        if answer_id:
            for ans in ans_list:
                if ans[1] == answer_id:
                    if ans[1] not in chek_answers_list:
                        ans[2] = 'cheked'
                        chek_answer(
                            user_id,
                            question_id,
                            answer_id)
                        chek_answers_list = get_chek_answers(user_id)
                    else:
                        chek_answer(
                            user_id,
                            question_id,
                            answer_id)
                        chek_answers_list = get_chek_answers(user_id)
        for ans in ans_list:
            if ans[1] in chek_answers_list:
                ans[2] = 'cheked'
        mes_text = ru.get('learn_question_test').format(
            date=date,
            num_q=get_question(question_id)[0][0].get('id'),
            q_count=questions_count(),
            question=question,
            answers=ans_text)
        keyboard.add(*[types.InlineKeyboardButton(
            text=ru.get('answer_btn').format(
                number=answer[0],
                chk=ru.get(answer[2])),
            callback_data='question_test-' + str(answer[1])) for answer in ans_list])
        keyboard.add(
            types.InlineKeyboardButton(
                text=ru.get('next_q'),
                callback_data='chekanswertest'),
            types.InlineKeyboardButton(
                text=ru.get('back_to_menu_btn'),
                callback_data='menu'))
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=mes_text,
        parse_mode='html',
        reply_markup=keyboard)
