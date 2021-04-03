import sys
from json import dumps
import json
from flask import Flask, request
from flask_cors import CORS

from src.error import InputError
from src import config

from src.data import read_data, write_data
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_details_v1, dm_leave_v1

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

read_data()

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    info = request.args.get('data')
    if info == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': info
    })

# Initialize
@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    clear_v1()
    return {}

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register_v2_flask(): 
    info = request.get_json()
    a_u_id = auth_register_v1(info['email'], info['password'], info['name_first'], info['name_last'])

    write_data()
    return json.dumps(a_u_id)

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create_v1_flask(): 
    info = request.get_json()
    dm_id = dm_create_v1(info["token"], info["u_ids"])

    write_data()
    return json.dumps(dm_id)

@APP.route('/dm/details/v1', methods=['GET'])
def dm_details_v1_flask(): 
    token = request.args.get("token")
    dm_id = int(request.args.get("dm_id"))
    dm_details = dm_details_v1(token, dm_id)

    write_data()
    return json.dumps(dm_details)

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave_v1_flask(): 
    info = request.get_json()
    dm_leave_v1(info["token"], info["dm_id"])

    write_data()
    return json.dumps({})

if __name__ == "__main__":
    APP.run(port=config.port,debug=True) # Do not edit this port
