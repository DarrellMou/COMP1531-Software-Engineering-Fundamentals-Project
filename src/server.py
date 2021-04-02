import sys
from json import dumps
import json
from flask import Flask, request
from flask_cors import CORS

from src.error import InputError
from src import config

from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1

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

    from src import auth
    app.register_blueprint(auth.bp)
    # add more blueprints here from channel, message, etc

    return app


# # Example
# @app.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })

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

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create_v1_flask(): 
    data = request.get_json()
    dm_id = dm_create_v1(data["token"], data["u_ids"])

    return json.dumps(dm_id)

@APP.route('/dm/details/v1', methods=['GET'])
def dm_details_v1_flask(): 
    data = request.get_json()
    dm_details = dm_details_v1(data["token"], data["dm_id"])

    return json.dumps(dm_details)

@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite_v1_flask(): 
    data = request.get_json()
    dm_invite_v1(data["token"], data["dm_id"], data["u_id"])

    return json.dumps({})

if __name__ == "__main__":
    APP.run(port=config.port,debug=True) # Do not edit this port
