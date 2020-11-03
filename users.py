from flask import Flask
from flask_restful import Resource, Api, reqparse


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
        parser.add_argument('title')
        parser.add_argument('content')

        # 将请求中传过来的参数存到args中
        args = parser.parse_args()
        # 将请求参数中的rate的值加以计算，并返回
        username = args["username"]+"ok"
        title = args["title"]+"ok"
        content = args["content"]+"ok"
        return {
            "username": username,
            "title": title,
            "content": content
            # "result": float(args["rate"]*100)
        }
