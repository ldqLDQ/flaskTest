from flask import Flask
from flask_restful import Resource, Api, reqparse
from config import *
import pymysql
import json

class UserAPI(Resource):
    def get(self, uid):
        return {"user": uid}

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


class Publish(Resource):
    def get(self):
        return {"error": "method not allowed"}

    def post(self):
        parser = reqparse.RequestParser()  # 新建parser实例
        # 向parser实例中添加rate参数，并加以配置
        # parser.add_argument('rate', type=float, help='Rate cannot be converted')
        parser.add_argument('username')
        parser.add_argument('stime')
        parser.add_argument('etime')
        parser.add_argument('location')
        parser.add_argument('remarks')

        # 将请求中传过来的参数存到args中
        args = parser.parse_args()
        # 将请求参数中的rate的值加以计算，并返回
        username = pymysql.escape_string(args["username"])
        stime = pymysql.escape_string(args["stime"])
        etime = pymysql.escape_string(args["etime"])
        location = pymysql.escape_string(args["location"])
        remarks = pymysql.escape_string(args["remarks"])
        str1 = username+stime+etime+location+remarks
        db = pymysql.connect(host=Q_HOST,port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM config"
        cursor.execute(sql)
        idnum = cursor.fetchone()[0]
        sql = "UPDATE config SET idnum=%d WHERE idnum = %d" % (idnum+1, idnum)
        idnum += 1
        cursor.execute(sql)
        sql = "INSERT INTO records (tid, username, stime, etime, location, remarks)" \
              " VALUES " \
              "(%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"% (idnum, username, stime, etime, location, remarks)

        cursor.execute(sql)
        #results = cursor.fetchone()
        return {
            "result": "ok",
            "sql": sql,
            "idnum": idnum,
            "message": str1
            # "result": float(args["rate"]*100)
        }


class Search(Resource):
    def display(self):
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM records"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def get(self):
        #return {"error": "method not allowed"}
        return self.display()

    def post(self):
        return 1


class Join(Resource):
    def get(self):
        return {"error": "method not allowed"}


    def post(self):
        parser = reqparse.RequestParser()  # 新建parser实例
        # 向parser实例中添加rate参数，并加以配置
        # parser.add_argument('rate', type=float, help='Rate cannot be converted')
        parser.add_argument('tid')
        parser.add_argument('pname')
        parser.add_argument('pmessage')

        # 将请求中传过来的参数存到args中
        args = parser.parse_args()
        # 将请求参数中的rate的值加以计算，并返回
        tid = int(args["tid"])
        pname = pymysql.escape_string(args["pname"])
        pmessage = pymysql.escape_string(args["pmessage"])

        str1 = str(tid)+pname+pmessage
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM config"
        cursor.execute(sql)
        pid = cursor.fetchone()[2]
        sql = "UPDATE config SET pnum=%d WHERE pnum = %d" % (pid+1, pid)
        pid += 1
        cursor.execute(sql)
        sql = "INSERT INTO participants (pid, pname, pmessage, tid)" \
              " VALUES " \
              "(%d,\"%s\",\"%s\",%d)" % (pid, pname, pmessage, tid)
        cursor.execute(sql)
        return {
            "result": "ok",
            "sql": sql,
            "pnum": pid,
            "message": str1
            # "result": float(args["rate"]*100)
        }