from src.data import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id for channel in data['channels'])): raise InputError
    if not(any(user == u_id for user in data['users'])): raise InputError
    if not(any(user == auth_user_id for user in data['channels'][channel_id]['members'] + data['channels'][channel_id]['owners'])): raise AccessError

    # Appends new user to given channel
    data['channels'][channel_id]['members'].append(u_id)

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