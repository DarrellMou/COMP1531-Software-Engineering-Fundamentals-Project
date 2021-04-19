# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao (channels_listall, channels_create), Kellen (channels_list)

from src.data import retrieve_data
import uuid

from src.error import InputError, AccessError
from src.auth import auth_token_ok, auth_decode_token

def channels_list_v1(auth_user_id):
    data = retrieve_data()

    # AccessError occurs when input is invalid auth_user_id
    if auth_user_id not in data['users']: raise AccessError("Invalid token")

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


def channels_list_v2(token):
    '''
    BRIEF DESCRIPTION
    2nd version of channels list that requires authenticated token
    
    Arguments:
        token (int) - The login session of the person accessing their channel_list
    
    Exceptions:
        InputError  - N/A
        AccessError - N/A
    
    Return value:
        channels (list of ints) - A list of channel ids belonging to channels the user is a part of
    '''

    user_id = auth_decode_token(token)
    return channels_list_v1(user_id)

# Provide a list of all channels (and their associated details)
def channels_listall_v2(token):
    '''
    BRIEF DESCRIPTION
    Provide a list of all channels (and their associated details)

    Arguments:
        token (string) - authenticated token to view channels

    Exceptions:
        AccessError - occurs when token is not a valid token

    Returns:
        Returns a list of all channels on the platform
    '''

    data = retrieve_data()
    
    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid token")

    # Create list of all channels
    channel_listall = []
    # Searches through channels in data to retrieve details
    for channel in data['channels']:
        channel_details = {
            'channel_id' : channel,
            'name' : data['channels'][channel]['name'],
        }
        channel_listall.append(channel_details)

    return {
        'channels': channel_listall
    }

# Creates a new channel with a name that is either a public or private channel
def channels_create_v2(token, name, is_public):
    '''
    BRIEF DESCRIPTION
    Creates a new channel with that name that is either a public or private channel

    Arguments:
        token (string)      - authenticated token to create channel
        name (string)       - name of the channel
        is_public (boolean) - the type of channel: public or private

    Exceptions:
        AccessError - occurs when token is not a valid token
        InputError  - occurs when the channel name is more than 20 characters long

    Returns:
        Returns an id of the channel created
    '''

    data = retrieve_data()

    # InputError occurs when creating a channel name longer than 20 characters
    if len(name) > 20: raise InputError("Channel name cannot be longer than 20 characters")

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid token")
    auth_user_id = auth_decode_token(token)

    # Generate unique channel_id
    channel_id = int(uuid.uuid4()) >> 100 # avoid overflow

    # Add new channel to channels data
    data['channels'][channel_id] = {
        'name' : name, 
        'is_public' : is_public, 
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages' : [],
        'standup' : {
            'is_active' : False,
            'time_finish' : None,
        },
    } 

    return {
        'channel_id': channel_id
    }


