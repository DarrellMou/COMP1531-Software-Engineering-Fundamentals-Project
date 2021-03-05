from src.data import data

from src.error import AccessError
from src.error import InputError

import uuid
from src.auth import auth_register_v1

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):

    global data
    
    # error when invalid auth_user_id
    curr_user = {}
    # find auth_user_id in data
    for user in data['users']:
        if user == auth_user_id['auth_user_id']:
            curr_user = user
    if curr_user == {}:
        raise AccessError("Invalid auth_user_id")

    # list of all channels
    channel_listall = []

    for channel in data['channels']:
        channel_details = {
            'channel_id' : channel,
            'name' : data['channels'][channel]['name'],
        }
        channel_listall.append(channel_details)

    return {
        'channels': channel_listall
    }


def channels_create_v1(auth_user_id, name, is_public):

    global data

    # error when creating a channel name longer than 20 characters
    if len(name) > 20:
        raise InputError("Channel name cannot be longer than 20 characters")

    # error when invalid auth_user_id
    curr_user = {}
    for user in data['users']:
        if user == auth_user_id:
            curr_user = user
    if curr_user == {}:
        raise AccessError("Invalid auth_user_id")
        
    channel_id = int(uuid.uuid1())
    data['channels'][channel_id] = {
            'name' : name, 
            'is_public' : is_public, 
            'owner_members' : [auth_user_id],
            'all_members' : [auth_user_id],
            'messages' : [],
    }

    return {
        'channel_id': channel_id
    }