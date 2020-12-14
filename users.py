"""
Author: ldqLDQ
功能： 进行与用户相关的转换
"""

from flask_restful import Resource, reqparse
from config import *
import pymysql
from TimeTrans import *


class UserAPI(Resource):
    def get(self, uid):
        return {"user": uid}

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


class MyPublished(Resource):
    """
    Author: ldqLDQ
    功能: 获取一用户已发布的自习列表
    """
    def get(self):
        return 1

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        args = parser.parse_args()
        username = pymysql.escape_string(args["username"])
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM records where username = \'%s\'" % username
        cursor.execute(sql)
        lis = cursor.fetchall()
        dat = {}
        num = 0
        for i in lis:
            dat0 = {"tid": i[0], "username": i[1], "stime": normal_time(i[2]), "etime": normal_time(i[3]),
                    "location": i[4], "remarks": i[5], "joined": i[6], "finished": finished_status(i[2], i[3])}
            dat[num] = dat0
            num += 1
        return {
            "result": "ok",
            # "sql": sql,
            "data": dat
        }


class MyJoined(Resource):
    """
    Author: ldqLDQ
    功能: 获取一用户当前加入的自习列表
    """
    def get(self):
        return 1

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        args = parser.parse_args()
        username = pymysql.escape_string(args["username"])
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM participants where pname = \'%s\'" % username
        cursor.execute(sql)
        lis = cursor.fetchall()
        # 获取加入自习数据
        tidlist = []
        for i in lis:
            tidlist.append(i[3])
        # 获取加入自习的tid列表
        dat = {}
        # 存储所有加入自习的自习数据
        num = 0
        for j in tidlist:
            sql = "SELECT * FROM records where tid = %d" % j
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in res:
                dat0 = {"tid": i[0], "username": i[1], "stime": normal_time(i[2]), "etime": normal_time(i[3]),
                        "location": i[4], "remarks": i[5], "joined": i[6], "finished": finished_status(i[2], i[3])}
                dat[num] = dat0
                num += 1
        return {
            "result": "ok",
            # "sql": sql,
            "data": dat
        }




