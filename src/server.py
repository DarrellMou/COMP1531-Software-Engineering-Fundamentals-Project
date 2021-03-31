import sys
from json import dumps
import json
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

from src.error import InputError
from src import config

from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_details_v2

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

# Initialize
@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    clear_v1()
    return {}

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register_v2_flask(): 
    data = request.get_json()
    a_u_id = auth_register_v1(data['email'], data['password'], data['name_first'], data['name_last'])

    return json.dumps(a_u_id)

@APP.route('/channel/invite/v2', methods=['POST'])
def channel_invite_v2_flask(): 
    data = request.get_json()
    channel_invite_v2(data["token"], data["channel_id"], data["u_id"])

    return json.dumps({})

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details_v2_flask(): 
    data = request.get_json()
    channel_details = channel_details_v2(data["token"], data["channel_id"])

    return json.dumps(channel_details)

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
