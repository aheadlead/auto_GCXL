# coding=utf-8
__author__ = 'aheadlead'

import requests
import re
import json

class remoteServerGuaLe(Exception):
    pass

class ACfetch(object):
    def __init__(self, raw_cookie):
        cookies_0 = raw_cookie.split('; ')
        cookies_1 = [item.split('=') for item in cookies_0]
        self.cookies = dict(cookies_1)

        self.key = None
        self.student_number = self.cookies["etc_ceping_login_u"]
        self.store = None

    def fetchKey(self):
        test_url = "http://211.65.106.99:5080/ceping/stu/test.htm"

        response = requests.get(url=test_url, cookies=self.cookies)

        try:
            m = re.search("key:\"([0-9a-f]{32})", response.content)
            self.key = m.group(1)
        except AttributeError:
            raise remoteServerGuaLe

    def fetch(self):
        question_url = "http://211.65.106.99:5080/ceping/doFindExamSheet.do"
        answer_url = "http://211.65.106.99:5080/ceping/doSaveExamAnswer.do"

        # questions
        payload = {"key": self.key, "stuNum": self.student_number}

        response = requests.post(url=question_url, cookies=self.cookies, data=payload)

        repsonse_json = json.loads(response.text)
        response_json_data = repsonse_json["data"]
        response_json_data_json = json.loads(response_json_data)
        question_json = response_json_data_json

        # answers
        my_answer = self.store.load(question_json)
        payload = {"stuNum": self.student_number, "key": self.key, "myAnswer": my_answer}

        response = requests.post(url=answer_url, cookies=self.cookies, data=payload)

        repsonse_json = json.loads(response.text)
        response_json_data = repsonse_json["data"]
        response_json_data_json = json.loads(response_json_data)
        answer_json = response_json_data_json

        return question_json, answer_json, my_answer == answer_json["answer_correct"]

    def confirm(self):
        confirm_url = "http://211.65.106.99:5080/ceping/doConfirmExamAnswer.do"

        payload = {"stuNum": self.student_number, "key": self.key}

        response = requests.post(confirm_url, cookies=self.cookies, data=payload)

        response_json = json.loads(response.text)

        return response_json["status"]

