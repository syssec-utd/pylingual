"""
本模块用于处理时间数据

This module is used for processing time data
"""
import numpy as np

def before(time_list, time, itself=False, sep=True):
    """
    寻找特定时间
    在时间列表中寻找某个时间点之前的时间
    要求time参数中时间的表述为'xxxx/xx/xx'，分别对应年-月-日，/表示可以是任意符号
    如“1970年1月1日”应表述为'1970/01/01'或'1970.01.01'等
    
    参数
    ----
    time_list：列表类型，时间列表
    time：字符串类型，设定的时间点
    itself：布尔类型，寻找时是否包括设定的时间点本身
    sep：布尔类型，可选，time_list中的元素是否有符号将年月日分开，默认为True
    
    返回
    ----
    元组形式，(筛选到的时间(列表), 筛选到的时间索引(列表))
    
    
    Search special time
    search all then time in time list which are before the point you set
    the expression of time are required to be like 'xxxx/xx/xx', corresponding to year-month-date, / can be any symbol
    e.g.  "January 1st, 1970" should be turned to '1970/01/01' or '1970.01.01' etc
    
    Parameters
    ----------
    time_list: list, list of time
    time: str, the time point
    itself: bool, if include the time point itself when searching
    sep: bool, callable, True means elements in time_list have symbols to seperate the year, month and day, default=True
    
    Return
    ------
    tuple, (filtered time(list), index of the filtered time(list))
    """
    select_time = []
    select_index = []
    date = int(time[:4] + time[5:7] + time[8:10])
    for i in range(len(time_list)):
        judge_time = time_list[i]
        if sep:
            judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
        else:
            judge_num = int(judge_time)
        if date > judge_num:
            select_time.append(judge_time)
            select_index.append(i)
        if itself:
            if date == judge_num:
                select_time.append(judge_time)
                select_index.append(i)
    return (select_time, select_index)

def after(time_list, time, itself=False, sep=True):
    """
    寻找特定时间
    在时间列表中寻找某个时间点之后的时间
    要求时间的表述为'xxxx/xx/xx'，分别对应年-月-日，/表示可以是任意符号
    如“1970年1月1日”应表述为'1970/01/01'或'1970.01.01'等
    
    参数
    ----
    time_list：列表类型，时间列表
    time：字符串类型，设定的时间点
    itself：布尔类型，寻找时是否包括设定的时间点本身
    sep：布尔类型，可选，time_list中的元素是否有符号将年月日分开，默认为True
    
    返回
    ----
    元组形式，(筛选到的时间(列表), 筛选到的时间索引(列表))
    
    
    Search special time
    search all then time in time list which are after the point you set
    the expression of time are required to be like 'xxxx/xx/xx', corresponding to year-month-date, / can be any symbol
    e.g.  "January 1st, 1970" should be turned to '1970/01/01' or '1970.01.01' etc
    
    Parameters
    ----------
    time_list: list, list of time
    time: str, the time point
    itself: bool, if include the time point itself when searching
    sep: bool, callable, True means elements in time_list have symbols to seperate the year, month and day, default=True
    
    Return
    ------
    tuple, (filtered time(list), index of the filtered time(list))
    """
    select_time = []
    select_index = []
    date = int(time[:4] + time[5:7] + time[8:10])
    for i in range(len(time_list)):
        judge_time = time_list[i]
        if sep:
            judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
        else:
            judge_num = int(judge_time)
        if judge_num > date:
            select_time.append(judge_time)
            select_index.append(i)
        if itself:
            if date == judge_num:
                select_time.append(judge_time)
                select_index.append(i)
    return (select_time, select_index)

def equal(time_list, time, sep=True, equal=True):
    """
    寻找特定时间的索引
    在时间列表中寻找某个时间点
    要求时间的表述为'xxxx/xx/xx'，分别对应年-月-日，/表示可以是任意符号
    如“1970年1月1日”应表述为'1970/01/01'或'1970.01.01'等
    
    参数
    ----
    time_list：列表类型，时间列表
    time：列表类型，设定的时间点列表
    sep：布尔类型，可选，time_list中的元素是否有符号将年月日分开，默认为True
    equal：布尔类型，可选，True表示搜索与time相同的时间，False表示搜索与time不相同的时间，默认为True
    
    返回
    ----
    元组形式，(筛选到的时间(列表), 筛选到的时间索引(列表))
    
    
    Search index of special time
    search all then time in time list which are the same as the point you set
    the expression of time are required to be like 'xxxx/xx/xx', corresponding to year-month-date, / can be any symbol
    e.g.  "January 1st, 1970" should be turned to '1970/01/01' or '1970.01.01' etc
    
    Parameters
    ----------
    time_list: list, list of time
    time: list, the time point list
    sep: bool, callable, True means elements in time_list have symbols to seperate the year, month and day, default=True
    equal: bool, callable, True means searching the time in "time", False means searching the time not in "time", default=True
    
    Return
    ------
    tuple, (filtered time(list), index of the filtered time(list))
    """
    select_index = []
    select_time = []
    for i in range(len(time)):
        time[i] = int(time[i][:4] + time[i][5:7] + time[i][8:10])
    if equal:
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if judge_num in time:
                select_index.append(i)
                select_time.append(judge_time)
    else:
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if not judge_num in time:
                select_index.append(i)
                select_time.append(judge_time)
    return (select_time, select_index)

