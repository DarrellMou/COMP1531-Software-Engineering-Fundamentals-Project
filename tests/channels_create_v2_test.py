import pytest

from src.channels import channels_create_v2, channels_listall_v2
from src.error import InputError, AccessError
from src.other import clear_v1

#################################################################################
#                       Tests channels_create                                   #
#   * uses pytest fixtures from src.conftest                                    #
#                                                                               #                                                                      #
#################################################################################

# error when creating a channel with an invalid token
def test_channels_create_access_error():

    with pytest.raises(AccessError):
        channels_create_v2("invalid a_u_id", "Channel", True)


# error when creating a channel name longer than 20 characters
def test_channels_create_input_error(setup_user):
    
    users = setup_user

    # public channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create_v2(users['user1']['token'], "This is longer than 20", True)

    # private channel with namesize > 20 characters
    with pytest.raises(InputError):
        channels_create_v2(users['user1']['token'], "This is longer than 20", False)


# assert channel id is an integer
def test_channels_create_return_value(setup_user):
    
    users = setup_user

    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    assert isinstance(channel_id1['channel_id'], int)


# create channels of the same name
def test_channels_create_same_name(setup_user):

    users = setup_user

    channel_id2 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    channel_id3 = channels_create_v2(users['user1']['token'], "Public Channel", True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v2(users['user3']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'

    assert channel_list['channels'][1]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][1]['name'] == 'Public Channel'


# create channel with no name 
def test_channels_create_no_name(setup_user):

    users = setup_user

    channel_id4 = channels_create_v2(users['user1']['token'], "", True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v2(users['user3']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id4['channel_id']
    assert channel_list['channels'][0]['name'] == ''

    

