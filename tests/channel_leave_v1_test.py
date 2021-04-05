# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

import pytest

from src.error import InputError, AccessError
from src.channel import channel_leave_v1, channel_join_v2
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v2
from src.other import clear_v1

# error when leaving a channel with an invalid token
def test_channel_leave_token_access_error(setup_user):
    users = setup_user

    channel_id1 = channels_create_v2(users['user1']['token'], "Channel", True)

    with pytest.raises(AccessError):
        channel_leave_v1("invalid token", channel_id1['channel_id'])


# error when member leaving a channel they are not in
def test_channel_leave_access_error(setup_user):
    users = setup_user

    channel_id1 = channels_create_v2(users['user1']['token'], "Channel", True)

    with pytest.raises(AccessError):
        channel_leave_v1(users['user2']['token'], channel_id1['channel_id'])


# error when channel id is invalid
def test_channel_leave_input_error(setup_user):
    users = setup_user

    with pytest.raises(InputError):
        channel_leave_v1(users['user1']['token'], 1234)


# assert channel still exists if there are no members left
def test_channel_leave_basic_channel(setup_user):
    users = setup_user

    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    
    channel_leave_v1(users['user1']['token'], channel_id1['channel_id'])

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v2(users['user3']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'


# assert channel is no longer in user's channel list
def test_channel_leave_basic_user(setup_user):
    users = setup_user

    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)

    channel_id2 = channels_create_v2(users['user3']['token'], "Private Channel", False)

    channel_join_v2(users['user1']['token'], channel_id2['channel_id'])
    
    channel_leave_v1(users['user1']['token'], channel_id1['channel_id'])

    # ensure channels_listall returns correct values
    channel_list = channels_list_v2(users['user1']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][0]['name'] == 'Private Channel'