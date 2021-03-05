def channels_list_v1(auth_user_id):
    data = retrieve_data()

    # No parameter errors
    # List of channels
    channel_ids = data['channels']

    # Search through individual channels for specific user
    for channel in channel_ids:
        # Create a list of channel attributes
        name = data['channels'][channel]['name']
        owners = data['channels'][channel]['owners']
        members = data['channels'][channel]['members']

        #Look for positive match
        for owner in owners:
            if owner == auth_user_id:
                print('channel_id: ' + channel)
                print('\nname: ' + name)
        for member in members:
            if member == auth_user_id:
                print('channel_id: ' + channel)
                print('\nname: ' + name)


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
    return {
        'channel_id': 1,
    }
