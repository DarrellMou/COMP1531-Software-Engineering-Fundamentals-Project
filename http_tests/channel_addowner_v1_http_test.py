# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from http_tests import * # import fixtures for pytest

import json
import requests
import urllib
import pytest

from src import config

# error when adding owners to non-existent channels
def test_channel_addowner_channel_id_error(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': 12345,
        'u_id': users['user2']['auth_user_id'],
    }).status_code == 400

# error when adding owners to channels they are already owners of
def test_channel_addowner_owner_error(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Join user2 as owner
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()
    
    # Ensure InputError
    assert requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 400

# error when trying to add owners without being an owner yourself
def test_addowner_access_error(setup_user_data):
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
        'channel_id': channel_id['channel_id'],
    }).json()

    # Join user3
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()
    
    # Ensure AccessError
    assert requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user3']['auth_user_id'],
    }).status_code == 403

# Test adding an owner as existing owner
def test_channel_join_owner_input_error(setup_user_data):
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
        'channel_id': channel_id['channel_id'],
    }).json()
    
    # Add user2 to onwer pool
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()

    # Get details
    channel_details = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert channel_details == {
        'name': 'Public',
        'is_public' : True,
        'owner_members': [
            {
                'u_id': users['user1']['auth_user_id'],
                'name_first': 'user1_first',
                'name_last': 'user1_last',
            },
            {
                'u_id': users['user2']['auth_user_id'],
                'name_first': 'user2_first',
                'name_last': 'user2_last',
            }
        ],
        'all_members': [
            {
                'u_id': users['user1']['auth_user_id'],
                'name_first': 'user1_first',
                'name_last': 'user1_last',
            },
            {
                'u_id': users['user2']['auth_user_id'],
                'name_first': 'user2_first',
                'name_last': 'user2_last',
            }
        ],
    }


# Test adding an owner as dreams owner
def test_addowner_dreams(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Join user3
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()
    
    # Add user2 to onwer pool as dreams owner
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user3']['auth_user_id'],
    }).json()

    # Get details
    channel_details = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert channel_details == {
        'name': 'Public',
        'is_public' : True,
        'owner_members': [
            {
                'u_id': users['user2']['auth_user_id'],
                'name_first': 'user2_first',
                'name_last': 'user2_last',
            },
            {
                'u_id': users['user3']['auth_user_id'],
                'name_first': 'user3_first',
                'name_last': 'user3_last',
            }
        ],
        'all_members': [
            {
                'u_id': users['user2']['auth_user_id'],
                'name_first': 'user2_first',
                'name_last': 'user2_last',
            },
            {
                'u_id': users['user3']['auth_user_id'],
                'name_first': 'user3_first',
                'name_last': 'user3_last',
            }
        ],
    }