# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye, Darrell Mounarath, Kellen, Winston Lin, Nikki Yao

import sys
from json import dumps
import json
from flask import Flask, request
from flask_cors import CORS

from src.error import InputError
from src import config

from src.data import read_data, write_data
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2, channel_addowner_v1, channel_removeowner_v1, channel_messages_v2, channel_leave_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2from src.dm import dm_create_v1, dm_messages_v1, dm_details_v1, dm_leave_v1, dm_invite_v1, dm_list_v1, dm_remove_v1, dm_messages_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_leave_v1, dm_invite_v1
from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_share_v1, message_senddm_v1
from src.user import user_profile_v2, user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v2, users_all_v1
from src.other import clear_v1, admin_userpermission_change_v1, admin_user_remove_v1, search_v2
from src.notifications import notifications_get_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = json.dumps({
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


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2_flask():
    payload = request.get_json()
    returnDict = auth_register_v1(payload['email'], payload['password'], payload['name_first'], payload['name_last'])

    write_data()
    return dumps(returnDict)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2_flask():
    payload = request.get_json()
    returnDict = auth_login_v1(payload['email'], payload['password'])

    write_data()
    return dumps(returnDict)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_route():
    payload = request.get_json()
    returnDict = auth_logout_v1(payload['token'])

    write_data()
    return dumps(returnDict)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2_flask():
    data = request.get_json()
    channel_id = channels_create_v2(data['token'], data['name'], data['is_public'])

    write_data()
    return json.dumps(channel_id)



@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove_v1_flask():
    data = request.get_json()
    message_remove_v1(data["token"], data["message_id"])
    
    write_data()
    return json.dumps({})


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2_flask():
    token = request.args.get('token')

    write_data()
    return dumps(channels_listall_v2(token))


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2_flask():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    write_data()
    return dumps(channel_details_v2(token, channel_id))


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']

    write_data()
    return dumps(channel_join_v2(token,channel_id))


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    write_data()
    return dumps(channel_invite_v2(token,channel_id,u_id))


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner_v1_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    write_data()
    return dumps(channel_addowner_v1(token,channel_id,u_id))


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner_v1_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    write_data()
    return dumps(channel_removeowner_v1(token,channel_id,u_id))


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2_flask():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    write_data()
    return dumps(channel_messages_v2(token, channel_id, start))


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave_v1_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']

    write_data()
    return dumps(channel_leave_v1(token,channel_id))


@APP.route('/dm/create/v1', methods=['POST'])
def dm_create_v1_flask(): 
    info = request.get_json()
    dm_id = dm_create_v1(info["token"], info["u_ids"])

    write_data()
    return json.dumps(dm_id)
    

@APP.route('/dm/messages/v1', methods=['GET'])
def dm_messages_v1_flask(): 
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))

    write_data()
    return dumps(dm_messages_v1(token, dm_id, start))

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

@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite_v1_flask(): 
    data = request.get_json()
    dm_invite_v1(data["token"], data["dm_id"], data["u_id"])

    write_data()
    return json.dumps({})

@APP.route('/dm/list/v1', methods=['GET'])
def dm_list_v1_flask(): 
    token = request.args.get("token")
    dm_list = dm_list_v1(token)

    write_data()
    return json.dumps(dm_list)

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove_v1_flask(): 
    data = request.get_json()
    dm_remove_v1(data["token"], data["dm_id"])

    write_data()
    return json.dumps({})


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_v1_flask():
    payload = request.get_json()
    token = payload['token']
    dm_id = payload['dm_id']

    return dumps(dm_leave_v1(token,dm_id))

@APP.route("/message/send/v2", methods=['POST'])
def message_send_v2_flask():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']

    write_data()
    return dumps(message_send_v2(token,channel_id,message))


@APP.route("/notifications/get/v1", methods=['GET'])
def notification_get_v1_flask():
    token = request.args.get('token')

    return dumps(notifications_get_v1(token))

@APP.route('/user/profile/v2', methods=['GET'])
def user_profile_v2_flask():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    returnDict = user_profile_v2(token, u_id)

    write_data()
    return dumps(returnDict)
    

@APP.route('/user/profile/setname/v2', methods=['PUT'])
def user_profile_setname_v2_flask():
    payload = request.get_json()
    returnDict = user_profile_setname_v2(payload['token'], payload['name_first'], payload['name_last'])

    write_data()
    return dumps(returnDict)  


@APP.route('/user/profile/setemail/v2', methods=['PUT'])
def user_profile_setemail_v2_flask():
    payload = request.get_json()
    returnDict = user_profile_setemail_v2(payload['token'], payload['email'])

    write_data()
    return dumps(returnDict) 


@APP.route('/user/profile/sethandle/v2', methods=['PUT'])
def user_profile_sethandle_v2_flask():
    payload = request.get_json()
    returnDict = user_profile_sethandle_v2(payload['token'], payload['handle_str'])

    write_data()
    return dumps(returnDict) 


@APP.route('/users/all/v1', methods=['GET'])
def users_all_v1_flask():
    token = request.args.get('token')

    write_data()
    return dumps(users_all_v1(token))


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm_v1_flask():
    payload = request.get_json()
    token = payload['token']
    dm_id = payload['dm_id']
    message = payload['message']

    write_data()
    return dumps(message_senddm_v1(token,dm_id,message))

@APP.route("/message/share/v1", methods=['POST'])
def message_share_v1_flask():
    data = request.get_json()
    token, og_message_id = data["token"], data["og_message_id"]
    message, channel_id, dm_id = data["message"], data['channel_id'], data['dm_id']
    shared = message_share_v1(token, og_message_id, message, channel_id, dm_id)

    write_data()
    return json.dumps(shared)


@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit_v2_flask():
    data = request.get_json()
    message_edit_v2(data["token"], data["message_id"], data["message"])

    write_data()
    return json.dumps({})


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1_flask():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']

    write_data()
    return dumps(admin_userpermission_change_v1(token, u_id, permission_id))


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_v1_flask():
    payload = request.get_json()
    token = payload['token']
    u_id = int(payload['u_id'])

    write_data()
    return dumps(admin_user_remove_v1(token, u_id))

@APP.route("/search/v2", methods=['GET'])
def search_v2_flask():
    token = request.args.get('token')
    query_str = request.args.get('query_str')

    write_data()
    return dumps(search_v2(token, query_str))


@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    clear_v1()

    return {}

if __name__ == "__main__":
    APP.run(debug=True, port=config.port) # Do not edit this port
