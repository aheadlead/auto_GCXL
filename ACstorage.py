# coding=utf-8
__author__ = 'aheadlead'

import sqlite3

db_filename = 'question_library.sqlite3'

class questionExisted(Exception):
    pass

class ACstorage(object):
    def init(self):
        self.sqlite3_handle = None

    def connect(self):
        self.sqlite3_handle = sqlite3.connect(db_filename)

    def store(self, question_json, answer_json):
        try:
            self.sqlite3_handle.execute("INSERT INTO \"question\" (\"depart_name\","
                                        "                      \"description\","
                                        "                      \"itemA\","
                                        "                      \"itemB\","
                                        "                      \"itemC\","
                                        "                      \"itemD\","
                                        "                      \"itemE\","
                                        "                      \"itemF\","
                                        "                      \"itemG\","
                                        "                      \"itemH\","
                                        "                      \"itemI\","
                                        "                      \"itemJ\","
                                        "                      \"itemNum\","
                                        "                      \"key\","
                                        "                      \"answer\","
                                        "                      \"id\")"
                                        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (question_json["depart_name"],
                                         question_json["description"],
                                         question_json["itemA"],
                                         question_json["itemB"],
                                         question_json["itemC"],
                                         question_json["itemD"],
                                         question_json["itemE"],
                                         question_json["itemF"],
                                         question_json["itemG"],
                                         question_json["itemH"],
                                         question_json["itemI"],
                                         question_json["itemJ"],
                                         question_json["itemNum"],
                                         question_json["key"],
                                         answer_json["answer_correct"],
                                         question_json["id"]))
            self.sqlite3_handle.commit()
        except sqlite3.IntegrityError:
            raise questionExisted

    def load(self, question_json):
        cur = self.sqlite3_handle.cursor()
        cur.execute("SELECT answer FROM question WHERE depart_name=? AND description=?",
                    (question_json["depart_name"],
                     question_json["description"]))

        ret = cur.fetchone()

        return ret[0] if ret is not None else 'A'

    def close(self):
        self.sqlite3_handle.close()
