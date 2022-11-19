from flaskr.models import db, User, Security, Order, Match, Record, Side
from  werkzeug.security import generate_password_hash, check_password_hash
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
        'public_id': user.id
    }, "KEY_PRIVATE").encode('ascii')

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
        'public_id': user.id
    }, "KEY_PRIVATE")
    token = base64.b64encode(token).decode("utf-8")
    return {'token': token}