# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

import pytest
from src.error import InputError, AccessError
from src.data import retrieve_data

from src.auth import auth_register_v1
from src.channel import channel_join_v2, channel_details_v2, channel_addowner_v1
from src.channels import channels_create_v2, channels_list_v2
from src.other import clear_v1

# Helper function to set up users
def setup_users():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first3', 'last3')

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
    }

#Cases start here

# Member made owner
def test_member_to_owner():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    # Expect a list containing channel 1
    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }

# Outsider made owner
def test_outsider_to_owner():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }

# Dream owner can designate owners for servers not owned
def test_dream_owner():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']
    chid1 = channels_create_v2(a_u_id2['token'], 'channel1', True) #Public channel created
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id3['auth_user_id'])

    assert channel_details_v2(a_u_id2['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'email': 'temp3@gmail.com',
                'name_first': 'first3',
                'name_last': 'last3',
                'handle_str': 'first3last3'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'email': 'temp3@gmail.com',
                'name_first': 'first3',
                'name_last': 'last3',
                'handle_str': 'first3last3'
            }
        ],
    }

# InputError-Channel ID is invalid
def test_invalid_channel():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']
    channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    with pytest.raises(InputError):
        channel_addowner_v1(a_u_id1['token'], -1111, a_u_id2['auth_user_id'])

# InputError-u_id is already an owner
def test_invalid_uid():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    chid1 = channels_create_v2(a_u_id2['token'], 'channel1', True) #Public channel created
    with pytest.raises(InputError):
        channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

# AccessError-Authorised user is neither an owner of Dreams or the channel
def test_invalid_auth_user():
    setup = setup_users()
    a_u_id1 = setup['user1']
    a_u_id2 = setup['user2']
    a_u_id3 = setup['user3']
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    with pytest.raises(AccessError):
        channel_addowner_v1(a_u_id2['token'], chid1['channel_id'], a_u_id3['auth_user_id'])
