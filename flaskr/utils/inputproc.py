from flask import request


def process_input_internal(request: dict):
    try:
        if request['func'] not in ['add', 'sell', 'del', 'list']:
            return (False, 'Invalid function')
        return (True, request.keys())
    except:
        return (False, "Invalid format of JSON")
    return (True, args)

def process_socket(request: object):
    print(request.data)
    if request.is_json is False:
        return (False, "Malformed input")
    return process_input_internal(request.get_json())

def process_http(request: object):
    content_type = request.headers.get('Content-Type')
    print(request.headers, request.form)
    if (content_type.startswith('application/json')):
        return process_input_internal(request.get_data())
    elif (content_type.startswith('multipart/form-data')):
        return process_input_internal(request.form.to_dict(flat=False))
    else:
        return (False, 'Content-Type not supported')

