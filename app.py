from flask import Flask
from flask_restful import Resource, Api, reqparse
from users import *

app = Flask(__name__)
api = Api(app)


class IndexView(Resource):
    def get(self):
        return {"hello": "world123"}
    #
    """
    
    """


class TestSearch(Resource):
    def get(self):
        return {"hello": "world123"}

    def post(self):
        return {"1":{"tid": "19", "username": "zhangsan", "stime": "2020111111:11", "etime": "2020111112:11",
                 "location": "210", "remarks": "hswt", "joined": "0", "finished": "1"},
                "2":{"tid": "20", "username": "zhangsan", "stime": "2020111111:11", "etime": "2020111112:11",
                 "location": "210", "remarks": "hswt", "joined": "0", "finished": "0"},
                "3":{"tid": "21", "username": "zhangsan", "stime": "2020111111:11", "etime": "2020111112:11",
                 "location": "210", "remarks": "hswt", "joined": "0", "finished": "0"},
                "4":{"tid": "22", "username": "zhangsan", "stime": "2020111111:11", "etime": "2020111112:11",
                 "location": "210", "remarks": "hswt", "joined": "0", "finished": "0"}
                }
''' return {
	"result": "ok",
	"data": {
		"0": {
			"tid": 19,
			"username": "zhangsan",
			"stime": "2020111111:11",
			"etime": "2020111112:11",
			"location": "210",
			"remarks": "hswt",
			"joined": 0,
			"finished": "已完成"
		},
		"1": {
			"tid": 20,
			"username": "zhangsan",
			"stime": "2020年11月11日11:11",
			"etime": "2020年11月11日12:11",
			"location": "博学楼210",
			"remarks": "黑色外套",
			"joined": 0,
			"finished": "已完成"
		},
		"2": {
			"tid": 21,
			"username": "zhangsan",
			"stime": "2020年11月11日11:11",
			"etime": "2020年11月11日12:11",
			"location": "博学楼210",
			"remarks": "黑色外套\"",
			"joined": 0,
			"finished": "已完成"
		},
		"3": {
			"tid": 22,
			"username": "zhangsan",
			"stime": "2020'年11月11日11:11",
			"etime": "2020年11月11日12:11'",
			"location": "博学楼210'",
			"remarks": "黑色外套\"'",
			"joined": 0,
			"finished": "已完成"
		},
		"4": {
			"tid": 23,
			"username": "zhangsan",
			"stime": "2020'年11月11日11:11",
			"etime": "2020年11月11日12:11'",
			"location": "博学楼210'",
			"remarks": "黑色外套\"'",
			"joined": 0,
			"finished": "已完成"
		},
		"5": {
			"tid": 24,
			"username": "zhangsan",
			"stime": "2020'年11月11日11:11",
			"etime": "2020年11月11日12:11'",
			"location": "博学楼210'",
			"remarks": "黑色外套\"'",
			"joined": 0,
			"finished": "已完成"
		}
	}
}'''

api.add_resource(UserAPI, '/users/<int:uid>', endpoint='user')
api.add_resource(IndexView, '/', endpoint='index')
api.add_resource(Publish, '/publish', endpoint='Publish')
api.add_resource(Search, '/search', endpoint='Search')
api.add_resource(Join, '/join', endpoint='Join')
api.add_resource(MyPublished, '/my/published', endpoint='MyPublished')
api.add_resource(MyJoined, '/my/joined', endpoint='MyJoined')
api.add_resource(TestSearch, '/test/search', endpoint='testsearch')


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


app.after_request(after_request)


#if __name__ == '__main__':
#    app.run()
