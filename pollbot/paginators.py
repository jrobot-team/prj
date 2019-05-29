# -*- coding: utf-8 -*-
from config import pagelimit


def paginator(array, page, limit=pagelimit):
    """
    Принимает массив и страницу
    возвращает массив страницу обрезанную на лимит отображения
    (данная настройка или передается напрямую в функцию
    или берется из конфига)
    """
    if array:
        try:
            if page == 1:
                array = array[:limit]
            else:
                start = limit * (int(page) - 1)
                stop = limit + start
                array = array[start:stop]
        except Exception as e:
            print(e)
            print('paginator error')
            array = []
    else:
        array = []
    return array
