"""
Author: ldqLDQ, Diaplo
功能： 进行与查询相关的操作
"""

from flask_restful import Resource, reqparse
from config import *
import pymysql
from TimeTrans import *


class Search(Resource):
    """
    Author: Diaplo
    功能: 搜索符合条件的已发布自习信息
    """

    """def display(self):
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM records"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results"""

    def get(self):
        return {"error": "method not allowed"}
        # return self.display()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location')
        parser.add_argument('time')
        args = parser.parse_args()
        location = pymysql.escape_string(args["location"])
        # 获取传入参数并存入变量
        Time = pymysql.escape_string(args["time"])
        Unix_Time = unix_time(Time)
        # 转换时间格式
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "select * from records where location like '%%%s%%' and(( stime<=%d and etime>=%d)or %d=-1)" % (
            location, Unix_Time, Unix_Time, Unix_Time)
        cursor.execute(sql)
        # 筛选符合条件的数据
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


class Detail(Resource):
    """
    Author: ldqLDQ
    功能: 获取当前自习详情
    """
    def get(self, tid):
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM records where tid = %d" % tid
        cursor.execute(sql)
        i = cursor.fetchone()
        dat1 = {"tid": i[0], "username": i[1], "stime": normal_time(i[2]), "etime": normal_time(i[3]), "location": i[4],
                "remarks": i[5], "joined": i[6], "finished": finished_status(i[2], i[3])}
        # 存储当前自习的详情数据
        sql = "SELECT * FROM participants where tid = %d" % tid
        cursor.execute(sql)
        dat2 = {}
        # 存储已加入该自习的成员数据
        num = 0
        res = cursor.fetchall()
        for i in res:
            dat0 = {"qname": i[1], "qmessage": i[2]}
            dat2[num] = dat0
            num += 1
        dat = {"detail": dat1, "joined": dat2}
        # 将以上数据均返回
        return {
            "result": "ok",
            # "sql": sql,
            "data": dat
        }

    def post(self):
        return {"error": "method not allowed"}