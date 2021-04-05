# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

# error when listing channels with an invalid token
def test_channels_list_access_error(setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.get(config.url + 'channels/list/v2', params={
        'token': invalid_token,
    }).status_code == 403


# listing channels with joined
def test_channels_list_empty(setup_user_data):
    users = setup_user_data

    assert requests.get(config.url + 'channels/list/v2', params={
        'token': users['user1']['token'],
    }).json() == {'channels': []}


# listing a single channel
def test_channels_list_single(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # ensure channels_listall returns correct values
    channel_list = requests.get(config.url + 'channels/list/v2', params={
        'token': users['user1']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Basic Stuff'


# listing multiple channels
def test_channels_list_multiple(setup_user_data):
    users = setup_user_data

    channel_id3 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': 'Public3',
        'is_public': True,
    }).json()

    channel_id4 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': 'Private4',
        'is_public': False,
    }).json()

    channel_id5 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': 'Public5',
        'is_public': True,
    }).json()

    # ensure channels_list returns correct values
    channel_list = requests.get(config.url + 'channels/list/v2', params={
        'token': users['user2']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public3'

    assert channel_list['channels'][1]['channel_id'] == channel_id4['channel_id']
    assert channel_list['channels'][1]['name'] == 'Private4'

    assert channel_list['channels'][2]['channel_id'] == channel_id5['channel_id']
    assert channel_list['channels'][2]['name'] == 'Public5'
