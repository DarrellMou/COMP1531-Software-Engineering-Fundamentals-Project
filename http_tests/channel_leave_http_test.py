# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

###################### Tests channel_leave route #########################
                                                         
#   * uses pytest fixtures from http_tests.__init__.py                                   
                                                                                                                                                
##########################################################################


# error when leaving a channel with an invalid token
def test_channel_leave_token_access_error(setup_user_data):
    users = setup_user_data

    # Create a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Name',
        'is_public': True,
    }).json()
    
    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']

    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + 'channel/leave/v1', json={
        'token': invalid_token,
        'channel_id': channel_id1['channel_id'],
    }).status_code == 403


# error when member leaving a channel they are not in
def test_channel_leave_access_error(setup_user_data):
    users = setup_user_data

    # Create a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Name',
        'is_public': True,
    }).json()

    # Ensure AccessError
    assert requests.post(config.url + 'channel/leave/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
    }).status_code == 403


# error when channel id is invalid
def test_channel_leave_input_error(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + 'channel/leave/v1', json={
        'token': users['user2']['token'],
        'channel_id': 1234,
    }).status_code == 400


# assert channel still exists if there are no members left
def test_channel_leave_basic_channel(setup_user_data):
    users = setup_user_data

    # Create a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    # User 1 leaves channel 1
    requests.post(config.url + 'channel/leave/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # ensure channels_listall returns correct values
    channel_list = requests.get(config.url + 'channels/listall/v2', params={
        'token': users['user3']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'


# assert channel is no longer in user's channel list
def test_channel_leave_basic_user(setup_user_data):
    users = setup_user_data

    # Create channel 1
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    # Create channel 2
    channel_id2 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user3']['token'],
        'name': "Private Channel",
        'is_public': False,
    }).json()

    # User 1 join channel 2
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()

    # User 1 leaves channel 1
    requests.post(config.url + 'channel/leave/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # ensure channels_list returns correct values
    channel_list = requests.get(config.url + 'channels/list/v2', params={
        'token': users['user1']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][0]['name'] == 'Private Channel'
