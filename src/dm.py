
from src.data import data, retrieve_data, reset_data
from src.error import AccessError, InputError

from src.auth import auth_token_ok, auth_decode_token

import uuid
'''
from data import data, retrieve_data, reset_data
from error import AccessError, InputError

from auth import auth_token_ok, auth_decode_token, auth_register_v1
from message import message_senddm_v1
'''
# Creates dm given list of users
def dm_create_v1(token, u_ids):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if users in u_ids exists
    for u_id in u_ids:
        if u_id not in data['users']: raise InputError

    # Create temporary list for dm members
    users_list = []
    users_list.append(auth_user_id)

    # Create variable to make dm name by combining handle_str(s) of given users
    dm_name = data['users'][auth_user_id]['handle_str'] + ', '
    for u_id in u_ids:
        if u_id == u_ids[-1]:
            dm_name += data['users'][u_ids[-1]]['handle_str']
        else:
            dm_name += data['users'][u_id]['handle_str'] + ', '
        users_list.append(u_id)

    dm_id = int(uuid.uuid1())
    # Add new dm to dms data
    data['dms'][dm_id] = {
        'name': dm_name,
        'members': users_list
    }   

    return {'dm_id': dm_id, 'dm_name': dm_name}

# Returns details of given dm
def dm_details_v1(token, dm_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    members = data['dms'][dm_id]['members']

    # Create temporary list for dm members
    tmp_list = []
    for member in members:
        tmp_dict = {
            'u_id' : member,
            'name_first' : data['users'][member]['name_first'],
            'name_last' : data['users'][member]['name_last']
        }
        tmp_list.append(tmp_dict)

    # Create list to return
    details_dict = {
        'name' : data['dms'][dm_id]['name'],
        'members': tmp_list
    }

    return details_dict

# Returns list of dms that user is a member of
def dm_list_v1(token):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Make list for dms
    dm_list = []

    # Make dict to append to dm_list
    for dm in data['dms']:
        if auth_user_id in data['dms'][dm]['members']:
            dm_dict = {
                'dm_id': dm,
                'name': data['dms'][dm]['name']
            }
            dm_list.append(dm_dict)

    return {'dms': dm_list}

# Returns nothing, removes dm from data
def dm_remove_v1(token, dm_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user is the creator of dm
    if auth_user_id != data['dms'][dm_id]['members'][0]: raise AccessError

    # Deletes dm from data
    del data['dms'][dm_id]

    return {}

# Inviting a user to an existing dm
def dm_invite_v1(token, dm_id, u_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user exists
    if u_id not in data['users']: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    data['dms'][dm_id]['members'].append(u_id)

    return {}

'''
data = reset_data()

user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

dm_id = message_senddm_v1(user1['token'], dm1, "Hey")

print(data)
'''
