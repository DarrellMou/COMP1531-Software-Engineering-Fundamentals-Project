import pytest
from src.data import data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1

#Cases start here

#Standard Case, pass expected
def test_standard():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel created
    channel_join_v1('auth_user_id2', 'channel_id1')
    
    # Will validate by asserting channels_list_v1, may use different function
    assert channels_list_v1('auth_user_id2') == {
        'channels': [
            {
                'channel_id': 1
                'name': 'channel1'
            },
        ],
    }

#Case where a user joins multiple channels
def test_multiple_channels_joined():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel1 created
    channels_create_v1('auth_user_id1', 'channel2', True) #Public channel2 created
    channels_create_v1('auth_user_id1', 'channel3', True) #Public channel3 created
    channel_join_v1('auth_user_id2', 'channel_id1')
    channel_join_v1('auth_user_id2', 'channel_id2')
    channel_join_v1('auth_user_id2', 'channel_id3')

    # Will validate by asserting channels_list_v1, may use different function
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

#Case where multiple users join one channel
def test_multiple_joiners():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    auth-auth_register_v1('temp3@gmail.com','pw3','first3','last3') #auth_user_id3 created
    auth-auth_register_v1('temp4@gmail.com','pw4','first4','last4') #auth_user_id4 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel1 created
    channel_join_v1('auth_user_id2', 'channel_id1')
    channel_join_v1('auth_user_id3', 'channel_id1')
    channel_join_v1('auth_user_id4', 'channel_id1')

    # Will validate by asserting channels_details_v1, may use different function
    assert channel_details_v1('auth_user_id0', 'channel_id0') == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': 'auth_user_id1',
                'name_first': 'first1',
                'name_last': 'last1',
            }
        ],
        'all_members': [
            {
                'u_id': 'auth_user_id2',
                'name_first': 'first2',
                'name_last': 'last2',
            },
            {
                'u_id': 'auth_user_id3',
                'name_first': 'first3',
                'name_last': 'last3',
            },
            {
                'u_id': 'auth_user_id4',
                'name_first': 'first4',
                'name_last': 'last4',
            },
        ],
    }

#(TODO)Assumption Case: A user who is already a member of a channel attempts to join

#(TODO)Assumption Case: A user who is already an owner of a channel attempts to join

#Case where user attempts to join a private channel (Access Error)
def test_private_channel():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', False) #Private channel created

    with pytest.raises(AccessError):
        channel_join_v1('auth_user_id2', 'channel_id1') #Channel_id1 is a private channel

#Case where channel_join is given the id of a non-existent channel
def test_invalid_channel():
    data.clear()
    auth-auth_register_v1('temp1@gmail.com','pw1','first1','last1') #auth_user_id1 created
    auth-auth_register_v1('temp2@gmail.com','pw2','first2','last2') #auth_user_id2 created
    channels_create_v1('auth_user_id1', 'channel1', True) #Public channel created

    with pytest.raises(InputError):
        channel_join_v1('auth_user_id2', 'channel_id2') #Channel_id2 doesn't exist