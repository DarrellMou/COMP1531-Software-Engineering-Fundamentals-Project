import uuid

from src.error import InputError, AccessError
from src.data import retrieve_data

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	},
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	},
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):

    data = retrieve_data()

    # error when creating a channel name longer than 20 characters
    if len(name) > 20:
        raise InputError("Channel name cannot be longer than 20 characters")

    # AccessError occurs when input isauth_user_id
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
        'owner_members' : auth_user_id,
        'all_members' : auth_user_id,
        'messages' : [],
    }   

    return {
        'channel_id': channel_id
    }

'''
# assert channel id is an integer
if __name__ == '__main__' :

    global data
    
    user1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    print(user1)

    print(     ) 
    channel_id1 = channels_create_v1(user1['auth_user_id'], "Public Channel", True)
    print(channel_id1)
'''
