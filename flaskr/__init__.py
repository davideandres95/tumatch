import os

from flask import Flask, request
from flask_sock import Sock
from .utils import process_websocket, process_http


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    socket = Sock(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello', methods=['POST'])
    def hello():
        valid = process_http(request)
        print(valid)
        return 'Hello, World!'

    @socket.route('/websocket')
    def websocket(sock):
        data = sock.receive()
        valid = process_websocket(data)
        print(valid)
    return app
