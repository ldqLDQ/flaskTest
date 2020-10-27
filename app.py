from flask import Flask
from flask_restful import Resource, Api, reqparse
# from users import *

app = Flask(__name__)
api = Api(app)


class IndexView(Resource):
    def get(self):
        return {"hello": "world123"}


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
        username= args["username"]
        title= args["title"]
        content= args["content"]
        return {
            "username": username,
            "title": title,
            "content": content
            # "result": float(args["rate"]*100)
        }


api.add_resource(UserAPI, '/users/<int:uid>', endpoint='/user')
api.add_resource(IndexView, '/', endpoint='index')
api.add_resource(Publish, '/publish', endpoint='Publish')


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers']= '*'
    return resp


app.after_request(after_request)


#if __name__ == '__main__':
#    app.run()
