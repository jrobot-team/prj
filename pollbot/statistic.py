# -*- coding: utf-8 -*-
import xlsxwriter

from bot_utilites import (Basedate, get_chat_arch_messages, get_chat_info,
                          get_poll_info, get_poll_user_stat, get_users,
                          pollstat_sorter, user_info)


def create_stata_file(pollid):
    sfile = 'stata/' + str(pollid) + '_poll.xlsx'
    pollname = get_poll_info(pollid)[0]
    pollstatainfo = pollstat_sorter(pollid)
    pcount = pollstatainfo[2]
    choises = pollstatainfo[0]
    poll_user_stat = get_poll_user_stat(pollid)
    workbook = xlsxwriter.Workbook(sfile)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:B', 15)
    worksheet.set_column('C:D', 20)
    worksheet.set_column('E:E', 2)
    worksheet.set_column('F:F', 20)
    worksheet.set_column('G:G', 15)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'Username', bold)
    worksheet.write('C1', 'ФИО', bold)
    worksheet.write('D1', 'Вариант', bold)
    worksheet.write('F1', 'Название', bold)
    worksheet.write('F2', pollname)
    worksheet.write('F3', 'Варианты ответов', bold)
    worksheet.write('G3', 'Проценты', bold)
    worksheet.write('G1', 'Проголосовало', bold)
    worksheet.write('G2', pcount)
    count = 4
    usercount = 2
    for choise in choises:
        prc = choise.get('percent')
        var = choise.get('var')
        worksheet.write('F' + str(count), var)
        worksheet.write('G' + str(count), prc)
        count += 1
    for user in poll_user_stat:
        user_id = user[0]
        var = ''
        for choise in choises:
            if choise.get('num') == user[1]:
                var = choise.get('var')
        userinfo = user_info(user_id)
        worksheet.write('A' + str(usercount), user_id)
        if userinfo:
            worksheet.write('B' + str(usercount), userinfo[0])
            worksheet.write('C' + str(usercount), userinfo[1])
        else:
            worksheet.write('B' + str(usercount), 'Супер администратор')
        worksheet.write('D' + str(usercount), var)
        usercount += 1
    workbook.close()


def create_arch_chat_messages_file(chatid):
    sfile = 'chat_msgs/' + str(chatid) + '_msgs.xlsx'
    chatinfo = get_chat_info(chatid)
    msgs = get_chat_arch_messages(chatid)
    workbook = xlsxwriter.Workbook(sfile)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:B', 15)
    worksheet.set_column('C:D', 30)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'Username', bold)
    worksheet.write('C1', 'ФИО', bold)
    worksheet.write('D1', 'Сообщение', bold)
    worksheet.write('E1', chatinfo.get('chat_name'), bold)
    usercount = 2
    for msg in msgs:
        userinfo = user_info(msg.get('user_id'))
        worksheet.write('A' + str(usercount), msg.get('user_id'))
        if userinfo:
            worksheet.write('B' + str(usercount), userinfo[0])
            worksheet.write('C' + str(usercount), userinfo[1])
        else:
            worksheet.write('B' + str(usercount), 'Супер администратор')
        worksheet.write('D' + str(usercount), msg.get('message'))
        usercount += 1
    workbook.close()


def create_users_file():
    date = Basedate().date_hms()
    sfile = 'export_users/' + str(date) + '_users.xlsx'
    workbook = xlsxwriter.Workbook(sfile)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:B', 15)
    worksheet.set_column('C:D', 30)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'Username', bold)
    worksheet.write('C1', 'ФИО', bold)
    worksheet.write('D1', 'Роль', bold)
    worksheet.write('E1', 'Дата регистрации', bold)
    usercount = 2
    users = get_users()
    for user in users:
        userinfo = user_info(user[0])
        worksheet.write('A' + str(usercount), user[0])
        if userinfo:
            worksheet.write('B' + str(usercount), userinfo[0])
            worksheet.write('C' + str(usercount), userinfo[1])
            worksheet.write('D' + str(usercount), userinfo[2])
            if userinfo[9]:
                worksheet.write('E' + str(usercount), userinfo[9])
            else:
                worksheet.write('E' + str(usercount), '2019-03-01')
        else:
            worksheet.write('B' + str(usercount), 'Супер администратор')
        usercount += 1
    workbook.close()
    return date
