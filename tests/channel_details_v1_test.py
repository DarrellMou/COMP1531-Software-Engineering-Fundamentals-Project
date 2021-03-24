import pytest

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.channel import channel_details_v1
from src.other import clear_v1

# Include fixtures?
# After required functions are implemented

# Typical case
def test_function():
    clear_v1()

    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') # returns auth_user_id e.g.
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') # returns auth_user_id e.g.
    ch_id = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) # returns channel_id e.g.
    channel_invite_v1(a_u_id1['auth_user_id'], ch_id['channel_id'], a_u_id2['auth_user_id'])
    assert channel_details_v1(a_u_id1['auth_user_id'], ch_id['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            }
        ],
    }

# Channel_details printing a lot of data
def test_many_channel_members():
    clear_v1()
    
    a_u_id_list = []
    # Runs auth_register_v1 10 times, appends auth_user_id return value to a_u_id_list
    for i in range(10):
        a_u_id = auth_register_v1(f'example{i}@hotmail.com', f'password{i}', f'first_name{i}', f'last_name{i}')
        a_u_id_list.append(a_u_id['auth_user_id'])
    ch_id = channels_create_v1(a_u_id_list[0], 'channel0', True) #returns channel_id0 e.g.
    
    # Runs channel_invite_v1 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(1,10):
        channel_invite_v1(a_u_id_list[0], ch_id['channel_id'], a_u_id_list[i])
    assert channel_details_v1(a_u_id_list[0], ch_id['channel_id']) == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': a_u_id_list[0],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id_list[0],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            },
            {
                'u_id': a_u_id_list[1],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id_list[2],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id_list[3],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': a_u_id_list[4],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
            {
                'u_id': a_u_id_list[5],
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            },
            {
                'u_id': a_u_id_list[6],
                'name_first': 'first_name6',
                'name_last': 'last_name6',
            },
            {
                'u_id': a_u_id_list[7],
                'name_first': 'first_name7',
                'name_last': 'last_name7',
            },
            {
                'u_id': a_u_id_list[8],
                'name_first': 'first_name8',
                'name_last': 'last_name8',
            },
            {
                'u_id': a_u_id_list[9],
                'name_first': 'first_name9',
                'name_last': 'last_name9',
            }
        ],
    }

def test_multiple_channels():
    clear_v1()
    
    a_u_id_list = []
    # Runs auth_register_v1 10 times, appends auth_user_id return value to a_u_id_list
    for i in range(10):
        a_u_id = auth_register_v1(f'example{i}@hotmail.com', f'password{i}', f'first_name{i}', f'last_name{i}')
        a_u_id_list.append(a_u_id['auth_user_id'])
    ch_id1 = channels_create_v1(a_u_id_list[0], 'channel0', True) #returns channel_id0 e.g.
    ch_id2 = channels_create_v1(a_u_id_list[5], 'channel1', True) #returns channel_id0 e.g.
    
    # Runs channel_invite_v1 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(1,5):
        channel_invite_v1(a_u_id_list[0], ch_id1['channel_id'], a_u_id_list[i])

    # Runs channel_invite_v1 9 times, adds a_u_id1 to a_u_id9 to 'channel0'
    for i in range(6,10):
        channel_invite_v1(a_u_id_list[5], ch_id2['channel_id'], a_u_id_list[i])

    assert channel_details_v1(a_u_id_list[2], ch_id1['channel_id']) == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': a_u_id_list[0],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id_list[0],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            },
            {
                'u_id': a_u_id_list[1],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id_list[2],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id_list[3],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': a_u_id_list[4],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
        ],
    }
    assert channel_details_v1(a_u_id_list[8], ch_id2['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id_list[5],
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            }
        ],
        'all_members': [
            {   
                'u_id': a_u_id_list[5],
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            },
            {
                'u_id': a_u_id_list[6],
                'name_first': 'first_name6',
                'name_last': 'last_name6',
            },
            {
                'u_id': a_u_id_list[7],
                'name_first': 'first_name7',
                'name_last': 'last_name7',
            },
            {
                'u_id': a_u_id_list[8],
                'name_first': 'first_name8',
                'name_last': 'last_name8',
            },
            {
                'u_id': a_u_id_list[9],
                'name_first': 'first_name9',
                'name_last': 'last_name9',
            }
        ],
    }

# Channel_details given channel id belonging to a non-existent channel
def test_invalid_channel_id():
    clear_v1()
    
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    with pytest.raises(InputError):
        channel_details_v1(a_u_id1['auth_user_id'], 126347542124)

# Channel_details executed by user not in given channel
def test_unauthorized_user():
    clear_v1()
    
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    ch_id = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_details_v1(a_u_id2['auth_user_id'], ch_id['channel_id'])