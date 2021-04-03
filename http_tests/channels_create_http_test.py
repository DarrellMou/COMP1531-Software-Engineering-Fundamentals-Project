from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config


def test_channels_create_access_error(setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']

    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + 'channels/create/v2', json={
        'token': invalid_token,
        'name': 'Name',
        'is_public': True,
    }).status_code == 403

# error when creating a channel name longer than 20 characters
def test_channels_create_input_error(setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure input error: Public channel with namesize > 20 characters
    requests.post(config.url + 'channels/create/v2', json={
        'token': invalid_token,
        'name': 'wayyyytoolongggggoffffffaaaaaanameeeeeeee',
        'is_public': True,
    }).status_code == 400

    # Ensure input error: Private channel with namesize > 20 characters
    requests.post(config.url + 'channels/create/v2', json={
        'token': invalid_token,
        'name': 'wayyyytoolongggggoffffffaaaaaanameeeeeeee',
        'is_public': False,
    }).status_code == 400

# create channels of the same name
def test_channels_create_same_name(setup_user_data):

    users = setup_user_data
    
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    channel_id2 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    # ensure channels_listall returns correct values
    channel_list = requests.get(config.url + 'channels/listall/v2', json={
        'token': users['user3']['token'],
    }).json()

    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'

    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][1]['name'] == 'Public Channel'

# create channel with valid data
def test_channels_create_valid_basic(setup_user_data):
 
    users = setup_user_data

    # Creating a basic public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Basic Stuff",
        'is_public': True,
    }).json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    channel_details = requests.get(config.url + 'channel/details/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()
    print(channel_details)

    assert channel_details['name'] == 'Basic Stuff'
    assert channel_details['owner_members'][0]['u_id'] == users['user1']['auth_user_id']
    assert channel_details['owner_members'][0]['name_first'] == 'user1_first'
    assert channel_details['owner_members'][0]['name_last'] == 'user1_last'
    assert channel_details['all_members'][0]['u_id'] == users['user1']['auth_user_id']
    assert channel_details['all_members'][0]['name_first'] == 'user1_first'
    assert channel_details['all_members'][0]['name_last'] == 'user1_last'

