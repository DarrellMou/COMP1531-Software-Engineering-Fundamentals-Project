import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config, auth_register_v1, message_send_v2
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
def auth_register_v1_flask():
    data = request.get_json()
    a_u_id1 = auth_register_v1(data['email'], data['password'], data['name_first'], data['name_last'])

    return json.dumps(a_u_id1)


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


@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1_flask():
    reset_data()
    return {}





if __name__ == "__main__":
    APP.run(debug=True, port=config.port) # Do not edit this port
