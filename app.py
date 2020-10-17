from flask import Flask
from flask_restful import Resource, Api, reqparse
from users import *

app = Flask(__name__)
api = Api(app)


class IndexView(Resource):
    def get(self):
        return {"hello": "world"}


api.add_resource(UserAPI, '/users/<int:uid>', endpoint='/user')
api.add_resource(IndexView, '/', endpoint='index')
api.add_resource(Publish, '/publish', endpoint='Publish')
if __name__ == '__main__':
    app.run()
