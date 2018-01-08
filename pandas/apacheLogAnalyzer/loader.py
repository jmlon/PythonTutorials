#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import sys
import datetime


# Apache's common log format
# LogFormat "%h %l %u %t \"%r\" %>s %b" common
commonPattern = '^(?P<host>(\d{1,3}\.(\d{1,3}){3})|([\w\.\-\@\'\*:]+))\s(?P<login>[\w\-]+)\s(?P<user>[\w\-]+)\s\[(?P<datetime>(?P<day>\d+)/(?P<month>\w+)/(?P<year>\d{4}):(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)\s(?P<tzh>[+-]\d{2})(?P<tzm>\d{2}))\]\s"(?P<request>(?P<method>\w+)\s+(?P<resource>[\S]+)(\s+(?P<protocol>HTTP/\w+\.\d+))?)\s*"\s(?P<status>\d+)\s(?P<length>(\d+)|(-)).*$'


months = { 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12 }

compiledRegex = re.compile(commonPattern)



fh = open('/opt/software/datasets/apache/NASA_access_log_Jul95', 'r', encoding='iso-8859-1')
count=0
try:
    for line in fh:
        count+=1
        result = compiledRegex.match(line)
        if result is not None:
            #print( result.lastindex )
            tz = datetime.timezone(datetime.timedelta( hours=int(result.group('tzh')), minutes=int(result.group('tzm')) ))
            dt = datetime.datetime(int(result.group('year')),months[result.group('month')],int(result.group('day')),int(result.group('hour')),int(result.group('minute')),int(result.group('second')), tzinfo=tz )
            #print(dt.isoformat())
            #print(result.group('method'),'--',result.group('resource'),'--',result.group('protocol'))
            #print(result.group('status'))
            #print(result.group('length'))
        else:
            print('INVALID:', line, end='')
            #print(''.join(' '+c+'='+hex(ord(c)) for c in line))
except UnicodeDecodeError:
    print("UnicodeDecodeError at line {}:\n{}".format(count, line))
    
fh.close()

