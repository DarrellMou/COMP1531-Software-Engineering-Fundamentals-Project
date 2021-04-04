# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

################ Tests admin_userpermission_change route #################
                                                        
#   * uses pytest fixtures from http_tests.__init__.py                                   
                                                                                                                                                
##########################################################################

# Checks invalid token
def test_admin_userpermission_change_invalid_token(setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': invalid_token,
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 403


# Checks invalid u_id
def test_admin_userpermission_change_invalid_uid(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': "Invalid u_id",
        'permission_id': 2,
    }).status_code == 400


# Checks invalid owner access
def test_admin_userpermission_change_invalid_owner(setup_user_data):
    users = setup_user_data
    
    # Ensure AccessError
    assert requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 403


# Checks invalid removal as user is the only owner
def test_admin_userpermission_change_only_owner(setup_user_data):
    users = setup_user_data
    
    # Ensure InputError
    assert requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user1']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 400


# Checks basic test of changing a member into owner
def test_admin_userpermission_change_basic(setup_user_data):
    users = setup_user_data

    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    channel_id2 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user3']['token'],
        'name': "Test Channel",
        'is_public': False,
    }).json()

    assert requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
    }).status_code == 403

    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()


# Asserts that member turned owner can join private channels and add other owners
def test_admin_userpermission_change_join_private_channels(setup_user_data):
    users = setup_user_data

    # User 1 makes channel 1
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': False,
    }).json()

    # Raises AccessError when user2 joins private channel 1
    assert requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
    }).status_code == 403

    # Global User 1 changes Member User 2 into Global owner
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    # Global User 2 should be able to join private channel now
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # Global User 2 invites User 3
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user3']['auth_user_id']
    }).json()

    # Global User 2 makes User 3 an owner of the channel
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user3']['auth_user_id']
    }).json()


# Asserts that member turned owner can change the user permission of the original global owner
def test_admin_userpermission_change_ogowner(setup_user_data):
    users = setup_user_data

    # Global User 1 changes Member User 2 into Global owner
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    # Global User 2 changes Member User 1 into member
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
        'permission_id': 2,
    }).json()

    # Global User 2 changes itself into member
    assert requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 400
