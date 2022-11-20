import os, enum, hashlib

from werkzeug.security import generate_password_hash
from flaskr.models import db, User, Security, Order, Match, Record, Side
from flaskr.models import db
from flask import Flask, request
from flask_sock import Sock
from .utils import process_websocket, process_http, process_auth, process_input_internal
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from threading import Thread
from flask import abort

from .api import register, login, extract_user

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

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
        if david == None:
            password_hash = generate_password_hash("D@avid123", "sha256")
            david = User(name='David', password=password_hash)
            db.session.add(david)

        jnpr = Security.query.filter_by(name='JNPR').first()
        hash_seed = str(david.id) + str(jnpr.id) + Side.buy.name + "5" + "100"
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        sell_order_1 = Order(side=Side.buy, user_id=david.id, security_id=jnpr.id, quantity=100, price=5, u_idx=hex_dig) 

        if Order.query.get(1) == None:
            db.session.add(sell_order_1)

        db.session.commit()

    def process_delete_order(payload_order, hex_dig):
        target = Order.query.filter_by(u_idx=hex_dig).order_by(Order.created_at.desc()).first()
        if ( target != None):
            db.session.delete(target)
            print('INFO: an order was deleted')

    def process_update_order(payload_order, hex_dig):
        quantity_text = payload_order["quantity"]
        previous = Order.query.filter_by(u_idx=hex_dig).first()
        previous.quantity = int(quantity_text)

    def log_order(payload_order):
        user_text = payload_order["user"]
        payload_text = str(payload_order)
        user_id = User.query.filter_by(name=user_text).first().id
        log = Record(user_id=user_id, payload=payload_text)
        db.session.add(log)
        print('order prepared for log')
        
    def process_list_orders(payload_order):
        user_text = payload_order["user"]
        user_id = User.query.filter_by(name=user_text).first().id
        orders = Order.query.filter_by(user_id=user_id).all()
        print('INFO: the orders of user {} are:\n {}'.format(user_text, str(orders)))
        log_order(payload_order)
        return orders

    def process_order(payload_order):
        type_text = payload_order["request"]
        user_text = payload_order["user"]
        security_text = payload_order["security"]
        side_text = payload_order["side"]
        price_text = payload_order["price"]
        quantity_text = payload_order["quantity"]

        security_id = Security.query.filter_by(name=security_text).first().id
        user_id = User.query.filter_by(name=user_text).first().id
        hash_seed = str(user_id) + str(security_id) + Side[side_text.lower()].name + str(price_text)
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()

        if  type_text == "Del":
            process_delete_order(payload_order, hex_dig)
        elif type_text == "Add":
            if (Order.query.filter_by(u_idx=hex_dig).first() == None):
                candidate_order = Order(side=Side[side_text.lower()], user_id=user_id, security_id=security_id, quantity=int(quantity_text), price=int(price_text), u_idx=hex_dig) 
                db.session.add(candidate_order)
            else:
                process_update_order(payload_order, hex_dig)
                print('Order already exists, it should be updated')

        log_order(payload_order)

    # a simple page that says hello
    @app.route('/hello')
    def hello_world():
        return 'Hello, World!'

    @app.route('/http', methods=['POST', 'GET'])
    def http():
        valid, data = process_http(request)
        if valid is False:
            abort(400, {"msg": data}) 
        return buy()
    
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
        return 'Hello, {} your cool id is {}'.format(david.name, david.id)

    @app.route('/Securities')
    def print_securities():
        security = Security.query.first()
        print(security)
        return '{}'.format(security.name)
    
    def websocket_client(arg):
        for i in range(arg):
            print("running")
            sleep(1)


    @app.route('/history', methods=['GET'])
    def process_history():
        pass

    @app.route('/order', methods=['GET','POST'])
    def place_order():
        valid_orders = 0
        global_result = ''

        if request.method == 'POST':
            payload = request.get_json()["AddOrderRequest"]
            for idx, payload_order in enumerate(payload):
                valid, data = process_input_internal(payload_order)
                if valid:
                    valid_orders += 1
                    result = process_order(payload_order)
                    single_result = 'SUCCESS - order #{} read succesfully. \n'.format(idx)
                else:
                    single_result = 'ERROR - order #{} has an invalid format: '.format(idx) + data +'\n'

                global_result = global_result + single_result

            if db.session.commit() == None:
                global_result = global_result + 'RESULT: {} orders from {} where processed.'.format(valid_orders, len(payload))

        if request.method == 'GET':
            payload = request.get_json()["ListOrdersRequest"]
            for idx, payload_order in enumerate(payload):
                valid, data = process_input_internal(payload_order)
                if valid:
                    valid_orders += 1
                    result = process_list_orders(payload_order)
                    single_result = 'SUCCESS - order #{} read succesfully. \n'.format(idx)
                else:
                    single_result = 'ERROR - order #{} has an invalid format: '.format(idx) + data +'\n'
                global_result = global_result + single_result

            global_result = global_result + 'RESULT: {} orders from {} where processed.'.format(valid_orders, len(payload))

        print(global_result)
        return global_result

    @socket.route('/websocket/<token>')
    def websocket(sock, token):
        user = extract_user(token)
        while True:
            data = sock.receive()
            valid, data = process_websocket("%s user=%s" % (data, user))
            sock.send(data)

    return app
