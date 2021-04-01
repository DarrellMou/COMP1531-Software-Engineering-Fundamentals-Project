import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.user import user_profile_v2, user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v2, users_all_v1
from src.data import reset_data

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


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2_flask():
    returnDict = auth_register_v1(request.args.get('email'), request.args.get('password'), request.args.get('name_first'), request.args.get('name_last'))

    return dumps(returnDict)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2_flask():
    returnDict = auth_login_v1(request.args.get('email'), request.args.get('password'))

    return dumps(returnDict)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_route():
    returnDict = auth_logout_v1(request.args.get('token'))
    return dumps(returnDict)


###
@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2_flask():
    data = request.get_json()
    channel_id = channels_create_v1(data['auth_user_id'], data['name'], data['is_public'])
    return json.dumps(channel_id)


@APP.route("/message/send/v2", methods=['POST'])
def message_send_v2_flask():
    data = request.get_json()
    message_id = message_send_v2(data['token'], data['channel_id'], data['message'])

    return json.dumps(message_id)


@APP.route('/user/profile/v2', methods=['GET'])
def user_profile_v2_flask():
    returnDict = user_profile_v2(request.args.get('token'), request.args.get('u_id'))
    return dumps(returnDict)


@APP.route('/user/profile/setname/v2', methods=['PUT'])
def user_profile_setname_v2_flask():
    returnDict = user_profile_setname_v2(request.args.get('token'), request.args.get('name_first'), request.args.get('name_last'))
    return dumps(returnDict)  


@APP.route('/user/profile/setemail/v2', methods=['PUT'])
def user_profile_setemail_v2_flask():
    returnDict = user_profile_setemail_v2(request.args.get('token'), request.args.get('email'))
    return dumps(returnDict) 


@APP.route('/user/profile/sethandle/v2', methods=['PUT'])
def user_profile_sethandle_v2_flask():
    returnDict = user_profile_sethandle_v2(request.args.get('token'), request.args.get('handle_str'))
    return dumps(returnDict) 


@APP.route('/users/all/v1', methods=['GET'])
def users_all_v2_flask():
    returnDict = users_all_v1(request.args.get('token'))
    return dumps(returnDict) 


@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    reset_data()
    return {}


if __name__ == "__main__":
    APP.run(debug=True, port=config.port) # Do not edit this port
