from django.test import TestCase
import re
from datetime import datetime
import time

# Create your tests here.
any_time = 1692894781.4534788
# str_time = 'Thu Aug 24 22:21:41 2023'
# str_time = 'Aug  24  - 23 __ 02:27:31  Wed'
# str_time = '24-03-23 23:46:58'
str_time = '2023-08-26 23:37:52.209301'
# !!! форматы даты/времени в именах файлов на телефонах/фотоаппаратах!
time_list = [12, 20, 48, 23, 48, 2]
# str_time = 'DSC000271-270823-230014'
vis = 'str'  # any/datetime/list

# немного из попыток:
# print(humdate)
# print(datetime.strptime(tm_var, "%H"))
# deadline = datetime.strptime("22/05/2017", "%d/%m/%Y")
# print(deadline)     # 2017-05-22 00:00:00
#
# deadline = datetime.strptime("22/05/2017 12:30", "%d/%m/%Y %H:%M")
# print(deadline)     # 2017-05-22 12:30:00
#
# deadline = datetime.strptime("05-22-2017 12:30", "%m-%d-%Y %H:%M")
# print(deadline)     # 2017-05-22 12:30:00

# print(time.ctime(1384112639)) # 'Sun Nov 10 13:43:59 2013'
# a = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
# print(a) # '2017-04-05-00.11.20'


