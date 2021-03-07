from src.data import retrieve_data
import uuid

from src.error import InputError
from src.error import AccessError

def channels_list_v1(auth_user_id):
    data = retrieve_data()

    # No parameter errors
    # List of channels
    channel_ids = data['channels']
    channel_list = []

    # Search through individual channels for specific user
    # Go through each channel
    for channel in channel_ids:
        for member in data['channels'][channel]['all_members']:
            if member == auth_user_id:
                # Create a list of channel attributes
                channel_details = {
                    'channel_id' : channel,
                    'name' : data['channels'][channel]['name'],
                }
                channel_list.append(channel_details)
    
    return{
        'channels': channel_list
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


def channels_create_v1(auth_user_id, name, is_public):

    data = retrieve_data()

    # error when creating a channel name longer than 20 characters
    if len(name) > 20:
        raise InputError("Channel name cannot be longer than 20 characters")

    # AccessError occurs when input is invalid auth_user_id
    if auth_user_id not in data['users']: raise AccessError("Invalid auth_user_id")

    channel_id = int(uuid.uuid1())

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
