# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from http_tests import * # import fixtures for pytest

import json
import requests
import urllib
import pytest

from src import config

# error when removing owners from non-existent channels
def test_channel_removeowner_channel_id_error(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': 12345,
        'u_id': users['user2']['auth_user_id'],
    }).status_code == 400

# error when removing owners from channels they are not owners of
def test_channel_removeowner_owner_error(setup_user_data):
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
    
    # Ensure InputError as user1 is currently the only owner of the channel
    assert requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 400

# error when trying to remove owners without being an owner yourself
def test_removeowner_access_error(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Join user2 as owner
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()

    # Join user3
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()
    
    # Ensure AccessError
    assert requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user3']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).status_code == 403

# error when trying to remove yourself as the only owner
def test_removesoleowner_access_error(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()
    
    # Ensure AccessError
    assert requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 400

# Test removing an owner as existing owner
def test_channel_removeowner_basic(setup_user_data):
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
    # Remove user2 from onwer pool
    requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()
    
    # Get details
    channel_details2 = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert channel_details2 == {
        'name': 'Public',
        'is_public' : True,
        'owner_members': [
            {
                'u_id': users['user1']['auth_user_id'],
                'name_first': 'user1_first',
                'name_last': 'user1_last',
            },
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

# Test removing an owner as dreams owner
def test_removeowner_dreams(setup_user_data):
    users = setup_user_data

    # Creating a public channel as user2
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
    
    # Add user3 to onwer pool
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user2']['token'],
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
    # Remove user3 from onwer pool as dreams user
    requests.post(config.url + 'channel/removeowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user3']['auth_user_id'],
    }).json()
    
    # Get details
    channel_details2 = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user2']['token'],
        'channel_id': channel_id['channel_id'],
    }).json()

    assert channel_details2 == {
        'name': 'Public',
        'is_public' : True,
        'owner_members': [
            {
                'u_id': users['user2']['auth_user_id'],
                'name_first': 'user2_first',
                'name_last': 'user2_last',
            },
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