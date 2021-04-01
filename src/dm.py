
from src.data import data, retrieve_data
from src.error import AccessError, InputError

from src.auth import auth_token_ok, auth_decode_token

import uuid
'''
from data import data, retrieve_data, reset_data
from error import AccessError, InputError

from auth import auth_token_ok, auth_decode_token, auth_register_v1
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

    dm_id = int(uuid.uuid1())

    dm_name = ''
    for u_id in u_ids:
        if u_id == u_ids[-1]:
            dm_name += data['users'][u_ids[-1]]['handle_str']
        else:
            dm_name += data['users'][u_id]['handle_str'] + ', '
        data['users'][u_id]['dms'].append(dm_id)

    data['users'][auth_user_id]['dms'].append(dm_id)

    return {'dm_id': dm_id, 'dm_name': dm_name}