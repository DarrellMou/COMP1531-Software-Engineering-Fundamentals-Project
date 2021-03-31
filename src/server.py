import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/login/v2", methods=['POST'])
def channels_create_v2_flask():

    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_login(email, password))

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register_v2_flask(): 
    if not request.json or not 'email' in request.json or not 'password' in request.json or not 'first_name' in request.json or not 'last_name' in request.json:
        responseObj = {'status' : 'input error', 'token' : '', 'auth_user_id' : -1}
        return make_response(jsonify(responseObj)), 408

    # responseObj is a dict with 'token' and 'auth_user_id'
    responseObj = auth_register_v1(request.json['email'], request.json['password'], 
                        request.json['first_name'], request.json['last_name'])
    
    # token = auth_encode_token(responseObj['auth_user_id'])
    # responseObj['token'] = token 

    return make_response(jsonify(responseObj)), 201

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2_flask():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = bool(payload['is_public'])

    return dumps(channels_create_v2(token, name, is_public))

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2_flask():
    token = request.args.get('token')

    return dumps(channels_listall_v2(token))

if __name__ == "__main__":
    APP.run(port=config.port,debug=True) # Do not edit this port
