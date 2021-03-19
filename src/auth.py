from src.error import InputError 
from src.data import retrieve_data
from src.server import APP

import datetime
import jwt
import hashlib 
from flask import jsonify, request, Blueprint, abort, make_response

SECRET = 'CHAMPAGGNE?'

'''
# For testing
from error import InputError 
from data import retrieve_data
'''
import re
import itertools
import uuid

# registered in src/__init__.py
bp = Blueprint('auth', __name__, url_prefix='/')

session = set() # can't use {} lmaooo

# checks if email address has valid format, if so returns true
def auth_email_format(email):
    pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    
    return bool(re.match(pattern, email))

# Given a registered users' email and password
# Returns their `auth_user_id` value
def auth_login_v1(email, password):  

    data = retrieve_data()

    # Checks for invalid email format
    if auth_email_format(email) == False:
        raise InputError
    
    # Checks for existing email and password
    for key_it in data['users'].keys():
        data_email = data['users'][key_it]['email']
        data_password = data['users'][key_it]['password']
        # Checks for matching email and password
        if email == data_email and auth_password_hash(password) == data_password:
            return {'auth_user_id' : key_it}        
    raise InputError


# Given a user's first and last name, email address, and password
# create a new account for them and return a new `auth_user_id`.
def auth_register_v1(email, password, name_first, name_last):

    data = retrieve_data()
    # Checks for invalid email format
    if auth_email_format(email) == False:
        raise InputError
    # Checks for an already existing email address
    elif any(email == data['users'][key_it]['email']\
    for key_it in data['users']):
        raise InputError
    # Ensuring password is over 5 characters
    elif len(password) < 6:
        raise InputError
    # Checks that name_first is not between 1 and 50 characters inclusively in length
    elif len(name_first) > 50 or len(name_first) < 1\
        or len(name_last) > 50 or len(name_last) < 1:
        raise InputError
    
    # Generate handle and add to data['users'][auth_user_id]
    new_handle = name_first.lower() + name_last.lower()
    # Limit handle to first 20 characters if exceeding 20 characters
    if len(new_handle) > 20:
        new_handle = new_handle[0:20]

    # Randomly generate a unique auth_user_id
    new_auth_user_id = int(uuid.uuid4())

    # type 1 is owner, type 2 is member 
    if not data['users']:
        permission_id = 1
    else:
        permission_id = 2

    data['users'][new_auth_user_id] = {
        'name_first' : name_first, 
        'name_last' : name_last, 
        'email' : email,
        'password' : auth_password_hash(password),
        'handle_str' : '',
        'permission_id': permission_id
    }

    # Check to see if the handle is unique
    if any(new_handle == data['users'][user]['handle_str']\
    for user in data['users']):
        # If the handle already exists, append with a number starting from 0
        for epilogue in itertools.count(0, 1):
            if(not any((new_handle + str(epilogue)) ==\
            data['users'][user]['handle_str'] for user in data['users'])):
                data['users'][new_auth_user_id]['handle_str'] =\
                new_handle + str(epilogue)
                return {'auth_user_id' : new_auth_user_id}
    else:   # unique handle, add straght away 
        data['users'][new_auth_user_id]['handle_str'] = new_handle
        return {'auth_user_id' : new_auth_user_id}

"""
Generate and return an expirable token based on auth_user_id
"""
def auth_encode_token(auth_user_id):
    try:
        payload = {
            'exp' : (datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30)),
            'iat' : datetime.datetime.utcnow(),
            'sub' : auth_user_id
        }

        return jwt.encode(
            payload,
            SECRET,
            algorithm='HS256'
        )
    except Exception as e: # catch all kinds of exception
        return e

"""
returns auth_user_id for others to use 
"""
def auth_decode_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])

        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Session expired, log in again'
    except jwt.InvalidTokenError:
        return 'invalid token, log in again'
    except jwt.InvalidTokenError as e:
        return e

# check before using auth_token_decode
def auth_token_ok(token):
    if(isinstance(auth_decode_token(token), str)):
        return False
    else:
        return True

# wrapper
def auth_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# http wrapper for v1 series 
@bp.route('register', methods=['POST'])
def auth_register_v2(): 
    if not request.json or not 'email' in request.json or not 'password' in request.json or not 'first_name' in request.json or not 'last_name' in request.json:
        responseObj = {'status' : 'input error', 'token' : '', 'auth_user_id' : -1}
        return make_response(jsonify(responseObj)), 408

    try:
        # responseObj is a dict with 'token' and 'auth_user_id'
        responseObj = auth_register_v1(request.json['email'], request.json['password'], 
                            request.json['first_name'], request.json['last_name'])
        
        token = auth_encode_token(responseObj['auth_user_id'])
        responseObj['token'] = token 
        session.add(responseObj['auth_user_id'])
        return make_response(jsonify(responseObj)), 201

    except InputError as e:
        responseObj = {'status' : 'input error', 'token' : '', 'auth_user_id' : -1, 'error_msg' : e}
        return make_response(jsonify(responseObj)), 402 # just random status codes, come back later呵呵


@bp.route('login', methods=['POST'])
def auth_login_v2():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        responseObj = {'status' : 'input error', 'token' : '', 'auth_user_id' : -1}
        return make_response(jsonify(responseObj)), 408

    try:
        responseObj = auth_login_v1(request.json['email'], request.json['password'])
        token = auth_encode_token(responseObj['auth_user_id'])
        responseObj['token'] = token

        session.add(responseObj['auth_user_id'])
        return make_response(jsonify(responseObj)), 201

    except InputError as e:
        responseObj = {'status' : 'input error', 'token' : '', 'auth_user_id' : -1, 'error_msg' : e}
        return make_response(jsonify(responseObj)), 402