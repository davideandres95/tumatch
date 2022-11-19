import os, enum, hashlib

from werkzeug.security import generate_password_hash
from flaskr.models import db, User, Security, Order, Match, Record, Side
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
        david = User.query.filter_by(name='David').first()
        jnpr = Security.query.filter_by(name='JNPR').first()
        hash_seed = str(david.id) + str(jnpr.id) + Side.buy.name + "5" + "100"
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        sell_order_1 = Order(side=Side.buy, user_id=david.id, security_id=jnpr.id, quantity=100, price=5, u_idx=hex_dig) 
        if Order.query.get(1) == None:
            db.session.add(sell_order_1)
            db.session.commit()

        if david == None:
            password_hash = generate_password_hash("D@avid123", "sha256")
            user_david = User(name='David', password=password_hash)
            db.session.add(user_david, sell_order_1)

            db.session.commit()

    def process_delete_order(payload_order):
        return True

    def process_update_order(payload_order):
        return True

    def process_order(payload_order):
        if payload_order["request"] == "Del":
            process_delete_order(payload_order)
        elif payload_order["request"] == "Add":
            user_text = payload_order["user"]
            security_text = payload_order["security"]
            side_text = payload_order["side"]
            price_text = payload_order["price"]
            quantity_text = payload_order["quantity"]


            security_id = Security.query.filter_by(name=security_text).first().id
            user_id = User.query.filter_by(name=user_text).first().id
            print(Side[side_text.lower()].name)
            hash_seed = str(user_id) + str(security_id) + Side[side_text.lower()].name + str(price_text) + str(quantity_text)
            hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
            hex_dig = hash_object.hexdigest()

            if (Order.query.filter_by(u_idx=hex_dig).first() == None):
                candidate_order = Order(side=Side[side_text.lower()], user_id=user_id, security_id=security_id, quantity=int(quantity_text), price=int(price_text), u_idx=hex_dig) 
                db.session.add(candidate_order)
            else:
                process_update_order(payload_order)
                print('Order already exists, it should be updated')


    # a simple page that says hello
    @app.route('/http', methods=['POST', 'GET'])
    def http():
        valid = process_http(request)
        print(valid)
        return 'Hello, World!'

    @app.route('/User')
    def print_user():
        david = User.query.first()
        return 'Hello, {} your cool id is {}'.format(david.name, david.id)

    @app.route('/Securities')
    def print_securities():
        security = Security.query.first()
        print(security)
        return '{}'.format(security.name)

    @app.route('/order', methods=['POST'])
    def post_order():
        payload = request.get_json()["AddOrderRequest"]
        for payload_order in payload:
            result = process_order(payload_order)
        result = db.session.commit()
        print(result)
        return 'Payload read succesfully (maybe)...{}'

    @socket.route('/websocket')
    def websocket(sock):
        data = sock.receive()
        valid = process_websocket(data)
        print(valid)

    return app
