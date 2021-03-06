from src.data import retrieve_data
import uuid

from src.error import InputError
from src.error import AccessError

# Function that lists all the channels a user is a part of and their associated details
def channels_list_v1(auth_user_id):
    data = retrieve_data()

    # No parameter errors
    # List of channels
    channel_ids = data['channels']
    # List of channels that user is a part of, starts empty
    channel_list = []

    # Search through individual channels for specific user
    # Go through each channel
    for channel in channel_ids:
        # Within each channel, search for a user_id that matches the input
        for member in data['channels'][channel]['all_members']:
            # In case of id match
            if member == auth_user_id:
                # Create a list of channel attributes
                channel_details = {
                    'channel_id' : channel,
                    'name' : data['channels'][channel]['name'],
                }
                # Add to final list
                channel_list.append(channel_details)
    
    # Return the list as output
    return{
        'channels': channel_list
    }

def channels_listall_v1(auth_user_id):

    data = retrieve_data()
    
    # AccessError occurs when input is invalid auth_user_id
    curr_user = {}
    for user in data['users']:
        if user == auth_user_id:
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

'''
# Testing Purposes
if __name__ == '__main__' :

    data = retrieve_data()
    
    data = reset_data()
  
    user1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    user2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    print(data)

    print(     ) 
    channel_id1 = channels_create_v1(user1['auth_user_id'], "Public Channel", True)
    print(channel_id1)
    print(     ) 
    channels_list = channels_listall_v1(user2['auth_user_id'])
    print(channels_list)
'''
