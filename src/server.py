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
    

'''
import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
import src.config

from src.channels import channels_create_v2, channels_listall_v2

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

# these are left as comment for you to compare the changes 
# APP = Flask(__name__)
# CORS(APP)

# APP.config['TRAP_HTTP_EXCEPTIONS'] = True
# APP.register_error_handler(Exception, defaultHandler)


# create new app instance
def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.register_error_handler(Exception, defaultHandler)

    from src import auth, channels
    app.register_blueprint(auth.bp)
    app.register_blueprint(channels.bp)
    # add more blueprints here from channel, message, etc

    return app

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


# # Example
# @app.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })

if __name__ == "__main__":
    APP = create_app()
    APP.run(port=config.port) # Do not edit this port
'''