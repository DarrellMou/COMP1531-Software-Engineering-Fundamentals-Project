from data import data

from error import AccessError
from error import InputError

import uuid
from auth import auth_register_v1
from channels import channels_listall_v1
from channels import channels_create_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id['channel_id'] for channel in data['channels'])): raise InputError
    if not(any(user == u_id['auth_user_id'] for user in data['users'])): raise InputError
    if not(any(user == auth_user_id['auth_user_id'] for user in data['channels'][channel_id['channel_id']]['owner_members'] + data['channels'][channel_id['channel_id']]['all_members'])): raise AccessError

    # Appends new user to given channel
    # Assume no duplicate entries allowed
    if not(any(user == u_id['auth_user_id'] for user in data['channels'][channel_id['channel_id']]['owner_members'] + data['channels'][channel_id['channel_id']]['all_members'])):
        data['channels'][channel_id['channel_id']]['all_members'].append(u_id['auth_user_id'])


def channel_details_v1(auth_user_id, channel_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id['channel_id'] for channel in data['channels'])): raise InputError
    if not(any(user == auth_user_id['auth_user_id'] for user in data['channels'][channel_id['channel_id']]['owner_members'] + data['channels'][channel_id['channel_id']]['all_members'])): raise AccessError

    # Creates list with necessary data
    name = data['channels'][channel_id['channel_id']]['name']
    owners = data['channels'][channel_id['channel_id']]['owner_members']
    members = data['channels'][channel_id['channel_id']]['all_members']

    string = ''
    string += f''''name': {name},\n'''
    string += "'owner_members': ["
    # Printing function
    #print('name: ' + name)
    #print('owner_members: [')
    i = 0
    # Iterates through owner members, and prints
    for owner in owners:
        string += f'''
    {'{'}
        u_id: {owners[i]},
        name_first: {data['users'][owner]['name_first']},
        name_last: {data['users'][owner]['name_last']},
    {'},'}'''
        i += 1

    string += f'\n'
    string += "'all_members': ["
    # Iterates through other members, and prints
    #print('all_members: [')
    i = 0
    for member in members:
        string += f'''
    {'{'}
        u_id: {members[i]},
        name_first: {data['users'][member]['name_first']},
        name_last: {data['users'][member]['name_last']},
    {'},'}'''
        i += 1
    string += f'\n]'
    return string

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

print(data)