#!/usr/bin/env python
# coding=utf-8

__author__ = 'aheadlead'

import time
import random

import ACfetch
import ACstorage

s = ACstorage.ACstorage()
s.connect()

test = ACfetch.ACfetch('JSESSIONID=ABCDEFABCDEF01234567890123456790; etc_ceping_login_p=abcdefabcdef01234567890123456789; etc_ceping_login_u=011210101')

test.store = s

try:
    test.fetchKey()
except ACfetch.remoteServerGuaLe:
    print "远程的服务器挂了"

existed_count = 0
for i in range(1, 51):
    delay = random.randint(1, 5) 
    print "假装在做题（延时 %.2f 秒）" % (delay,)
    time.sleep(delay)
    try:
        question_json, answer_json, passed = test.fetch()
        print "第 " + str(question_json["currentSubject"]) + " 题 ",
        print "通过" if passed else "失败"
        s.store(question_json, answer_json)
    except ACstorage.questionExisted:
        existed_count += 1
    print "fetched: %d\texisted: %d\tadded:%d" % (i, existed_count, i-existed_count)

if 1 == test.confirm():
    print "恭喜您通过本次安全知识考核，可以参加工程训练了！"
else:
    print "服务器不知道出了什么卵事"

s.close()


