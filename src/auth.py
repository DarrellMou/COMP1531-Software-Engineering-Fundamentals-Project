# PROJECT-BACKEND: Team Echo
# Written by Winston Lin

from src.error import InputError 
from src.data import retrieve_data

import datetime
import jwt
import hashlib 

SECRET = 'CHAMPAGGNE?'
TOKEN_DURATION=5 # 5 seconds

import re
import itertools
import uuid

sessionID = 0

# generates a unique session ID for every login
def getNewSessionID():
    global sessionID 
    sessionID += 1
    return sessionID

# checks if email address has valid format, if so returns true
def auth_email_format(email):
    pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    
    return bool(re.match(pattern, email))

# Given a registered users' email and password
# Returns their `auth_user_id` value
def auth_login_v1(email, password):  
    '''
    BRIEF DESCRIPTION
    Given a registered users' email and password and returns a new `token` for that session

    Arguments:
        email (string)	  - existing email in the system
	    password (string) - existing password to the email

    Exceptions:
    InputError - Occurs when the email entered is not a valid email
    InputError - Occurs when the email entered does not belong to a user
    InputError – Occurs when the password is not correct
    
    Return Value:
        Returns a token to authenticate the user
	    Returns an auth_user_id of the user
    '''

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
            new_sessionID = getNewSessionID()

            data['users'][key_it]['sessions'].append(new_sessionID)
            return {'auth_user_id' : key_it, 'token' : auth_encode_token(key_it, new_sessionID)}        
    raise InputError


# Given a user's first and last name, email address, and password
# create a new account for them and return a new `auth_user_id`.
def auth_register_v1(email, password, name_first, name_last):
    '''
    BRIEF DESCRIPTION
    Given a user's first and last name, email address, and password, create a new account for them and return a new `token` for that session.

    Arguments:
        email (string)	    - new email
        password (string)   - new password
        name_first (string) - first name of the user
        name_last (string)  - last name of the user

    Exceptions:
    InputError - Occurs when the email entered is not a valid email
    InputError - Occurs when the email entered is already being used by another user
    InputError – Occurs when the password entered is less than 6 characters long
    InputError – Occurs when the name_first is not between 1 and 50 characters inclusively in length
    InputError – Occurs when the name_last is not between 1 and 50 characters inclusively in length
    
    Return Value:
        Returns a token to authenticate the user
	    Returns an auth_user_id of the user
    '''

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

    new_sessionID = getNewSessionID()

    data['users'][new_auth_user_id] = {
        'name_first' : name_first, 
        'name_last' : name_last, 
        'email' : email,
        'password' : auth_password_hash(password),
        'handle_str' : '',
        'permission_id': permission_id,
        'sessions' : [new_sessionID],
        'is_removed': False,
        'dms': [],
        'notifications': [],
    }

    # Check to see if the handle is unique
    if any(new_handle == data['users'][user]['handle_str'] for user in data['users']):
        # If the handle already exists, append with a number starting from 0
        for epilogue in itertools.count(0, 1):
            if(not any((new_handle + str(epilogue)) == data['users'][user]['handle_str'] for user in data['users'])):
                data['users'][new_auth_user_id]['handle_str'] = new_handle + str(epilogue)
                return {'auth_user_id' : new_auth_user_id, 'token' : auth_encode_token(new_auth_user_id, new_sessionID)}
    else:   # unique handle, add straght away 
        data['users'][new_auth_user_id]['handle_str'] = new_handle
        return {'auth_user_id' : new_auth_user_id, 'token' : auth_encode_token(new_auth_user_id, new_sessionID)}

"""
Generate and return an expirable token based on auth_user_id
This function does not work on itself, it is used only in auth_register_v1 and auth_login_v1
"""
def auth_encode_token(auth_user_id, sessionID):
    # try:
    payload = {
        'exp' : (datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=TOKEN_DURATION)),
        'iat' : datetime.datetime.utcnow(),
        'auth_user_id' : auth_user_id,
        'sessionID' : sessionID
    }

    return jwt.encode(
        payload,
        SECRET,
        algorithm='HS256'
    )
    # except Exception as e: # catch all kinds of exception
    #     return e

"""
returns auth_user_id for others to use 
"""
def auth_decode_token(token):

    data = retrieve_data()

    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        auth_user_id = payload['auth_user_id']
        sessionID = payload['sessionID'] 

        if sessionID not in data['users'][auth_user_id]['sessions']:
            return 'This session is over'

        return auth_user_id

    except jwt.ExpiredSignatureError:
        return 'Session expired, log in again'
    except jwt.InvalidTokenError:
        return 'invalid token, log in again'


# check before using auth_token_decode
def auth_token_ok(token):
    if(isinstance(auth_decode_token(token), str)):
        return False
    else:
        return True


# retrieves the sessionID embedded in the token, only used in auth_logout_v1, other modules don't need to use this
def auth_get_token_session(token):
    if auth_token_ok(token):
        return jwt.decode(token, SECRET, algorithms=['HS256'])['sessionID']
    else:
        return False

# wrapper
def auth_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# logs out the user session that owns the token
def auth_logout_v1(token):
    '''
    BRIEF DESCRIPTION
    Given an active token, invalidates the token to log the user out. If a valid token is given, 
    and the user is successfully logged out, it returns true, otherwise false.

    Arguments:
        token (string) - token of an authenticated user

    Exceptions:
        n/a
    
    Return Value:
        Returns is_success : True if user is successfully logged out, otherwise False
    '''

    data = retrieve_data()

    if auth_token_ok(token) == True:
        auth_user_id = auth_decode_token(token)
        sessionID = auth_get_token_session(token)
        data['users'][auth_user_id]['sessions'].remove(sessionID)

        responseObj = {'is_success':True}
        return responseObj
    else:
        responseObj = {'is_success':False}
        return responseObj
