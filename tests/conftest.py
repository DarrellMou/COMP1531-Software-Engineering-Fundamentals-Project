# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.dm import dm_create_v1

'''
The following fixtures are used 
'''

@pytest.fixture
def reset():
    clear_v1()

@pytest.fixture
def setup_user(reset):
    '''
    Nikki's fixtures used in:
        - channels/create
        - channels/listall
        - admin/userpermission/change
        - admin/user/remove
        - search
    '''
    # a_u_id* has two fields: token and auth_user_id
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


@pytest.fixture
def set_up_data(reset):
    '''
    Brendan's fixtures used in:
        - channel/messages
        - dm/messages
        - message/send
        - message/senddm
        - message/pin
        - message/unpin
        - message/sendlater
        - message/sendlaterdm
    '''
    # Populate data - create/register users 1 and 2 and have user 1 make channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password12345', 'Thomas', 'Tankengine')
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    setup = {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'channel1': channel1['channel_id'],
        'dm1': dm1['dm_id']
    }

    return setup


@pytest.fixture
def set_up_message_data(reset):
    '''
    Brendan's fixtures used in:
        - message/edit
        - message/remove
        - message/share
    '''
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1 and
    # channel2 and invite user2 to the channels
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    channel_invite_v2(user1["token"], channel1['channel_id'], user2['auth_user_id'])
    channel2 = channels_create_v2(user1['token'], 'Channel2', True)
    channel_invite_v2(user1["token"], channel2['channel_id'], user2['auth_user_id'])
    dm1 = dm_create_v1(user1["token"], [user2["auth_user_id"]])
    dm2 = dm_create_v1(user2["token"], [user1["auth_user_id"]])


    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1['channel_id'],
        "channel2": channel2['channel_id'],
        "dm1": dm1["dm_id"],
        "dm2": dm2["dm_id"]
    }

    return setup
