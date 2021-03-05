from src.data import data

from src.error import AccessError
from src.error import InputError

import uuid
from src.auth import auth_register_v1
from src.channels import channels_listall_v1
from src.channels import channels_create_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id for channel in data['channels'])): raise InputError
    if not(any(user == u_id for user in data['users'])): raise InputError
    if not(any(user == auth_user_id for user in data['channels'][channel_id]['owner_members'] + data['channels'][channel_id]['all_members'])): raise AccessError

    # Appends new user to given channel
    # Assume no duplicate entries allowed
    # Assume no inviting themselves
    if not(any(user == u_id for user in data['channels'][channel_id]['owner_members'] + data['channels'][channel_id]['all_members'])):
        data['channels'][channel_id]['all_members'].append(u_id)

    return {}


def channel_details_v1(auth_user_id, channel_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id for channel in data['channels'])): raise InputError
    if not(any(user == auth_user_id for user in data['channels'][channel_id]['owner_members'] + data['channels'][channel_id]['all_members'])): raise AccessError

    # Creates list with necessary data
    name = data['channels'][channel_id]['name']
    owners = data['channels'][channel_id]['owner_members']
    members = data['channels'][channel_id]['all_members']

    details_dict = {}
    details_dict['name'] = name
    details_dict['owner_members'] = []
    details_dict['all_members'] = []

    tmp_list = []
    for owner in owners:
        tmp_dict = {}
        tmp_dict['u_id'] = owner
        tmp_dict['name_first'] = data['users'][owner]['name_first']
        tmp_dict['name_last'] = data['users'][owner]['name_last']
        tmp_list.append(tmp_dict)
    details_dict['owner_members'] = tmp_list

    tmp_list = []
    for member in members:
        tmp_dict = {}
        tmp_dict['u_id'] = member
        tmp_dict['name_first'] = data['users'][member]['name_first']
        tmp_dict['name_last'] = data['users'][member]['name_last']
        tmp_list.append(tmp_dict)
    details_dict['all_members'] = tmp_list

    return details_dict

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }