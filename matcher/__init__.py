import os, enum, hashlib

from werkzeug.security import generate_password_hash
from matcher.models import db, User, Security, Order, Match, Record, Side
from flask import Flask, request, Response, jsonify
from flask_sock import Sock
from .utils import process_websocket, process_http, process_auth, process_input_internal
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
from threading import Thread
from flask import abort

from .api import register, login, extract_user

def create_app(test_config=None):
    global export_datamatch, export_dataorder

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

    def process_delete_order(payload_order, hex_dig):
        target = Order.query.filter_by(u_idx=hex_dig).order_by(Order.created_at.desc()).first()
        quantity = int(payload_order["quantity"])
        if ( target != None):
            if(quantity >= target.quantity):
                db.session.delete(target)
                print('INFO: an order was deleted')
            else:
                target.quantity-=quantity


    def process_update_order(payload_order, hex_dig):
        quantity_text = payload_order["quantity"]
        previous = Order.query.filter_by(u_idx=hex_dig).first()
        previous.quantity += int(quantity_text)
        return previous

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
        log_order(payload_order)
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
        else: #type is Add
            if (Order.query.filter_by(u_idx=hex_dig).first() == None):
                candidate_order = Order(side=Side[side_text.lower()], user_id=user_id, security_id=security_id, quantity=int(quantity_text), price=int(price_text), u_idx=hex_dig) 
                db.session.add(candidate_order)
            else:
                candidate_order = process_update_order(payload_order, hex_dig)
                print('Order already exists, it should be updated')
            return candidate_order
        return None


    def process_match(order):
        if( order.side == Side.sell):
            buy_orders = Order.query.filter_by(side=Side.buy, security_id=order.security_id)
            for buy_order in buy_orders:
                if order.price > buy_order.price:
                    continue
                else:
                    remaining = order.quantity - buy_order.quantity #might be negative!
                    if (remaining > 0):
                        result_match = Match(sell_id=order.id, buy_id=buy_order.id, quantity=buy_order.quantity, price=order.price, security_id=order.security_id)
                        db.session.add(result_match)
                        order.quantity = remaining
                        db.session.delete(buy_order)
                        print('INFO: There was a match')
                        break

                    else:
                        result_match = Match(sell_id=order.id, buy_id=buy_order.id, quantity=order.quantity, price=order.price, security_id=order.security_id)
                        db.session.add(result_match)
                        remaining = abs(remaining)
                        buy_order.quantity = remaining
                        db.session.delete(order)
                        db.session.delete(buy_order)
                        print('INFO: There was a match')
                        break

        else: #Side.buy
            sell_orders = Order.query.filter_by(side=Side.sell, security_id=order.security_id)
            for sell_order in sell_orders:
                if order.price > sell_order.price:
                    continue
                else:
                    remaining = sell_order.quantity - order.quantity #might be negative!
                    if (remaining > 0):
                        result_match = Match(sell_id=sell_order.id, buy_id=order.id, quantity=order.quantity, price=sell_order.price, security_id=order.security_id)
                        db.session.add(result_match)
                        sell_order.quantity = remaining
                        db.session.delete(sell_order)
                        print('INFO: There was a match')
                        break

                    else:
                        result_match = Match(sell_id=sell_order.id, buy_id=order.id, quantity=sell_order.quantity, price=sell_order.price, security_id=order.security_id)
                        db.session.add(result_match)
                        remaining = abs(remaining)
                        order.quantity = remaining
                        db.session.delete(sell_order)
                        db.session.delete(order)
                        print('INFO: There was a match')
                        break
    export_datamatch = process_match
    export_dataorder = process_order

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
        print(request)
        valid, data = process_auth(request)
        if valid is False:
            abort(400, {"msg": data}) 
        return login(data['username'], data['password'])

    @app.route('/User')
    def print_user():
        david = User.query.first()
        return 'Hello, {} your cool id is {}'.format(david.name, david.id)

    @app.route('/http/securities', methods=['GET'])
    def get_securities():
        securities = Security.query.all()
        result = jsonify([{'label': security.as_dict()['name']} for security in securities])
        # result = jsonify(security.as_dict())
        return result, 200
    
    def websocket_client(arg):
        for i in range(arg):
            print("running")
            sleep(1)


    @app.route('/history', methods=['GET'])
    def process_history():
        pass

    @app.route('/http/order/<order_id>', methods=['GET'])
    def get_order_by_id(order_id):
        order = Order.query.filter_by(id=order_id).first()
        return order.as_dict(), 200

    @app.route('/http/all_orders', methods=['GET'])
    def get_all_orders():
        response_dict = {}
        orders = Order.query.all()
        response_dict = [order.as_dict() for order in orders]
        return response_dict, 200


    @app.route('/http/matches', methods=['GET'])
    def get_matches():
        response_dict = {}
        matches = Match.query.all()
        response_dict = [match.as_dict() for match in matches]
        return response_dict, 200

    @app.route('/http/order', methods=['POST'])
    def place_order():
        valid_orders = 0
        global_result = ''
        response_dict = {}

        if list(request.get_json().keys())[0] == "AddOrderRequest":
            payload = request.get_json()["AddOrderRequest"]
            for idx, payload_order in enumerate(payload):
                valid, data = process_input_internal(payload_order)
                if valid:
                    valid_orders += 1
                    success_order = process_order(payload_order)
                    if success_order:
                        match_result = process_match(success_order)
                    single_result = 'SUCCESS - order #{} read succesfully. \n'.format(idx)
                else:
                    single_result = 'ERROR - order #{} has an invalid format: '.format(idx) + data +'\n'

                response_dict[idx]=single_result

                global_result = global_result + single_result

            if db.session.commit() == None:
                global_result = global_result + 'RESULT: {} orders from {} where processed.\n'.format(valid_orders, len(payload))

            #response_dict['global_result'] = global_result + 'INFO: Checking for matches... \n'
            return response_dict, 200
        else:
            return 'BAD PAYLOAD', 400

    @app.route('/http/get_order_batch', methods=['POST'])
    def get_order_batch():
        response_dict = {}
        valid_orders = 0
        global_result = ''
        if list(request.get_json().keys())[0] == "ListOrdersRequest":
            payload = request.get_json()["ListOrdersRequest"]
            for idx, payload_order in enumerate(payload):
                valid, data = process_input_internal(payload_order)
                if valid:
                    valid_orders += 1
                    if 'user_token' in list(payload_order.keys()):
                        user_text = extract_user(payload_order['user_token'])
                        payload_order['user'] = user_text
                    else:
                        user_text = payload_order['user']
                    results = process_list_orders(payload_order)
                    response_dict = [result.as_dict() for result in results]
                    single_result = 'SUCCESS - order #{} read succesfully. \n'.format(idx)
                else:
                    single_result = 'ERROR - order #{} has an invalid format: '.format(idx) + data +'\n'
                global_result = global_result + single_result

            global_result = global_result + 'RESULT: {} orders from {} where processed.'.format(valid_orders, len(payload))
            print(global_result)
            return response_dict, 200
        else:
            return 'BAD PAYLOAD', 400

    @socket.route('/websocket/<token>')
    def websocket(sock, token):
        user = extract_user(token)
        while True:
            data = sock.receive()
            valid, data = process_websocket("%s user=%s" % (data, user))
            sock.send(data)

    return app
