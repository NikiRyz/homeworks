import re
from datetime import datetime, date, time
from collections import defaultdict


def fun1(log):
    parser = re.search(r"(?<=./)[-.\w]+[.]\w+(?=[?\s])", log)
    return parser


def fun2(log):
    parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)
    if parser:
        return parser.group(0)
    else:
        return None


def parse_ignore_urls(log, ignore_urls):
    if log in ignore_urls:
        return True
    else:
        return False


def fun_www(log):
    return re.sub(r"(?<=://)www.", "", log)


def start(log, start):
    parser = re.search("(?<=\[)\d{2}/\w+/\w{4}\s\w+:\w+:\w+", log)
    if parser:
        date_from_log = datetime.strptime(parser.group(0), '%d/%b/%Y %H:%M:%S')
        if start > date_from_log:
            return True
        else:

            return False


def stop(log, stop):
    parser = re.search("(?<=\[)\d{2}/\w+/\w{4}\s\w+:\w+:\w+", log)
    if parser:
        date_from_log = datetime.strptime(parser.group(0), '%d/%b/%Y %H:%M:%S')
        if stop < date_from_log:
            return True
        else:
            return False


def slow(log):
    parser = re.search('(?<=://).*\s([\d]+)(?=\n)', log)
    if parser:
        edit_parser = re.search('^[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', parser.group(1))
        return edit_parser.group()
    else:
        return None


def parse_by_request_type(log, request_type):
    parser = re.search('(?<=")\w+(?=.*://)', log)
    if parser:
        if request_type != parser.group():
            return True
        else:
            return False


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    urls = defaultdict(lambda: {'querie_time': 0, 'count': 0})
    with open('log.log') as f:
        for line in f:
            if ignore_files:
                if fun1(line):
                    continue
            if ignore_urls:
                if fun2(line, ignore_urls):
                    continue
            if ignore_www:
                line = fun_www(line) if fun_www(line) else line
            if start_at:
                if start(line, start_at):
                    continue
            if stop_at:
                if stop(line, stop_at):
                    continue
            if request_type:
                if parse_by_request_type(line, request_type):
                    continue

            if slow_queries:
                if slow(line):
                    urls[fun2(line)]['querie_time'] += int(slow(line))
                    urls[fun2(line)]['count'] += 1

            else:
                if fun2(line):
                    urls[fun2(line)]['count'] += 1
    res = list()
    if slow_queries:
        for val in urls.values():
            res.append(val['querie_time'] // val['count'])
        res = sorted(res, reverse=True)
    else:
        urls = sorted(urls.items(), key=lambda x: x[1]['count'], reverse=True)
        res = [val[1]['count'] for val in urls]

    return res[:5]