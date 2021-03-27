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

if __name__ == "__main__":
    APP = create_app()
    APP.run(port=config.port) # Do not edit this port
