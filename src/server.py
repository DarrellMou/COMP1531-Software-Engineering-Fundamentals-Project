import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2, channel_addowner_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.dm import dm_create_v1
from src.message import message_senddm_v1
from src.other import clear_v1, admin_userpermission_change_v1

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
def auth_login_v2_flask():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    return dumps(auth_login_v1(email, password))

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_route():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']

    return dumps(auth_register_v1(email, password, name_first, name_last))

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_route():
    payload = request.get_json()
    token = payload['token']

    return dumps(auth_logout_v1(token))

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2_flask():

    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = bool(payload['is_public'])

    return dumps(channels_create_v2(token, name, is_public))

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2_flask():
    payload = request.get_json()
    token = payload['token']

    return dumps(channels_listall_v2(token))

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']

    return dumps(channel_details_v2(token,channel_id))

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']

    return dumps(channel_join_v2(token,channel_id))

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    return dumps(channel_invite_v2(token,channel_id,u_id))

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner_v1_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    return dumps(channel_addowner_v1(token,channel_id,u_id))

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create_v1_flask(): 
    data = request.get_json()
    dm_id = dm_create_v1(data['token'], data['u_ids'])

    return json.dumps(dm_id)
    '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_ids']

    '''
@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm_v1_flask():
    payload = request.get_json()
    token = payload['token']
    dm_id = payload['dm_id']
    message = payload['message']

    return dumps(message_senddm_v1(token,dm_id,message))

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1_flask():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']

    return dumps(admin_userpermission_change_v1(token, u_id, permission_id))

@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    clear_v1()
    return {}

if __name__ == "__main__":
    APP.run(port=config.port,debug=True) # Do not edit this port
    
