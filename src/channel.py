from src.data import data, retrieve_data
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

# Given a Channel with ID channel_id that the authorised user is part of
# Provides basic details about the channel
def channel_details_v1(auth_user_id, channel_id):

    data = retrieve_data()

    # Checks if given channel_id is valid
    if not any(channel == channel_id for channel in data['channels']): raise InputError

    # Checks if the auth_user is in channel
    if not any(user == auth_user_id for user in data['channels'][channel_id]['all_members']): raise AccessError

    # Creates list with necessary data
    name = data['channels'][channel_id]['name']
    owners = data['channels'][channel_id]['owner_members']
    members = data['channels'][channel_id]['all_members']

    # Create list to return
    details_dict = {
        'name' : name,
        'owner_members' : [],
        'all_members' : []
    }

    # Create temporary list for owner members
    tmp_list = []
    for owner in owners:
        tmp_dict = {
            'u_id' : owner,
            'name_first' : data['users'][owner]['name_first'],
            'name_last' : data['users'][owner]['name_last']
        }
        tmp_list.append(tmp_dict)

    # Assigns 'owner_members' key to tmp_list
    details_dict['owner_members'] = tmp_list

    # Create temporary list for all members
    tmp_list = []
    
    # Iterates through members in 'all_members', and appends to tmp_list
    for member in members:
        tmp_dict = {
            'u_id' : member,
            'name_first' : data['users'][member]['name_first'],
            'name_last' : data['users'][member]['name_last']
        }
        tmp_list.append(tmp_dict)
    
    # Assigns 'all_members' key to tmp_list
    details_dict['all_members'] = tmp_list

    return details_dict

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