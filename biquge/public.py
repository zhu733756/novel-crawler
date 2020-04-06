# -*- coding: utf-8 -*-
import re
import datetime

def format_time(str):
    if not str:
        return None

    str = str.replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-').replace('\\', '-')

    # 2018-01-01 12:01:01
    pat1 = '\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    # 2018-01-01 12:01
    pat1 = '\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")

    # 2018-01-0112:01:01
    pat1 = '\d{4}-\d{1,2}-\d{1,2}\d{2}:\d{2}:\d{2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y-%m-%d%H:%M:%S")

    # 2018-01-0112:01
    pat1 = '\d{4}-\d{1,2}-\d{1,2}\d{2}:\d{2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y-%m-%d%H:%M")

    # 2018-01-01
    pat1 = '\d{4}-\d{1,2}-\d{1,2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y-%m-%d")

    # 20180101
    pat1 = '\d{4}\d{2}\d{2}'
    time = ''.join(re.findall(pat1, str))
    if time:
        return datetime.datetime.strptime(time, "%Y%m%d")