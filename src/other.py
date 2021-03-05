def clear_v1():
    pass

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'auth_user_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def write_into_data(data):
    user_string = ''
    for user in data['users']:
        user_string += f"""    '{user}' : {'{'}
                'name_first' : '{data['users'][user]['name_first']}',
                'name_last' : '{data['users'][user]['name_last']}',
                'email' : '{data['users'][user]['email']}',
                'password' : '{data['users'][user]['password']}',
            {'},'}
        """

    channel_string = ''
    for channel in data['channels']:
        channel_string += f"""    '{channel}' : {'{'}
                'name' : '{data['channels'][channel]['name']}',
                'is_public' : {data['channels'][channel]['is_public']},
                'owners' : {data['channels'][channel]['owners']},
                'members' : {data['channels'][channel]['members']},
            {'},'}
        """
    data_string = f'''data = {'{'}
        'users' : {'{'}
        {user_string}{'},'}
        'channels' : {'{'}
        {channel_string}{'},'}
    {'}'}'''

    f = open("data.py", "w")
    f.write(data_string)
    f.close()