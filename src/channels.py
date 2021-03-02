import uuid

from error import InputError, AccessError
from data import retrieve_data

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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):

    data = retrieve_data

    # error when creating a channel name longer than 20 characters
    if len(name) > 20:
        raise InputError(description = "Channel name cannot be longer than 20 characters")

    # creates channel object
    channel_new = {
        'channel_id' : int(uuid.uuid1()) # make a int(UUID) based on the host ID and current time
        'name' : name,  
        'is_public' : is_public,  
        'owner' : auth_user_id
    }

    # appends the new channel to the list of channels
    data["channels"].append(channel_new)

    return {
        'channel_id': channel_new['channel_id']
    }
