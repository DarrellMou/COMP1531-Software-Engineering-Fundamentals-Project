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
    channel_join_v1('auth_user_id2', 'channel_id1')
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
    auth_register_v1('example0@hotmail.com', 'password0', 'first_name0', 'last_name0') #returns auth_user_id0 e.g.
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3') #returns auth_user_id3 e.g.
    auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4') #returns auth_user_id4 e.g.
    auth_register_v1('example5@hotmail.com', 'password5', 'first_name5', 'last_name5') #returns auth_user_id5 e.g.
    auth_register_v1('example6@hotmail.com', 'password6', 'first_name6', 'last_name6') #returns auth_user_id6 e.g.
    auth_register_v1('example7@hotmail.com', 'password7', 'first_name7', 'last_name7') #returns auth_user_id7 e.g.
    auth_register_v1('example8@hotmail.com', 'password8', 'first_name8', 'last_name8') #returns auth_user_id8 e.g.
    auth_register_v1('example9@hotmail.com', 'password9', 'first_name9', 'last_name9') #returns auth_user_id9 e.g.
    channels_create_v1('auth_user_id0', 'channel0', True) #returns channel_id0 e.g.
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id1')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id2')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id3')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id4')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id5')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id6')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id7')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id8')
    channel_invite_v1('auth_user_id0', 'channel0', 'auth_user_id9')
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