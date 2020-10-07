from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user')
def user():
    return 'USR!'


if __name__ == '__main__':
    app.run()