def between(time_list, begin, end, begin_itself=False, end_itself=False, sep=True):
    """
    寻找特定时间
    在时间列表中寻找某个时间点之后的时间
    要求时间的表述为'xxxx/xx/xx'，分别对应年-月-日，/表示可以是任意符号
    如“1970年1月1日”应表述为'1970/01/01'或'1970.01.01'等
    
    参数
    ----
    time_list：列表类型，时间列表
    begin：字符串类型，设定的开始时间点
    end：字符串类型，设定的结束时间点
    begin_itself：布尔类型，可选，寻找时是否包括设定的开始时间点本身，默认为False
    end_itself：布尔类型，可选，寻找时是否包括设定的结束时间点本身，默认为False
    sep：布尔类型，可选，time_list中的元素是否有符号将年月日分开，默认为True
    
    返回
    ----
    元组形式，(筛选到的时间(列表), 筛选到的时间索引(列表))
    
    
    Search special time
    search all then time in time list which are after the point you set
    the expression of time are required to be like 'xxxx/xx/xx', corresponding to year-month-date, / can be any symbol
    e.g.  "January 1st, 1970" should be turned to '1970/01/01' or '1970.01.01' etc
    
    Parameters
    ----------
    time_list: list, list of time
    begin: str, the beginning time point
    end: str, the end time point
    bengin_itself: bool, callable, if include the beginning time point itself when searching, default=False
    end_itself: bool, callable, if include the end time point itself when searching, default=False
    sep: bool, callable, True means elements in time_list have symbols to seperate the year, month and day, default=True
    
    Return
    ------
    tuple, (filtered time(list), index of the filtered time(list))
    """
    select_time = []
    select_index = []
    date_1 = int(begin[:4] + begin[5:7] + begin[8:10])
    date_2 = int(end[:4] + end[5:7] + end[8:10])
    if not begin_itself and (not end_itself):
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if date_1 < judge_num < date_2:
                select_time.append(judge_time)
                select_index.append(i)
    elif begin_itself and (not end_itself):
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if date_1 <= judge_num < date_2:
                select_time.append(judge_time)
                select_index.append(i)
    elif not begin_itself and end_itself:
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if date_1 < judge_num <= date_2:
                select_time.append(judge_time)
                select_index.append(i)
    else:
        for i in range(len(time_list)):
            judge_time = time_list[i]
            if sep:
                judge_num = int(judge_time[:4] + judge_time[5:7] + judge_time[8:10])
            else:
                judge_num = int(judge_time)
            if date_1 <= judge_num <= date_2:
                select_time.append(judge_time)
                select_index.append(i)
    return (select_time, select_index)

def _time_adjust(time):
    """
    调整时间至正确格式
    """
    for i in range(2):
        decimal = time[i] - int(time[i])
        time[i] -= decimal
        time[i + 1] += decimal * 60
    for i in range(1, 3):
        delta = time[-i] // 60
        time[-i] = time[-i] % 60
        time[-i - 1] += delta
    if time[0] < 0:
        for i in range(1, 3):
            if time[-i] > 0:
                time[-i] -= 60
                time[-i - 1] += 1
    return time

def add(*time):
    """
    时间相加
    例：
        add(time_1, time_2, ..., time_n)
        得到Σ time_i
    
    参数
    ----
    time：列表形式，时间，格式为[时, 分, 秒]
    
    返回
    ----
    一维ndarray，相加后的时间
    
    
    Time Addition
    e.g.
        add([1, 23, 45], [5, 43, 21])
        return array([7, 7, 6])
    
    Parameter
    ---------
    time: list, time, in the form of [hour, minute, second]
    
    Return
    ------
    1-D ndarray, time after addition
    """
    time = np.array(time)
    time = time.sum(axis=0)
    return _time_adjust(time)

def sub(time_1, time_2):
    """
    时间相减
    例：
        sub(time_1, time_2)
        得time_1 - time_2
    
    参数
    ----
    time_1，time_2：列表形式，时间，格式为[时, 分, 秒]
    
    返回
    ----
    一维ndarray，相减后的时间
    
    
    Time Subtraction
    e.g.
        sub(time_1, time_2)
        return time_1 - time_2
    
    Parameters
    ----------
    time_1，time_2: list, time, in the form of [hour, minute, second]
    
    Return
    ------
    1-D ndarray, time after subtraction
    """
    time_1 = np.array(time_1)
    time_2 = -np.array(time_2)
    return add(time_1, time_2)

def mul(time, num):
    """
    时间与数相乘
    例：
        mul(time, num)
        得time * num
    
    参数
    ----
    time：列表形式，时间，格式为[时, 分, 秒]
    num：数
    
    返回
    ----
    一维ndarray，相乘后的时间
    
    
    Time Multiplication
    e.g.
        mul(time, num)
        return time * num
    
    Parameters
    ----------
    time: list, time, in the form of [hour, minute, second]
    num: num
    
    Return
    ------
    1-D ndarray, time after multiplication
    """
    time = np.array(time) * np.array(num)
    return _time_adjust(time)

def div(time, divisor):
    """
    时间相除
    时间除以数或时间除以时间
    
    参数
    ----
    time：列表形式，时间，格式为[时, 分, 秒]
    divisor：数或列表，数或时间，时间格式同上
    
    返回
    ----
    time_mode=False时返回数，time_mode=True时返回一维ndarray
    
    
    Time Division
    time divided by number or time divided by time
    
    Parameters
    ----------
    time: list, time, in the form of [hour, minute, second]
    divisor: num or list, number or time, in the form of [hour, minute, second]
    
    Return
    ------
    return a number when time_mode=False, return 1-D ndarray when time_mode=True
    """
    time = np.array(time)
    if type(divisor) == int or type(divisor) == float:
        time = time / divisor
        return _time_adjust(time)
    else:
        divisor = np.array(divisor)
        divisor = 3600 * divisor[0] + 60 * divisor[1] + divisor[0]
        time = 3600 * time[0] + 60 * time[1] + time[0]
        return time / divisor