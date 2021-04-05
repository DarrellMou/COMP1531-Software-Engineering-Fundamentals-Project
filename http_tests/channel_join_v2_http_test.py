# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from http_tests import * # import fixtures for pytest

import json
import requests
import urllib
import pytest

from src import config

# error when joining non-existent channels
def test_channel_join_input_error(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + 'channel/join/v2', json={
        'token': users['user1']['token'],
        'channel_id': 12345
    }).status_code == 400

# error when joining private channels
def test_channel_join_access_error(setup_user_data):
    users = setup_user_data

    # Creating a private channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Private',
        'is_public': False,
    }).json()

    # Ensure AccessError
    assert requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id']
    }).status_code == 403

# Test joining a public channel
def test_channels_join_basic(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Join user2
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id']
    }).json()

    # Ensure user2 is properly joined
    channel_list = requests.get(config.url + 'channels/list/v2', params={
        'token': users['user2']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public'

# Test joining a private channel as dreams owner
def test_channels_join_dreams(setup_user_data):
    users = setup_user_data

    # Creating a private channel as user2
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': 'Private',
        'is_public': False,
    }).json()

    # Join user1 (Dreams owner)
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id']
    }).json()

    # Ensure user2 is properly joined
    channel_list = requests.get(config.url + 'channels/list/v2', params={
        'token': users['user1']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Private'