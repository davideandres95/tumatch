import os, enum

from flaskr.models import db, User, Security, Order, Match, Record
from flaskr.models import db
from flask import Flask, request
from flask_sock import Sock
from .utils import process_websocket, process_http


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    # configure the SQLite database, relative to the app instance folder
    socket = Sock(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

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

    # initialize the app with the extension
    db.init_app(app)

    with app.app_context():
        db.create_all()
        user_david = User(name='David')
        db.session.add(user_david)
        db.session.commit()

    # a simple page that says hello
    @app.route('/hello', methods=['POST'])
    def hello():
        valid = process_http(request)
        print(valid)
        return 'Hello, World!'

    @app.route('/User')
    def print_user():
        david = User.query.first()
        return 'Hello, {} your id is {}'.format(david.name, david.id)

    @socket.route('/websocket')
    def websocket(sock):
        data = sock.receive()
        valid = process_websocket(data)
        print(valid)

    return app
