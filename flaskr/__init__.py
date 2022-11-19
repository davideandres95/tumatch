import os, enum

from werkzeug.security import generate_password_hash
from flaskr.models import db, User, Security, Order, Match, Record, Side
from flaskr.models import db
from flask import Flask, request
from flask_sock import Sock
from .utils import process_websocket, process_http, process_auth
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from threading import Thread

from .api import register, login, extract_user

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
    CORS(app)

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
        david = User.query.filter_by(name='David').first()
        jnpr = Security.query.filter_by(name='JNPR').first()

        if david == None:
            password_hash = generate_password_hash("D@avid123", "sha256")
            user_david = User(name='David', password=password_hash)
            db.session.add(user_david)

        if Order.query.get(1) == None:
            sell_order_1 = Order(side=Side.buy, user_id=user_david.id, security_id=jnpr.id, quantity=100) 
            db.session.add(sell_order_1)
        
        db.session.commit()

    # a simple page that says hello
    @app.route('/http', methods=['POST', 'GET'])
    def http():
        valid, data = process_http(request)
        print(valid)
        return 'Hello, World!'
    
    @app.route('/http/auth/register', methods=['POST'])
    def http_register():
        valid, data = process_auth(request)
        if valid is False:
            abort(400, {"msg": data}) 
        return register(data['username'], data['password'])

    @app.route('/http/auth/login', methods=['POST'])
    def http_login():
        valid, data = process_auth(request)
        if valid is False:
            abort(400, {"msg": data}) 
        return login(data['username'], data['password'])

    @app.route('/User')
    def print_user():
        david = User.query.first()
        return 'Hello, {} your id is {}'.format(david.name, david.id)

    @app.route('/Securities')
    def print_securities():
        security = Security.query.first()
        print(security)
        return '{}'.format(security.name)
    
    def websocket_client(arg):
        for i in range(arg):
            print("running")
            sleep(1)


    @socket.route('/websocket/<token>')
    def websocket(sock, token):
        user = extract_user(token)
        while True:
            data = sock.receive()
            valid, data = process_websocket("%s user=%s" % (data, user))
            sock.send(data)

    return app
