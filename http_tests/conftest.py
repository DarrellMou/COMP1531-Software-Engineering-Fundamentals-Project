# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

import pytest
import requests
import json
from src import config

@pytest.fixture
def reset():
    requests.delete(config.url+'clear/v1')

@pytest.fixture
def setup_user_dict(reset):

    a_u_id1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }

    a_u_id2 = {
        'email': 'user2@email.com',
        'password': 'user2_pass!',
        'name_first': 'user2_first',
        'name_last': 'user2_last'
    }

    a_u_id3 = {
        'email': 'user30@email.com',
        'password': 'user3_pass!',
        'name_first': 'user3_first',
        'name_last': 'user3_last'
    }

    a_u_id4 = {
        'email': 'user4@email.com',
        'password': 'user4_pass!',
        'name_first': 'user4_first',
        'name_last': 'user4_last'
    }
    a_u_id5 = {
        'email': 'user5@email.com',
        'password': 'user5_pass!',
        'name_first': 'user5_first',
        'name_last': 'user5_last'
    }

    return {
        'user1_dict': a_u_id1,
        'user2_dict': a_u_id2,
        'user3_dict': a_u_id3,
        'user4_dict': a_u_id4,
        'user5_dict': a_u_id5
    }


@pytest.fixture
def setup_user_data(setup_user_dict):
    '''
    This fixture is used in:
        - channels/create
        - channels/listall
        - message/senddm
        - admin/userpermission/change
        - admin/user/remove
        - search
        - channel/join/v2
        - channels/list/v2,
        - channel/addowner/v1
        - channel/removeowner/v1
        - channel/leave/v1
        - notifications/get/v1
    '''
    user1 = setup_user_dict['user1_dict']
    user1_details = requests.post(config.url + "auth/register/v2", json=user1).json()

    user2 = setup_user_dict['user2_dict']
    user2_details = requests.post(config.url + "auth/register/v2", json=user2).json()

    user3 = setup_user_dict['user3_dict']
    user3_details = requests.post(config.url + "auth/register/v2", json=user3).json()

    user4 = setup_user_dict['user4_dict']
    user4_details = requests.post(config.url + "auth/register/v2", json=user4).json()

    user5 = setup_user_dict['user5_dict']
    user5_details = requests.post(config.url + "auth/register/v2", json=user5).json()
    
    return {
        'user1' : user1_details,
        'user2' : user2_details,
        'user3' : user3_details,
        'user4' : user4_details,
        'user5' : user5_details
    }

@pytest.fixture
def set_up_data(setup_user_dict):
    '''
    This fixture is used in:
        - channel/messages
        - message/send
        - message/pin
        - message/unpin
        - message/sendlater
        - message/sendlaterdm
    '''
    user1_dict = setup_user_dict['user1_dict']
    user1 = requests.post(config.url + "auth/register/v2", json=user1_dict).json()

    user2_dict = setup_user_dict['user2_dict']
    user2 = requests.post(config.url + "auth/register/v2", json=user2_dict).json()

    user3_dict = setup_user_dict['user3_dict']
    user3 = requests.post(config.url + "auth/register/v2", json=user3_dict).json()

    channel1 = requests.post(f"{config.url}channels/create/v2",
        json={
            "token": user1["token"],
            "name": "channel1",
            "is_public": True
        }).json()

    dm1 = requests.post(f"{config.url}dm/create/v1",
        json={
            "token": user1["token"],
            "u_ids": [user2["auth_user_id"]]
        }).json()

    setup = {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'channel1': channel1['channel_id'],
        'dm1': dm1['dm_id']
    }

    return setup

@pytest.fixture
def set_up_message_data(setup_user_dict):
    '''
    This fixture is used in:
        - message/edit
        - message/remove
        - message/share
    '''
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1 and
    # channel2 and invite user2 to the channels
    user1_dict = setup_user_dict['user1_dict']
    user1 = requests.post(config.url + "auth/register/v2", json=user1_dict).json()

    user2_dict = setup_user_dict['user2_dict']
    user2 = requests.post(config.url + "auth/register/v2", json=user2_dict).json()

    channel1 = requests.post(f"{config.url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    requests.post(f"{config.url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user2["auth_user_id"]
    }).json()

    channel2 = requests.post(f"{config.url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel2",
        "is_public": True
    }).json()

    requests.post(f"{config.url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "u_id": user2["auth_user_id"]
    }).json()

    dm1 = requests.post(f"{config.url}dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [user2["auth_user_id"]]
    }).json()

    dm2 = requests.post(f"{config.url}dm/create/v1", json = {
        "token": user2["token"],
        "u_ids": [user1["auth_user_id"]]
    }).json()

    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1["channel_id"],
        "channel2": channel2["channel_id"],
        "dm1": dm1["dm_id"],
        "dm2": dm2["dm_id"]
    }

    return setup
