#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 上午10:49
# @Author  : wjq
# @File    : time_translater
import calendar
from datetime import datetime
from datetime import timedelta
import time
import re
from dateutil.parser import parse as date_parser
from news_all.tools.html_clean import html2text

_STRICT_DATE_REGEX_PREFIX = r'(?<=\W)'  # \W 除[a-zA-Z0-9_]汉字之外的字符
DATE_REGEX = r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_]?)|(\w{3,}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?'
STRICT_DATE_REGEX = _STRICT_DATE_REGEX_PREFIX + DATE_REGEX


def parse_date_str(date_str):
    if date_str:
        try:
            return date_parser(date_str)
        except (ValueError, OverflowError, AttributeError, TypeError):
            # near all parse failures are due to URL dates without a day
            # specifier, e.g. /2014/04/
            return None


def find_url_date(url):
    date_match = re.search(STRICT_DATE_REGEX, url)
    if date_match:
        date_str = date_match.group(0)
        
        date_str = re.sub(r'[a-z,_,-,/,.]', '', date_str)
        date_str = date_str[:8]
        # print(date_str)
        datetime_obj = parse_date_str(date_str)
        if datetime_obj:
            return datetime_obj


class Pubtime(object):
    def __init__(self, rawtime):
        rawtime = html2text(rawtime)
        self.stamp = nettime_to_pubtime(rawtime)
        self.datetime = timestamp_to_otherStyleTime(self.stamp, return_datetime=True)


def timestamps():
    # 时间戳
    t = str(int(time.time() * 1000))
    return t


def find_time_style(time_str):
    # todo 改为效率更高的正则
    # 2019年02月03日  19年02月03日 2019年2月3日 19年2月3日  02月03日  2月3日
    if re.search(r'\d{1,2}月\d{1,2}日', time_str):
        if re.match(r'\d{1,2}月\d{1,2}日', time_str):
            pattern1 = '%m月%d日'  # 开头是月份
        elif re.match(r'\d{2}年\d{1,2}月\d{1,2}日', time_str):
            pattern1 = '%y年%m月%d日'  # 开头的年份是2位数字
        else:
            pattern1 = '%Y年%m月%d日'  # 开头的年份是4位数字
        time_str = re.sub(r'(?:\d{2,}年)?\d{1,2}月\d{1,2}日', '', time_str)
    
    # 2019-02-03  19-02-03 2019-2-3  19-2-3 02-03 2-3
    elif re.search(r'\d{1,2}-\d{1,2}', time_str):
        if re.match(r'\d{4}-\d{1,2}-\d{1,2}', time_str):
            pattern1 = "%Y-%m-%d"
        elif re.match(r'\d{2}-\d{1,2}-\d{1,2}', time_str):
            pattern1 = "%y-%m-%d"
        else:
            pattern1 = "%m-%d"
        time_str = re.sub(r'(?:\d{2,}-)?\d{1,2}-\d{1,2}', '', time_str, count=1)  # '2019-07-10 14-13-59'
    
    # 2019/02/03 19/02/03 2019/2/3  2019/2/3
    elif re.search(r'\d{1,2}/\d{1,2}', time_str):
        if re.search(r'\d{4}/\d{1,2}/\d{1,2}', time_str):
            pattern1 = "%Y/%m/%d"
        elif re.match(r'\d{2}/\d{1,2}/\d{1,2}', time_str):
            pattern1 = "%y/%m/%d"
        else:
            pattern1 = "%m/%d"
        time_str = re.sub(r'(?:\d{2,}/)?\d{1,2}/\d{1,2}', '', time_str, count=1)
    
    # 2019.02.03  19.02.03 2019.2.3  19.2.3  02.03   2.3
    elif re.search(r'\d{1,2}\.\d{1,2}', time_str):
        if re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', time_str):
            pattern1 = "%Y.%m.%d"
        elif re.match(r'\d{2}\.\d{1,2}\.\d{1,2}', time_str):
            pattern1 = "%y.%m.%d"
        else:
            pattern1 = "%m.%d"
        time_str = re.sub(r'(?:\d{2,}\.)?\d{1,2}\.\d{1,2}', '', time_str)
    else:
        print(time_str, '时间解析错误!')
        return
    
    if time_str == "":
        return pattern1
    
    # tt = time_str.find('T')
    st = time_str.count(' ')
    mt = time_str.count(':')
    if mt > 0:  # '2019-07-10 14-13-59'
        if time_str.find('T') < 0:
            # return pattern1 + ' ' * st + '%H:%M' + ':%S' * (mt - 1)  # 解决 "2019-07-02 10:04:47星期二"
            return pattern1 + ' ' * st + re.sub(r'\d{1,2}:\d{1,2}(?:\:\d{1,2})?(.*?)',
                                                r'%H:%M' + ':%S' * (mt - 1) + r'\1', time_str)
        else:  # UTC时间
            if re.findall(r'\d{1,2}:\d{1,2}:\d{1,2}\.\d{3}', time_str):
                return pattern1 + re.sub(r'\d{1,2}:\d{1,2}:\d{1,2}\.\d{3}(.*?)', r'%H:%M:%S.%f\1', time_str)
            else:
                return pattern1 + re.sub(r'\d{1,2}:\d{1,2}:\d{1,2}(.*?)', r'%H:%M:%S\1', time_str)
    else:
        mt = time_str.count('-')
        # return pattern1 + ' ' * st + '%H-%M' + '-%S' * (mt - 1)
        return pattern1 + ' ' * st + re.sub(r'\d{1,2}-\d{1,2}(?:-\d{1,2})?(.*?)', r'%H-%M' + '-%S' * (mt - 1) + r'\1',
                                            time_str)


def nettime_to_pubtime(pubtime):
    if isinstance(pubtime, Pubtime):
        return pubtime.stamp
    print(pubtime, '转换前的')
    # 转时间戳
    pubtime = str(pubtime).strip()
    if len(pubtime) > 19 and 'T' not in pubtime:
        pubtime = ''.join(get_time_entity(pubtime))
        print('clear time str: %s' % pubtime)
    
    if pubtime.isdigit():
        return pubtime if len(pubtime) >= 13 else pubtime + '000'
    elif pubtime[-1] == "前":  # 3小时前  30分钟前
        day = int(pubtime[:-2]) if pubtime[-2:] == "天前" else 0
        hour = int(pubtime[:-3]) if pubtime[-3:] == "小时前" else 0
        miniute = int(pubtime[:-3]) if pubtime[-3:] == "分钟前" else 0
        t = time.time() - ((day * 24 + hour) * 60 + miniute) * 60
        print(t, '转换后的')
        return str(int(t * 1000))
    
    elif pubtime.find('今天') >= 0:
        # pubtime = pubtime[pubtime.find('今天'):].replace('今天', datetime.today().strftime('%Y-%m-%d'))
        pubtime = datetime.today().strftime('%Y-%m-%d') + pubtime.replace('今天', '')  # 保持日期在时间前
    
    elif pubtime.find('昨天') >= 0:
        # pubtime = pubtime[pubtime.find('昨天'):].replace('昨天', get_zero_dt_of_days(1).strftime('%Y-%m-%d'))
        pubtime = get_zero_dt_of_days(1).strftime('%Y-%m-%d') + pubtime.replace('昨天', '')
    
    pattern = find_time_style(pubtime)
    if not pattern:
        if pubtime == "刚刚":
            return timestamps()
        raise ValueError('时间解析错误!')
    
    a = datetime.strptime(pubtime, pattern)
    
    if pattern.find(r"%Y") < 0:
        a = a.replace(datetime.now().year)  # 新闻发布时间缺少年份就默认取今年
    print(a, '转换后的')
    b = int(time.mktime(a.timetuple())) * 1000
    return str(b)


def timestamp_to_otherStyleTime(timestamp, return_datetime=False):
    """时间戳转字符串或者datetime.datetime类型"""
    if not timestamp:
        return
    tp = int(timestamp) if len(str(timestamp)) < 13 else int(timestamp) // 1000
    
    if return_datetime:
        return datetime.fromtimestamp(tp)
    else:
        timearray = time.localtime(tp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearray)


def get_date_of_Monday(nw=0, return_date=True):
    """
    获取星期一的日期
    :param nw:     int      计算间隔多少周之前周一日期, 默认nw=0本周星期一的日期
    :param return_date      返回数据类型 是 <class 'datetime.date'> 还是str
    :return        datetime.date or str
    """
    today = datetime.date.today()
    m1 = calendar.MONDAY
    t = today.weekday()
    days = datetime.timedelta(days=t - m1 + 7 * nw)
    date_Monday = today - days
    return date_Monday if return_date else date_Monday.strftime('%Y-%m-%d')


def get_zero_dt_of_Monday(nw=0, return_datetime=True):
    """
    获取星期一的凌晨时间
    :param nw:     int          计算间隔多少周之前周一的凌晨时间, 默认nw=0本周星期一的凌晨时间
    :param return_datetime      返回数据类型 是 <class 'datetime.datetime'> 还是str
    :return        datetime.datetime or str
    """
    now = datetime.datetime.now()
    today = datetime.date.today()
    m1 = calendar.MONDAY
    t = today.weekday()
    time_delta = datetime.timedelta(days=t - m1 + 7 * nw, hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
    zero_Monday = now - time_delta
    return zero_Monday if return_datetime else zero_Monday.strftime('%Y-%m-%d %H:%M:%S')


def get_zero_dt_of_days(nd=0, return_datetime=True):
    """
    获取前nd天的凌晨时间
    :param nd:     int          计算间隔多少天之前的凌晨时间, 默认nd=0今天的凌晨时间
    :param return_datetime      返回数据类型 是 <class 'datetime.datetime'> 还是str
    :return        datetime.datetime or str
    """
    now = datetime.now()
    # today = datetime.today()
    time_delta = timedelta(days=nd, hours=now.hour, minutes=now.minute, seconds=now.second,
                           microseconds=now.microsecond)
    zero_Monday = now - time_delta
    return zero_Monday if return_datetime else zero_Monday.strftime('%Y-%m-%d %H:%M:%S')


def get_datetime_ago(days=1, hours=0, minutes=0, seconds=0, return_datetime=True, now=None):
    """
    获取now时间days天hours小时minutes分钟之前的时间
    :param now                  时间基准
    :param return_datetime      返回数据类型 是 <class 'datetime.datetime'> 还是str
    :return        datetime.datetime or str
    """
    if not now:
        now = datetime.now()
    time_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=now.microsecond)
    tt = now - time_delta
    return tt if return_datetime else tt.strftime('%Y-%m-%d %H:%M:%S')


# UTC+8:00的时间就是指北京时间。UTC+0:00就是伦敦时间（格林尼治标准时间）
# todo check
def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


# todo check
def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.utcfromtimestamp(time_struct)
    return utc_st


def get_everyday_date(sd, ed):
    """获取每一天的日期"""
    date_1 = sd
    date_list = [sd]
    ds = (ed - sd).days  # 间隔多少天
    
    for i in range(1, ds):
        date_1 = date_1 + timedelta(days=1)  # 前一天+1天
        date_list.append(date_1)
    
    return date_list + [ed]


import jieba


def get_time_entity(text):
    final_time_list = []
    regex = "(([0-9\uFF10-\uFF19]{1,2}[月底初]{1,2}[0-9\uFF10-\uFF19]{0,2}[日号]{0,1}[\\s|.]{0,1}\\d{0,2}[:时点刻]{0,1}\\d{0,2}[:分钟]{0,2}\\d{0,2}[秒]{0,2})[\\s\\S]*?)|" \
            "([0-9\uFF10-\uFF19]{1,3}[日天])|([一二三四五六七八九十]{0,2}[月底初]{1,2}[一二三四五六七八九十]{0,3}[日号]{0,1})|" \
            "(^(1|2)[0-9]{3}[-/.](([1-9]|0[1-9]|1[0-2])[-/.]([1-9]|0[1-9]|1[0-9]|2[0-8])|([13-9]|0[13-9]|1[0-2])[-/.](29|30)|([13578]|0[13578]|1[02])[-/.]31)([-/.]|\\s{0,})\\d{0,2}:{0,1}\\d{0,2}:{0,1}\\d{0,2}[\\s\\S]*?)|" \
            "([012\uFF10\uFF11\uFF19]{0,1}[0-9\uFF10-\uFF19][:：点时h][0-3\uFF10-\uFF12\uFF19][0-9半\uFF10-\uFF19][:：分m种]{0,2}[0-6\uFF10-\uFF15\uFF109]{0,1}[0-9\uFF10-\uFF19]{0,1}[秒s]{0,1})|" \
            "([零一二三四五六七八九十半个]{0,3}[点小时]{0,2}[零一二三四五六七八九十半]{1,3}[分钟]{1,2}[零一二三四五六七八九十半]{1,3}(秒)?)|" \
            "(([0-9零〇一二三四五六七八九十]{4}[年]{1}[0-9一二三四五六七八九十]{0,2}[月底初]{0,3}[一二三四五六七八九十0-9]{0,2}[日号]{0,1}[\\s|.]{0,1}\\d{0,2}[:时点刻]{0,1}\\d{0,2}[:分钟]{0,2}\\d{0,2}[秒]{0,2})[\\s\\S]*?)|" \
            "(([0-9零〇一二三四五六七八九十]{4}[-/]{1}[0-9一二三四五六七八九十]{0,2}[-/]{0,3}[一二三四五六七八九十0-9]{0,2}[日号]{0,1}[\\s|.]{0,1}\\d{0,2}[:时点刻]{0,1}\\d{0,2}[:分钟]{0,2}\\d{0,2}[秒]{0,2})[\\s\\S]*?)"
    it = re.finditer(regex, text, flags=0)
    for match in it:
        print(match.group())
        final_time_list.append(match.group())
    
    word_list = list(jieba.cut(text, cut_all=False))
    # for x in word_list:
    # print(x)
    # 识别时间单元
    independentTriggerWordRegex = "^(\\d{1,4}[-|\\/]\\d{1,2}[-|\\/](\\d{1,2})?|(星期|周)[日一二三四五六]|黎明|凌晨|拂晓|破晓|初更|早晨|清晨|清早|上午|中午|晌午|下午|傍晚|黄昏|夜晚|晚上|半夜|前天|大前天|昨天|今天|明天|每天|后天|上月|上个月|本月|下月|下个月|正月|腊月|去年|今年|明年|每年|元旦|春节|元宵节|寒食节|情人节|清明节|端午节|愚人节|劳动节|儿童节|父亲节|母亲节|七夕节|国庆节|中秋节|教师节|冬至|圣诞节|平安夜|万圣节)$"
    preDigitalTriggerWordRegex = "^(上世纪|公元|公元前|星期|周)$"
    sufDigitalTriggerWordRegex = "^(世纪|年代|周年)$"
    time_unit_list = []
    for num, word in enumerate(word_list):
        if re.match(independentTriggerWordRegex, word, flags=0):
            time_unit_list.append(word + ';' + str(num))
            continue
        if re.match(preDigitalTriggerWordRegex, word, flags=0):
            if num >= len(word_list) - 1:
                continue
            word_next = word_list[num + 1]
            if word_next.isdigit():
                time_unit_list.append(word + word_next + ';' + str(num + 1))
        if re.match(sufDigitalTriggerWordRegex, word, flags=0):
            if num <= 0:
                continue
            pre_word = word_list[num - 1]
            if pre_word.isdigit():
                time_unit_list.append(pre_word + word + ';' + str(num))
    
    # 识别时间缀词
    timePrefixWordRegex = "^(早|晚|晚间|未来|近|过去|数|上)$"
    timeSuffixWordRegex = "^(晚|同期|末|下旬|中旬|上旬|许|左右|底|初|前|春|夏|秋|冬|春天|夏天|秋天|冬天)$"
    for num, time_unit in enumerate(time_unit_list):
        time_list = time_unit.split(';')
        if len(time_list) < 2:
            continue
        index = int(time_list[1])
        if index <= 0 or index >= len(word_list) - 1:
            continue
        new_time_unit = ''
        pre_word = word_list[index - 1]
        if re.match(timePrefixWordRegex, pre_word, flags=0):
            new_time_unit = pre_word
        word_next = word_list[index + 1]
        if re.match(timeSuffixWordRegex, word_next, flags=0):
            new_time_unit = new_time_unit + time_list[0] + word_next + ';' + str(index + 1)
        if len(new_time_unit) > 0:
            time_unit_list[num] = new_time_unit
    
    # 合并时间单元
    timeConjRegex = "^(至|到)$"
    final_time = ''
    if len(time_unit_list) == 0:
        return final_time_list
    if len(time_unit_list) == 1:
        final_time = time_unit_list[0].split(';')[0]
        final_time_list.append(final_time)
        return final_time_list
    if len(time_unit_list) > 1:
        final_time = time_unit_list[0].split(';')[0]
    for num, tim_unit in enumerate(time_unit_list):
        if num < 1:
            continue
        current_time_list = time_unit.split(';')
        pre_time_list = time_unit_list[num - 1].split(';')
        if len(current_time_list) < 2 or len(pre_time_list) < 2:
            continue
        current_index = int(current_time_list[1])
        pre_index = int(pre_time_list[1])
        if (current_index - pre_index) <= 2:
            if type((current_index - pre_index) / 2) == type(1):
                tim_conj = word_list[(current_index - pre_index) / 2]
                if re.match(timeConjRegex, tim_conj, flags=0):
                    final_time = final_time + tim_conj
                final_time = final_time + current_time_list[0]
        else:
            if final_time != '':
                final_time_list.add(final_time)
            final_time = current_time_list[0]
    return final_time_list


if __name__ == '__main__':
    # print(nettime_to_pubtime('2019-02-21 07:54:50'))
    # print(nettime_to_pubtime('1550729849000'))
    # print(time.localtime(int("15507054240")//10))
    
    # print(nettime_to_pubtime('2019-02-15 9:40'))
    print(nettime_to_pubtime('2019-08-06 10:47:17.0'))
    print(timestamps())
    # dhm = (3, 0, 0)
    # print(get_datetime_ago(*dhm))
    # print(nettime_to_pubtime('发布时间：2019/7/17 09:03:39 | 来源 ：央视网'))
    # print(nettime_to_pubtime('2019-02-26 8:39'))
    # print(nettime_to_pubtime('03月05日'))
    # print(nettime_to_pubtime('2019-05-27 09:44:08'))
    # print(nettime_to_pubtime('-----------来源 昨天 09:34'))
    # #
    # print(nettime_to_pubtime('2018-07-13T16:00:00'))
    # print(nettime_to_pubtime('2018-07-13T16:00:00Z'))
    # print(nettime_to_pubtime('2017-12-21T04:57:42.000Z'))
    # print(nettime_to_pubtime('2018-10-30T07:00:00+0000'))
    # print(nettime_to_pubtime('2018-10-30T07:00:00+08:00'))
    # print(nettime_to_pubtime("2017-07-28T08:28:47.776Z"))
    # print(nettime_to_pubtime('发布时间：2018-10-30T07:00:00+08:00'))  # todo
    
    # print(nettime_to_pubtime('2019年07月10日07:16  来源：人民网－人民日报'))
    # print(get_time_entity('http://kuaixun.stcn.com/2019/0724/15272226.shtml'))
    # print(nettime_to_pubtime('2019-7-1 15:08:22'))
    # print(nettime_to_pubtime('07-02 20:40'))
    # print(nettime_to_pubtime('2019-07-22 14:44'))
    # print(nettime_to_pubtime('2019-07-02 10:04:47星期二'))
    # print(nettime_to_pubtime('2019-07-30 05-04-47星期日'))  # todo
    # print(nettime_to_pubtime('2019-07-30 05-04-47'))
    url = 'http://news.hangzhou.com.cn/shxw/content/2019-07/25/content_7233348.htm'
    # url = 'http://kuaixun.stcn.com/2019/0724/15272226.shtml'
    # url = 'https://it.hangzhou.com.cn/content/content_5458376.htm'
    # url = 'http://www.peopleweekly.cn/html/2019/leyou_0612/15455.html'
    # url = 'http://edu.workercn.cn/209/201907/26/190726132821022.shtml'
    # a = find_url_date(url)
    # print(a)
    
    # utc_time = datetime(2019, 3, 18, 10, 42, 16, 126000)
    #
    # # utc转本地
    # local_time = utc2local(utc_time)
    # print(local_time, local_time.strftime("%Y-%m-%d %H:%M:%S"))
    # # output：2014-09-18 18:42:16
    #
    #
    # # 本地转utc
    # utc_tran = local2utc(local_time)
    # print(utc_tran, utc_tran.strftime("%Y-%m-%d %H:%M:%S"))
    # # output：2014-09-18 10:42:16
