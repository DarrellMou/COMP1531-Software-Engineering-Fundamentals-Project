from src.data import data, retrieve_data
from src.error import AccessError, InputError
#from data import data, retrieve_data
#from error import AccessError, InputError

# Invites a user (with user id u_id) to join a channel with ID channel_id
# Once invited the user is added to the channel immediately
def channel_invite_v1(auth_user_id, channel_id, u_id):
    data = retrieve_data()

    # Checks if given channel_id is valid
    if not any(channel == channel_id for channel in data['channels']): raise InputError

    # Checks if user exists
    if not any(user == u_id for user in data['users']): raise InputError

    # Checks if the auth_user is in channel
    if not any(user == auth_user_id for user in data['channels'][channel_id]['all_members']): raise AccessError

    # Appends new user to given channel
    # Assume no duplicate entries allowed
    # Assume no inviting themselves
    # Assume inviting people outside channel only
    if not any(user == u_id for user in data['channels'][channel_id]['all_members']):
        data['channels'][channel_id]['all_members'].append(u_id)

    return {}

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

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
