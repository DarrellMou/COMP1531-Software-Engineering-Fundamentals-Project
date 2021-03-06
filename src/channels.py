import uuid

from src.error import InputError, AccessError
from src.data import retrieve_data, reset_data
'''
# For testing 
from error import InputError, AccessError
from data import retrieve_data, reset_data
from auth import auth_register_v1
'''

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	},
        ],
    }


# Provide a list of all channels (and their associated details)
def channels_listall_v1(auth_user_id):

    data = retrieve_data()
    
    # AccessError occurs when input is invalid auth_user_id
    if auth_user_id not in data['users']: raise AccessError("Invalid auth_user_id")

    # Create list of all channels
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


# Creates a new channel with that name that is either a public or private channel
def channels_create_v1(auth_user_id, name, is_public):

    data = retrieve_data()

    # InputError occurs when creating a channel name longer than 20 characters
    if len(name) > 20: raise InputError("Channel name cannot be longer than 20 characters")

    # AccessError occurs when input is invalid auth_user_id
    if auth_user_id not in data['users']: raise AccessError("Invalid auth_user_id")

    # Generate unique channel_id
    channel_id = int(uuid.uuid1())

    # Add new channel to channels data
    data['channels'][channel_id] = {
        'name' : name, 
        'is_public' : is_public, 
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages' : [],
    }   

    return {
        'channel_id': channel_id
    }


