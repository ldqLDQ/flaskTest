from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class UserAPI(Resource):
    def get(self, id):
        return {"user": id}

    def put(self, id):
        pass

    def delete(self, id):
        pass


class IndexView(Resource):
    def get(self):
        return {"hello":"world"}


api.add_resource(UserAPI, '/users/<int:id>', endpoint='/user')
api.add_resource(IndexView,'/',endpoint='index')
#if __name__ == '__main__':
#    app.run()
