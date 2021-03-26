import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.error import InputError, AccessError
from src.other import clear_v1


# listing channels with invalid token
def test_channels_listall_invalid_user():

    with pytest.raises(AccessError):
        channels_listall_v2("invalid a_u_id")

# listing channels with none created
def test_channels_listall_empty(setup_user):

    users = setup_user

    assert channels_listall_v2(users['user3']['token']) == {'channels': []}

# listing a single channel
def test_channels_listall_single(setup_user):

    users = setup_user

    channel_id3 = channels_create_v2(users['user3']['token'], 'Public3', True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v2(users['user3']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public3'

# listing multiple channels
def test_channels_listall_multiple(setup_user):

    users = setup_user

    channel_id3 = channels_create_v2(users['user3']['token'], 'Public3', True)
    channel_id4 = channels_create_v2(users['user2']['token'], 'Private4', False)
    channel_id5 = channels_create_v2(users['user1']['token'], 'Public5', True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v2(users['user3']['token'])

    assert channel_list['channels'][0]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public3'

    assert channel_list['channels'][1]['channel_id'] == channel_id4['channel_id']
    assert channel_list['channels'][1]['name'] == 'Private4'

    assert channel_list['channels'][2]['channel_id'] == channel_id5['channel_id']
    assert channel_list['channels'][2]['name'] == 'Public5'


    