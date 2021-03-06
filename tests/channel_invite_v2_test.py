# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import pytest

from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.channel import channel_details_v2
from src.other import clear_v1

@pytest.fixture(autouse=True)
def reset():
    clear_v1()

# Helper function to set up users
def setup_users():
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')
    user4 = auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4')
    user5 = auth_register_v1('example5@hotmail.com', 'password5', 'first_name5', 'last_name5')

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'user4': user4,
        'user5': user5,
    }

def test_function():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    
    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) # returns channel_id e.g.
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id2['auth_user_id'])
    assert channel_details_v2(a_u_id1["token"], ch_id['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            }
        ],
    }

# Running channel_invite multiple times
def test_multiple_runs():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']
    a_u_id4 = setup['user4']
    a_u_id5 = setup['user5']
    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id2['auth_user_id'])
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id3['auth_user_id'])
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id4['auth_user_id'])
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id5['auth_user_id'])
    assert channel_details_v2(a_u_id2["token"], ch_id['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': a_u_id4['auth_user_id'],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
            {
                'u_id': a_u_id5['auth_user_id'],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
        ],
    }

# Inviting chain
def test_multiple_users_invite():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']
    a_u_id4 = setup['user4']
    a_u_id5 = setup['user5']
    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], a_u_id2['auth_user_id'])
    channel_invite_v2(a_u_id2["token"], ch_id['channel_id'], a_u_id3['auth_user_id'])
    channel_invite_v2(a_u_id3["token"], ch_id['channel_id'], a_u_id4['auth_user_id'])
    channel_invite_v2(a_u_id4["token"], ch_id['channel_id'], a_u_id5['auth_user_id'])
    assert channel_details_v2(a_u_id2["token"], ch_id['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': a_u_id4['auth_user_id'],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
            {
                'u_id': a_u_id5['auth_user_id'],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
        ],
    }

# Channel_invite given channel id belonging to a non-existent channel
def test_invalid_channel_id():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']

    with pytest.raises(InputError):
        channel_invite_v2(a_u_id1["token"], 13637355236473, a_u_id2['auth_user_id'])

# Channel_invite given user that does not exist
def test_invalid_invited_user():
    setup = setup_users()
    a_u_id1 = setup['user1']

    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(InputError):
        channel_invite_v2(a_u_id1["token"], ch_id['channel_id'], 1216374684571)

# Channel_invite executed by user not in given channel
def test_unauthorized_user():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']

    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_invite_v2(a_u_id2["token"], ch_id['channel_id'], a_u_id3['auth_user_id'])

# Channel_invite given invalid token
def test_invalid_token():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']

    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_invite_v2(12345, ch_id['channel_id'], a_u_id2['auth_user_id'])