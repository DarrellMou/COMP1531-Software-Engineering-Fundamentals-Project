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

data['users'] = {}
data['channels'] = {}
a_u_id1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
a_u_id2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
a_u_id3 = auth_register_v1('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
a_u_id4 = auth_register_v1('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
a_u_id5 = auth_register_v1('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

#print(a_u_id1)
ch_id = channels_create_v1(a_u_id1, 'channel1', True)
ch_id2 = channels_create_v1(a_u_id1, 'channel2', True)
#channels_create_v1(a_u_id1, 'channel3', True)
#print(channels_listall_v1(a_u_id1))
channel_invite_v1(a_u_id1, ch_id, a_u_id2)
channel_invite_v1(a_u_id1, ch_id, a_u_id3)
channel_invite_v1(a_u_id1, ch_id, a_u_id4)
channel_invite_v1(a_u_id1, ch_id, a_u_id5)
channel_invite_v1(a_u_id1, ch_id, a_u_id2)
#print(data['channels'])
print(channel_details_v1(a_u_id1, ch_id))