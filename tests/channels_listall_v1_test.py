import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
    
def setup_user():
    
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

# listing channels with invalid auth_user_id
def test_channels_listall_invalid_user():

    with pytest.raises(AccessError):
        channels_listall_v1("invalid a_u_id")

# listing channels with none created
def test_channels_listall_empty():
    users = setup_user()

    assert channels_listall_v1(users['user3']) == {'channels': []}

# listing a single channel
def test_channels_listall_single():
    users = setup_user()

    channel_id3 = channels_create_v1(users['user3'], 'Public3', True)

    # ensure channels_listall returns correct values
    channel_list = channels_listall_v1(users['user3'])

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id_3']
    assert channel_list['channels'][0]['name'] == 'Public3'



