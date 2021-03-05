import pytest
from src.data import data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1

#Cases start here

#Standard Case, only one channel joined
def test_standard():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel created
    channel_join_v1('auth_user_id2', 'channel_id1')
    
    assert channels_list_v1('auth_user_id2') == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'channel1',
            },
        ],
    }
#Case where a user joins multiple channels
def test_multiple_channels():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel1 created
    channels_create_v1('auth_user_id1', 'channel2', True) #Public channel2 created
    channels_create_v1('auth_user_id1', 'channel3', True) #Public channel3 created
    channel_join_v1('auth_user_id2', 'channel_id1')
    channel_join_v1('auth_user_id2', 'channel_id2')
    channel_join_v1('auth_user_id2', 'channel_id3')

    assert channels_list_v1('auth_user_id2') == {
        'channels': [
            {
                'channel_id': 1,
                'name': 'channel1',
            },
            {
                'channel_id': 2,
                'name': 'channel2',
            },
            {
                'channel_id': 3,
                'name': 'channel3',
            },
        ],
    }

#Case where user is valid, but is a member of no channels
def test_memberless():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created

    assert channels_list_v1('auth_user_id1') == {
        'channels': [

        ],
    }

#Assumptions, users don't have to be in a channel