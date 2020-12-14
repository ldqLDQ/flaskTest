"""
Author: ldqLDQ
功能： 进行与信息发布相关的操作
"""

from flask_restful import Resource, reqparse
from config import *
import pymysql
from TimeTrans import *


class Publish(Resource):
    """
    Author: ldqLDQ
    功能: 发布一条自习信息
    """
    def get(self):
        return {"error": "method not allowed"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('stime')
        parser.add_argument('etime')
        parser.add_argument('location')
        parser.add_argument('remarks')
        args = parser.parse_args()
        username = pymysql.escape_string(args["username"])
        stime = pymysql.escape_string(args["stime"])
        etime = pymysql.escape_string(args["etime"])
        location = pymysql.escape_string(args["location"])
        remarks = pymysql.escape_string(args["remarks"])
        # 获取传入参数并存入变量
        unix_t_s = unix_time(stime)
        unix_t_e = unix_time(etime)
        # 转换时间格式
        if unix_t_s > unix_t_e:
            return{
                "result": "failed",
                "message": "结束时间不能早于开始时间"
            }
        if username == "" or stime == "" or etime == "" or location == "":
            return{
                "result": "failed",
                "message": "请完整填写信息！"
            }
        # 返回错误信息
        # str1 = username+stime+etime+location+remarks
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM config"
        cursor.execute(sql)
        idnum = cursor.fetchone()[0]
        # 查询已发布的自习数量
        sql = "UPDATE config SET idnum=idnum+1"
        cursor.execute(sql)
        idnum += 1
        # 发布自习数+1
        sql = "INSERT INTO records (tid, username, stime, etime, location, remarks)" \
              " VALUES " \
              "(%d,\"%s\",%d,%d,\"%s\",\"%s\")"% (idnum, username, unix_t_s, unix_t_e, location, remarks)
        cursor.execute(sql)
        # 插入数据
        return {
            "result": "ok",
            # "sql": sql,
            "idnum": idnum,
            # "message": str1
            "message": "发布自习成功！正在跳转至首页"
        }


class Join(Resource):
    """
    Author: ldqLDQ
    功能: 加入一个自习
    """
    def get(self):
        return {"error": "method not allowed"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tid')
        parser.add_argument('pname')
        parser.add_argument('pmessage')
        args = parser.parse_args()
        tid = int(args["tid"])
        pname = pymysql.escape_string(args["pname"])
        pmessage = pymysql.escape_string(args["pmessage"])
        # 获取传入参数并存入变量
        if pname == "":
            return{
                "result": "failed",
                "message": "请输入姓名"
            }
        # 返回错误数据
        # str1 = str(tid)+pname+pmessage
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "UPDATE records SET joined=joined+1 WHERE tid=%d" % tid
        cursor.execute(sql)
        sql = "SELECT * FROM config"
        cursor.execute(sql)
        pid = cursor.fetchone()[2]
        sql = "UPDATE config SET pnum=pnum+1"
        cursor.execute(sql)
        pid += 1
        sql = "INSERT INTO participants (pid, pname, pmessage, tid)" \
              " VALUES " \
              "(%d,\"%s\",\"%s\",%d)" % (pid, pname, pmessage, tid)
        cursor.execute(sql)
        return {
            "result": "ok",
            # "sql": sql,
            "pnum": pid,
            # "message": str1
            "message": "加入自习成功！"
        }