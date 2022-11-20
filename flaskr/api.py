from flaskr.models import db, User, Security, Order, Match, Record, Side
from  werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
import jwt
import base64

def register(username, password):
    user = User.query\
        .filter_by(name = username)\
        .first()
    
    if user:
        abort(400, {'msg': 'Already exists'})

    user = User(
        name = username,
        password = generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    token = jwt.encode({
        'public_id': user.id,
        'user_name': user.name
    }, "KEY_PRIVATE")
    if isinstance(token, str):
        token = bytes(token.encode('utf-8'))
    token = base64.b64encode(token).decode('utf-8')
    return {'token': token}


def login(username, password):
    user = User.query\
        .filter_by(name = username)\
        .first()
  
    if not user:
        abort(400, {'msg': 'Incorrect credentials'})
  
    if check_password_hash(user.password, password) is False:
        abort(400, {'msg': 'Incorrect credentials'})

    token = jwt.encode({
        'public_id': user.id,
        'user_name': user.name
    }, "KEY_PRIVATE")
    if isinstance(token, str):
        token = bytes(token.encode('utf-8'))
    token = base64.b64encode(token).decode("utf-8")
    return {'token': token}

def extract_user(token: str):
    try:
        token = base64.b64decode(token.encode("utf-8"))
        return jwt.decode(token, key='KEY_PRIVATE')['user_name']
    except:
        return None

# DEFINE APIs
def buy(username, quantity, security, price):
    success_order = process_order(payload_order)
    if success_order:
        match_result = process_match(success_order)
        single_result = 'SUCCESS - order #{} read succesfully. \n'.format(idx)
    else:
        single_result = 'ERROR - order #{} has an invalid format: '.format(idx) + data +'\n'
    return None

def sell(username, quantity, security, price):
    #TODO implement is
    return None
