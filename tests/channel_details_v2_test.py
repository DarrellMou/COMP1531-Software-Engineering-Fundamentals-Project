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

# Typical case
def test_function():
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') # returns auth_user_id e.g.
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') # returns auth_user_id e.g.
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

# Channel_details printing a lot of data
def test_many_channel_members():
    a_u_id_list = []
    token_list = []
    # Runs auth_register_v1 10 times, appends auth_user_id return value to a_u_id_list
    for i in range(10):
        a_u_id = auth_register_v1(f'example{i}@hotmail.com', f'password{i}', f'first_name{i}', f'last_name{i}')
        a_u_id_list.append(a_u_id['auth_user_id'])
        token_list.append(a_u_id['token'])
    ch_id = channels_create_v2(token_list[0], 'channel0', True) #returns channel_id0 e.g.
    
    # Runs channel_invite_v2 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(1,10):
        channel_invite_v2(token_list[0], ch_id['channel_id'], a_u_id_list[i])
    assert channel_details_v2(token_list[0], ch_id['channel_id']) == {
        'name': 'channel0',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id_list[0],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id_list[0],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            },
            {
                'u_id': a_u_id_list[1],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': a_u_id_list[2],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': a_u_id_list[3],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': a_u_id_list[4],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
            {
                'u_id': a_u_id_list[5],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
            {
                'u_id': a_u_id_list[6],
                'email': 'example6@hotmail.com',
                'name_first': 'first_name6',
                'name_last': 'last_name6',
                'handle_str': 'first_name6last_name'
            },
            {
                'u_id': a_u_id_list[7],
                'email': 'example7@hotmail.com',
                'name_first': 'first_name7',
                'name_last': 'last_name7',
                'handle_str': 'first_name7last_name'
            },
            {
                'u_id': a_u_id_list[8],
                'email': 'example8@hotmail.com',
                'name_first': 'first_name8',
                'name_last': 'last_name8',
                'handle_str': 'first_name8last_name'
            },
            {
                'u_id': a_u_id_list[9],
                'email': 'example9@hotmail.com',
                'name_first': 'first_name9',
                'name_last': 'last_name9',
                'handle_str': 'first_name9last_name'
            }
        ],
    }

def test_multiple_channels():
    a_u_id_list = []
    token_list = []
    # Runs auth_register_v1 10 times, appends auth_user_id return value to a_u_id_list
    for i in range(10):
        a_u_id = auth_register_v1(f'example{i}@hotmail.com', f'password{i}', f'first_name{i}', f'last_name{i}')
        a_u_id_list.append(a_u_id['auth_user_id'])
        token_list.append(a_u_id['token'])
    ch_id1 = channels_create_v2(token_list[0], 'channel0', True) #returns channel_id0 e.g.
    ch_id2 = channels_create_v2(token_list[5], 'channel1', True) #returns channel_id0 e.g.
    
    # Runs channel_invite_v2 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(1,5):
        channel_invite_v2(token_list[0], ch_id1['channel_id'], a_u_id_list[i])

    # Runs channel_invite_v2 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(6,10):
        channel_invite_v2(token_list[5], ch_id2['channel_id'], a_u_id_list[i])

    assert channel_details_v2(token_list[2], ch_id1['channel_id']) == {
        'name': 'channel0',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id_list[0],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id_list[0],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            },
            {
                'u_id': a_u_id_list[1],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': a_u_id_list[2],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': a_u_id_list[3],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': a_u_id_list[4],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
        ],
    }
    assert channel_details_v2(token_list[8], ch_id2['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id_list[5],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id_list[5],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
            {
                'u_id': a_u_id_list[6],
                'email': 'example6@hotmail.com',
                'name_first': 'first_name6',
                'name_last': 'last_name6',
                'handle_str': 'first_name6last_name'
            },
            {
                'u_id': a_u_id_list[7],
                'email': 'example7@hotmail.com',
                'name_first': 'first_name7',
                'name_last': 'last_name7',
                'handle_str': 'first_name7last_name'
            },
            {
                'u_id': a_u_id_list[8],
                'email': 'example8@hotmail.com',
                'name_first': 'first_name8',
                'name_last': 'last_name8',
                'handle_str': 'first_name8last_name'
            },
            {
                'u_id': a_u_id_list[9],
                'email': 'example9@hotmail.com',
                'name_first': 'first_name9',
                'name_last': 'last_name9',
                'handle_str': 'first_name9last_name'
            }
        ],
    }

# Channel_details given channel id belonging to a non-existent channel
def test_invalid_channel_id():
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    with pytest.raises(InputError):
        channel_details_v2(a_u_id1['token'], 126347542124)

# Channel_details executed by user not in given channel
def test_unauthorized_user():
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    ch_id = channels_create_v2(a_u_id1['token'], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_details_v2(a_u_id2['token'], ch_id['channel_id'])

# Channel_details given invalid token
def test_invalid_token():
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    ch_id = channels_create_v2(a_u_id1["token"], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_details_v2(12345, ch_id['channel_id'])
