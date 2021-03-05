import pytest
from src.data import data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1

# Include fixtures?
# After required functions are implemented

# Typical case
def test_function():
    data.clear()
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    channels_create_v1('auth_user_id1', 'channel1', True) #returns channel_id1 e.g.
    channel_invite_v1('auth_user_id1', 'channel_id1', 'auth_user_id2')
    assert channel_details_v1('auth_user_id2', 'channel_id1') == {
        'name': 'channel1',
        'owners': [
            {
                'u_id': 'auth_user_id1',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
        'members': [
            {
                'u_id': 'auth_user_id2',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            }
        ],
    }

# Channel_details printing a lot of data
def test_many_channel_members():
    data.clear()
    for i in range(10):
        auth_register_v1(f'example{i}@hotmail.com', f'password{i}', f'first_name{i}', f'last_name{i}')
    channels_create_v1('auth_user_id0', 'channel0', True) #returns channel_id0 e.g.
    for i in range(1,10):
        channel_invite_v1('auth_user_id0', 'channel0', f'auth_user_id{i}')
    assert channel_details_v1('auth_user_id0', 'channel_id0') == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': 'auth_user_id0',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': 'auth_user_id1',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': 'auth_user_id2',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': 'auth_user_id3',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': 'auth_user_id4',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
            {
                'u_id': 'auth_user_id5',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            },
            {
                'u_id': 'auth_user_id6',
                'name_first': 'first_name6',
                'name_last': 'last_name6',
            },
            {
                'u_id': 'auth_user_id7',
                'name_first': 'first_name7',
                'name_last': 'last_name7',
            },
            {
                'u_id': 'auth_user_id8',
                'name_first': 'first_name8',
                'name_last': 'last_name8',
            },
            {
                'u_id': 'auth_user_id9',
                'name_first': 'first_name9',
                'name_last': 'last_name9',
            },
        ],
    }

# Channel_details given channel id belonging to a non-existent channel
def test_invalid_channel_id():
    data.clear()
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    with pytest.raises(InputError):
        channel_details_v1('auth_user_id1', 'channel_id1')

# Channel_details executed by user not in given channel
def test_unauthorized_user():
    data.clear()
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    channels_create_v1('auth_user_id1', 'channel1', True) #returns channel_id1 e.g.
    with pytest.raises(AccessError):
        channel_details_v1('auth_user_id2', 'channel_id1')