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



    #Look for positive match, if found print channel details
    for member in data['channels']:
        if member == auth_user_id:
            return {
                'channels': channel_list
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

    data = retrieve_data()

    # error when creating a channel name longer than 20 characters
    if len(name) > 20:
        raise InputError("Channel name cannot be longer than 20 characters")

    # AccessError occurs when input is invalid auth_user_id
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
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages' : [],
    }   

    return {
        'channel_id': channel_id
    }