def restruct_datetime(in_var):
    """Функция для преобразования даты/времени (в именах тоже) в заданный пользователем формат. Например, менять место
    указания года, менять его форму представления (4/2 знака), выводить месяц в виде числа или в сокращении на указанном
    языке (Ru/En).
     Может принимать как стандартные для Python форматы, так и используемые в именах файлов (снимки, например).
    Если формат нестандартный, тогда рекомендуется указывать список, где первое значение - сама строка символов, а
    вторым его маска ("N Y-M-D h:m:s (W)")"""
    time_string = ''
    if type(in_var) is float:  # 1692894781.4534788
        time_string = time.ctime(in_var)
        print('input type = "float" >>>', time_string, '<<<')
    elif type(in_var) is str:
        time_string = in_var
        print('input type = "string" >>>', time_string, '<<<')
    elif str(type(in_var)) == "<class 'datetime.datetime'>":
        time_string = str(in_var)
        print('input type = "datetime" >>>', time_string, '<<<')
    elif str(type(in_var)) is list:
        time_string = in_var[0]
        input_mask = in_var[1]
        print(in_var)
    else:
        return 'Unknow format'
    t_s = ':'  # разделитель времени
    if time_string.count(t_s) < 2:
        print('_!!!_ Time used another seperator, but ":"')

    # должен понимать странные форматы питона и YYYY-MM-DD hh:mm:ss
    # при использовании разделителей, не обязательно указывать YYYY-MM-DD, достаточно Y-M-D, если год явно указан
    # 4-мя знаками
    # переводить названия месяцев/дней недели (пока просто выбрасывать) в числа
    output_mask = "N-n-Y-M-D h:m:s (W) Dig"  # соответствие параметров в разбираемой строке с выходной
    # форматирование "формата" вывода: YYYYYY - больше 4 и ограничивается 4, YYY - менее 4 и ограничивается 2
    # заглавными - Имя (N) (txt), год (Y) (dig), месяц (M) (dig/txt), день (D) (dig), день недели (W) (txt)
    # прописными - час (h) (dig), минуты (m) (dig), секунды (s) (dig), доли секунд (u) (dig)
    # разделение "*"-ми ( YY*M*D h*m*s*(W) )- вернуть с оригинальными разделителями, что делать если для нужного их нет?
    # (поиск в input_mask), YY - для только двух цифр года...
    # Месяц и день приводить к краткому виду? Задание DDD не приводит к виду 003, число знаков не более 2, а на
    # текстовый формат вывода (месяца, например) вообще не влияет
    # (!!! проверка параметров при считывании маски и формы вывода !!)
    # Rus/Eng/Dig - взаимоисключающие, Rus - перевод текстовых полей на русский, Dig - замена текстовых полей численными
    if 'Rus' in output_mask:
        output_code = 'Rus'  # при output_num = 1 не имеет значения
    elif 'Eng' in output_mask:
        output_code = 'Eng'
    elif 'Dig' in output_mask:
        output_code = 'Digital'
    months_list = [['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'],
                   ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']]
    dow_list = [['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']]
    out_string = ''

    # if autoindent == 1
    # ручная разборка строки
    cur_pre_sep = '"'
    par_pos = 0
    new_flag = 1
    var_list = []  # структура: [['значение', 'разделитель до', 'разделитель после', 'чем является'], [], [], []]
    for c_cou in time_string:  # поиск разделителей и сборка кусков (только буквы и цифры)
        if new_flag:
            var_list.append(['', cur_pre_sep, '"', ''])
            new_flag = 0
        if c_cou.isalpha() or c_cou.isdigit():
            var_list[par_pos][0] += c_cou
        else:  # найден разделитель (не число и не буква)
            cur_pre_sep = c_cou
            if var_list[par_pos][0]:  # если при этом строка не пустая (не дубликат разделителя)
                var_list[par_pos][2] = c_cou
                par_pos += 1
                new_flag = 1
    # print(var_list)
    # для имен файлов анализ групп кратный 2 (?), например: 8 знаков - вероятно с годом, 6 - вероятно время, проверка на
    # эти параметры, если не укладывается, то вероятно это номер
    # если указан год, то это число, 4 знака и значение (int) > ?1000
    err_list = []
    for d_cou in var_list:  # обработка найденных значений
        if d_cou[0].isalpha():
            if d_cou[0] in months_list[0] or d_cou[0] in months_list[1]:
                d_cou[3] = 'M'
            elif d_cou[0] in dow_list[0] or d_cou[0] in dow_list[1]:
                d_cou[3] = 'W'
            else:
                d_cou[3] = '?t'
                err_list.append('unknow text')

        elif d_cou[0].isdigit():
            if d_cou[1] != t_s and d_cou[2] != t_s and d_cou[1] != '.':  # не окружен разделителями времени
                # год - 4 цифры - > 1983 <= текущего
                # год - 2 цифры - 83-99 или 00-текущий + ? нужна ли конвертация в 4-х значный (наверное только при Y)?
                if int(d_cou[0]) > 31:
                    d_cou[3] = 'Y'
                elif int(d_cou[0]) > 12:
                    d_cou[3] = 'D'
                elif int(d_cou[0]) <= 12:
                    d_cou[3] = 'M'
                else:
                    d_cou[3] = f'?D{d_cou[0]}'
                    err_list.append('unknow date')
            elif d_cou[1] == t_s and d_cou[2] == t_s:
                if int(d_cou[0]) < 60:
                    d_cou[3] = 'm'
                else:
                    d_cou[3] = '?m'
                    err_list.append('wrong minutes')
            elif d_cou[1] != t_s and d_cou[2] == t_s:
                if int(d_cou[0]) < 24:
                    d_cou[3] = 'h'
                else:
                    d_cou[3] = '?h'
                    err_list.append('wrong hours')
            elif d_cou[1] == t_s and d_cou[2] != t_s:
                if int(d_cou[0]) < 60:
                    d_cou[3] = 's'
                else:
                    d_cou[3] = '?s'
                    err_list.append('wrong seconds')
            elif d_cou[1] == '.' and d_cou[0].isdigit():
                # print(d_cou[0])
                d_cou[3] = 'u'
            else:
                print('\nHZ\n')
        else:  # это сепараторы и при формировании списка исключаются!
            print('Program ERROR!!')
            d_cou[3] = '?,,,?'
            err_list.append('wtf?')
    print(var_list)

    # Пересборка даты:
    # месяц в число
    # проверка чисел на граничные значения (год > 31, месяц <= 12, число <= 31, часы <= 23, минуты <= 59, секунды <= 59)
    # идентификация по строковым маркерам (названия месяцев и дней недели).
    # print(var_list)
    input_mask = ''.join([tmp[3] for tmp in var_list])
    print('find input_mask: ', input_mask, ' Errors:', str(err_list))
    print('    Output_mask: ', output_mask)

    err_mess = ''
    # ctrl_str = 'DMYhmsu'
    # if output_mask.find('W'):
    #     ctrl_str += 'W'
    ctrl_str = output_mask
    for chr in ctrl_str:  # W можно и не обрабатывать, только если нужно в выводе
        if chr.isalpha():
            if input_mask.count(chr) > 1:
                err_mess += f'many {chr}, '
            elif not input_mask.count(chr):
                err_mess += f'{chr}- not define, '
    print('_!!!_', err_mess)
    # проверка маски вида DDDhms, что делать при ?h/?m/?s (выдача ошибки в конце и сборка как есть)
    # print(var_list)
    if 'Y' not in input_mask:
        find_flag = 0
        for val in range(len(var_list)-1, -1, -1):
            print(val, type(val))
            print(var_list[val][3])
            if find_flag and var_list[val][3] == 'D':
                print(var_list[val][3])

    # если вставлены не все найденные значения, то добавить разделитель из шаблона
    # print('output_mask = ', output_mask, 'coded =', output_code)

    # out_string = ''
    # for i in output_mask:
    #     pos = input_mask.find(i)
    #     print(pos)
    # print(var_list)
    # var_pos = []
    # for i in var_list:
    #     tmp_pos = output_mask.find(i[3])
    #     var_pos.append([i[3], tmp_pos])
    # print(var_pos)

    # for i in output_mask:
    #     if i.isalpha():
    #         for tmp in var_list:
    #             if tmp[3] == i:
    #                 out_string += str(tmp[0])
    #     else:
    #         out_string += str(i)
    # print('out_string =', out_string)



    # input_mask = "WMDhmsY"  # для тупого алгоритма нужно указать, при автомате сам формируется
    # par_list = re.split(term_mask, time_string)  # strings in list
    # print('Par_list', par_list)
    # if len(input_mask) != len(par_list):
    #     print('что-то не сходится', input_mask, par_list)
    # par_list = [tmp for tmp in par_list if tmp]
    # print(' Cleaned ', par_list)
    # return par_list

    # # Тупой алгоритм перестановки по шаблонам (? что с разделителями делать?)
    # restruct_time_str = ''
    # for cou in output_mask:
    #     restruct_time_str += ' ' + par_list[input_mask.find(cou)]
    # print('Restruct >', restruct_time_str, '< len =', len(restruct_time_str))
    return f'out_string =>{out_string}<'
    # return f'{par_list[6]}-{par_list[1]}-{par_list[2]} {par_list[3]}:{par_list[4]}:{par_list[5]}'


# a = 'one'; b = 'two'  # (['{} - {}'.format(p.name, p.price) for p in products])
# print('{} - {}'.format(a, b))

# ish = '1234567'
# fin = ''
# for i in reversed(ish):
#     fin += i
# print(fin)

# ps = 'As, mn,  bk ,ps,,  a'
# term_mask = ' |,'
# par_list = re.split(term_mask, ps)
# print(par_list)  # ['As', '', 'mn', '', '', 'bk', '', 'ps', '', '', '', 'a']
# final = []
# for tmp in par_list:
#     if tmp:
#         final.append(tmp)
# print(final)
# f2 = []
# f2 = [tmp for tmp in par_list if tmp]
# print(f2)

if vis == 'any':
    print(restruct_datetime(any_time))
elif vis == 'str':
    print('\nFunction answer ', restruct_datetime(str_time))
elif vis == 'datetime':
    print('\nFunction answer ', restruct_datetime(datetime.now()))
elif vis == 'list':
    print('\nFunction answer ', restruct_datetime(time_list))

# w_rename = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
# print(w_rename)
# w_rename[2] = 'x'
# print(w_rename)
# w_rename.pop(2)
# print(w_rename)
# w_rename.insert(2, 'XX')
# print(w_rename)


