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


class Publish(Resource):
    """
    功能：发布一条自习信息
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
        str1 = username+stime+etime+location+remarks
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
            "sql": sql,
            "idnum": idnum,
            "message": str1
            # "result": float(args["rate"]*100)
        }


class Search(Resource):
    """
    功能：搜索符合条件的已发布自习信息
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
        #return self.display()

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
        sql = "select * from records where location like '%%%s%%' and(( stime<%d and etime>%d)or %d=-1)" % (
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
            "sql": sql,
            "data": dat
            # "result": float(args["rate"]*100)
        }


class Join(Resource):
    """
    功能：加入一个自习
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
        str1 = str(tid)+pname+pmessage
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
            "sql": sql,
            "pnum": pid,
            "message": str1
            # "result": float(args["rate"]*100)
        }


class MyPublished(Resource):
    def get(self):
        return 1

    def post(self):
        parser = reqparse.RequestParser()  # 新建parser实例
        # 向parser实例中添加rate参数，并加以配置
        # parser.add_argument('rate', type=float, help='Rate cannot be converted')
        parser.add_argument('username')

        # 将请求中传过来的参数存到args中
        args = parser.parse_args()
        # 将请求参数中的rate的值加以计算，并返回
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
            "sql": sql,
            "data": dat
            # "result": float(args["rate"]*100)
        }


class MyJoined(Resource):
    def get(self):
        return 1

    def post(self):
        parser = reqparse.RequestParser()  # 新建parser实例
        # 向parser实例中添加rate参数，并加以配置
        # parser.add_argument('rate', type=float, help='Rate cannot be converted')
        parser.add_argument('username')

        # 将请求中传过来的参数存到args中
        args = parser.parse_args()
        # 将请求参数中的rate的值加以计算，并返回
        username = pymysql.escape_string(args["username"])
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM participants where pname = \'%s\'" % username
        cursor.execute(sql)
        lis = cursor.fetchall()
        print(lis)
        tidlist = []
        for i in lis:
            tidlist.append(i[3])
        dat = {}
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
            "sql": sql,
            "data": dat
        }


class Detail(Resource):
    def get(self, tid):
        db = pymysql.connect(host=Q_HOST, port=Q_PORT, user=Q_USER, passwd=Q_PASSWORD, db=Q_DB)
        cursor = db.cursor()
        sql = "SELECT * FROM records where tid = %d" % tid
        cursor.execute(sql)
        i = cursor.fetchone()
        dat1 = {"tid": i[0], "username": i[1], "stime": normal_time(i[2]), "etime": normal_time(i[3]), "location": i[4],
                "remarks": i[5], "joined": i[6], "finished": finished_status(i[2], i[3])}
        sql = "SELECT * FROM participants where tid = %d" % tid
        cursor.execute(sql)
        dat2 = {}
        num = 0
        res = cursor.fetchall()
        for i in res:
            dat0 = {"qname": i[1], "qmessage": i[2]}
            dat2[num] = dat0
            num += 1
        dat = {"detail": dat1, "joined": dat2}
        return {
            "result": "ok",
            "sql": sql,
            "data": dat
        }

    def post(self):
        return {"error": "method not allowed"}

