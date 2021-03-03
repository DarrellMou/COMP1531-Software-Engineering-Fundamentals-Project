import pytest

from src.error import InputError
from src.error import AccessError

from src.channel import channel_details_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1

def test_authorized_user_and_valid_channel_id():
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    channels_create_v1('auth_user_id1', 'channel1', True)
    channel_join_v1('auth_user_id2', 'channel1')
    assert channel_details_v1('auth_user_id2', 'channel1') == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            }
        ],
    }

def test_authorized_user_and_invalid_channel_id():
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    with pytest.raises(InputError):
        channel_details_v1('auth_user_id1', 'channel1')

def test_unauthorized_user_and_valid_channel_id():
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    channels_create_v1('auth_user_id1', 'channel1', True)
    with pytest.raises(AccessError):
        channel_details_v1('auth_user_id2', 'channel1')

def test_unauthorized_user_and_invalid_channel_id():
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    with pytest.raises(InputError):
        channel_details_v1('auth_user_id2', 'channel1')

def test_many_channel_members():
    auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1') #returns auth_user_id1 e.g.
    auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2') #returns auth_user_id2 e.g.
    auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3') #returns auth_user_id3 e.g.
    auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4') #returns auth_user_id4 e.g.
    auth_register_v1('example5@hotmail.com', 'password5', 'first_name5', 'last_name5') #returns auth_user_id5 e.g.
    channels_create_v1('auth_user_id1', 'channel1', True)
    channel_join_v1('auth_user_id2', 'channel1')
    channel_join_v1('auth_user_id3', 'channel1')
    channel_join_v1('auth_user_id4', 'channel1')
    channel_join_v1('auth_user_id5', 'channel1')
    assert channel_details_v1('auth_user_id2', 'channel1') == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': 3,
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': 4,
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
            {
                'u_id': 5,
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            },
        ],
    }