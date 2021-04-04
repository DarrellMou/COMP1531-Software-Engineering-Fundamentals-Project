# PROJECT-BACKEND: Team Echo
# Written by Winston Lin

from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token, auth_email_format

###############################################################################
'''       A user's profile is set when he registers, in auth_register       '''
###############################################################################

def user_profile_v2(token, u_id):
    data = retrieve_data()

    if not auth_token_ok(token):
        raise AccessError('invalid token')
    auth_user_id = auth_decode_token(token)

    #if not auth_user_id in data['users']:
    #    raise InputError 
    # print(data['users'])
    # print(type(u_id))
    # print(data['users'].keys())

    try:
        u_id = int(u_id)
    except ValueError:
        print ("Not convertable to integer")

    if not any(x == u_id for x in data['users'].keys()):
        raise InputError('User doesn\'t exist')

    userDict = data['users'][u_id]

    if data['users'][u_id]['is_removed']:
        return {'user' : {
                    'name_first': "Removed",
                    'name_last' : "user"
                    }
                }

    return {'user' : {
                'auth_user_id' : u_id,
                'email'        : userDict['email'],
                'name_first'   : userDict['name_first'],
                'name_last'    : userDict['name_last'],
                'handle_str'   : userDict['handle_str']
                }
           }

def user_profile_setname_v2(token, name_first, name_last):

    data = retrieve_data()

    if len(name_first) not in range(1, 50) or len(name_last) not in range(1, 50):
        raise InputError('invalid name length')

    if not auth_token_ok(token):
        raise InputError('invalid token')

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['name_last'] = name_last
    data['users'][auth_user_id]['name_first'] = name_first

    return {}


def user_profile_setemail_v2(token, new_email):

    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    # email format check 
    if not auth_email_format(new_email):
        raise InputError('invalid email format')

    # if email already used by another user 
    if any(user['email'] == new_email for user in data['users'].values()):
        raise InputError('email already exists') 

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['email'] = new_email

    return {}


def user_profile_sethandle_v2(token, new_handle):

    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    # if email already used by another user 
    if any(user['handle_str'] == new_handle for user in data['users'].values()):
        raise InputError('handle already exists') 
           
    # check handle format
    if len(new_handle) not in range(3, 20):
        raise InputError('invalid handle length')

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['handle_str'] = new_handle

    return {}


def users_all_v1(token):
    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    return data['users']