import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.data import reset_data

def setup_user():
    reset_data()

    a_u_id1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    a_u_id2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    a_u_id3 = auth_register_v1('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    a_u_id4 = auth_register_v1('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
    a_u_id5 = auth_register_v1('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

    return {
        'user1' : a_u_id1,
        'user2' : a_u_id2,
        'user3' : a_u_id3,
        'user4' : a_u_id4,
        'user5' : a_u_id5
    }


# error when creating a channel with an invalid auth_user_id
def test_channels_create_access_error():

    with pytest.raises(AccessError):
        channels_create_v1("invalid a_u_id", "Channel", True)


# error when creating a channel name longer than 20 characters
def test_channels_create_input_error():
    
    users = setup_user()

    # public channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create_v1(users['user1']['auth_user_id'], "This is longer than 20", True)

    # private channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create_v1(users['user1']['auth_user_id'], "This is longer than 20", False)


# assert channel id is an integer
def test_channels_create_return_value():
    
    users = setup_user()

    channel_id1 = channels_create_v1(users['user1']['auth_user_id'], "Public Channel", True)
    assert isinstance(channel_id1['channel_id'], int)


# create channels of the same name
def test_channels_create_same_name():

    users = setup_user()

    channel_id2 = channels_create_v1(users['user1']['auth_user_id'], "Public Channel", True)
    channel_id3 = channels_create_v1(users['user1']['auth_user_id'], "Public Channel", True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v1(users['user3']['auth_user_id'])

    assert channel_list['channels'][0]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'

    assert channel_list['channels'][1]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][1]['name'] == 'Public Channel'


# create channel with no name 
def test_channels_create_no_name():

    users = setup_user()

    channel_id4 = channels_create_v1(users['user1']['auth_user_id'], "", True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v1(users['user3']['auth_user_id'])

    assert channel_list['channels'][0]['channel_id'] == channel_id4['channel_id']
    assert channel_list['channels'][0]['name'] == ''


'''
# test private channel 
def test_channels_create_private():
    users = setup_user()

    channel_id2 = channels_create_v1(users['user1']['auth_user_id'], "Private Channel", False)

    # ensure a non-member cannot join private channel
    with pytest.raises(AccessError):
        channel_join_v1(users['user2'], channel_id_2)
'''



    

