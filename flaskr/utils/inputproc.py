from flask import request
import re
import base64
import jwt

def extract_user(token: str):
    try:
        token = base64.b64decode(token.encode("utf-8"))
        return jwt.decode(token, key='KEY_PRIVATE')['user_name']
    except:
        return None

def process_input_internal(request: dict):
    try:
        request_type = request['request'].lower()
        if request_type not in ['add', 'del', 'list']:
            return (False, 'Invalid function')
        if request_type == 'list':
            return (True, ['list']) if len(request.keys()) == 2 else (False, "Invalid Format")
        elif request_type == 'add':
            keys = list(request.keys()).copy()
            keys.sort()

            if keys == ['price', 'quantity', 'request', 'security', 'side', 'user_token']:
                # token process
                user = extract_user(request['user_token'])
                if user is None:
                    return (False, "Invalid token")
                del request['user_token']
                request['user'] = user
                keys = list(request.keys()).copy()
                keys.sort()

            if keys != ['price', 'quantity', 'request', 'security', 'side', 'user']:    
                return (False, "Invalid format")
            if request['side'].lower() not in ['buy', 'sell', 'del']:
                return (False, "Invalid format: Side must be [buy, sell, del]")
            if (isinstance(request['quantity'],  int) is False) and (request['quantity'].isdigit() is False or int(request['quantity']) <= 0):
                return (False, "Invalid format: Quantity must be a positive integer")
            if (isinstance(request['price'],  int) is False) and (request['price'].isdigit() is False or int(request['price']) <= 0):
                return (False, "Invalid format: Price must be a positive integer")
            if len(request['user']) < 3:
                return (False, "Invalid format: User invalid (too short or missing)")
            if len(request['security']) <= 2:
                return (False, "Invalid format: Security invalid (too short or missing)")
        return (True, request)
    except:
        return (False, "Invalid format: {request, qty={}, price={}, sec={}, side={}, user={}")
    return (True, args)


def normalize_dict(request: dict):
    return {k.lower(): request[k] for k in request.keys()}

def process_http(request: object):
    content_type = request.headers.get('Content-Type')
    if (content_type.startswith('application/json')):
        return process_input_internal(normalize_dict(request.get_json()))
    elif (content_type.startswith('multipart/form-data')):
        return process_input_internal(normalize_dict(request.form.to_dict(flat=True)))
    else:
        return (False, 'Content-Type not supported')

def process_auth(request: object):
    data = normalize_dict(request.get_json())
    keys = list(data.keys()).copy()
    keys.sort()
    if keys != [ 'password', 'username']:
        return (False, "Invalid format")
    return (True, data)    


def parse_string(request: str):
    request = request.split(" ")
    comp_dict = {value.replace("=", " ").split(" ")[0]: value.replace("=", " ").split(" ")[1] for value in request[1:]}
    comp_dict['request'] = request[0]
    return comp_dict

def process_websocket(request: str):
    try:
        options = parse_string(request)
        return process_input_internal(options)
    except:
        return (False, "Invalid Format")
