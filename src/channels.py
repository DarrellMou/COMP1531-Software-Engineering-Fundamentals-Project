import uuid

from src.error import InputError, AccessError
from src.data import retrieve_data

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

    data = retrieve_data()
    
    # error when invalid auth_user_id
    curr_user = {}
    # find auth_user_id in data
    for user in data['users']:
        if user['auth_user_id'] == auth_user_id:
            curr_user = user
    if curr_user == {}:
        raise AccessError("Invalid auth_user_id")

    # list of all channels
    channel_listall = []

    for channel in data['channels']:
        channel_details = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name']
        }
        channel_listall.append(channel_details)

    return {
        'channels': channel_listall
    }

def channels_create_v1(auth_user_id, name, is_public):

    return {
        'channel_id' : 1
    }
