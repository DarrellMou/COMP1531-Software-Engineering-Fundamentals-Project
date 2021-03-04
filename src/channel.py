from src.data import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # Checks for any errors involving parameters
    if not(any(channel == channel_id for channel in data['channels'])): raise InputError
    if not(any(user == auth_user_id for user in data['channels'][channel_id]['members'] + data['channels'][channel_id]['owners'])): raise AccessError

    # Creates list with necessary data
    name = data['channels'][channel_id]['name']
    owners = data['channels'][channel_id]['owners']
    members = data['channels'][channel_id]['members']

    # Printing function
    print('name: ' + name)
    print('owner_members: [')
    i = 0
    # Iterates through owner members, and prints
    for owner in owners:
        print(f'''    {'{'}
        u_id: {owners[i]},
        name_first: {data['users'][owner]['name_first']},
        name_last: {data['users'][owner]['name_last']},
        {'},'}''')
        i += 1

    # Iterates through other members, and prints
    print('all_members: [')
    i = 0
    for member in members:
        print(f'''    {'{'}
        u_id: {members[i]},
        name_first: {data['users'][member]['name_first']},
        name_last: {data['users'][member]['name_last']},
        {'},'}''')
        i += 1

    # Template
    '''
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
    ],'''


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