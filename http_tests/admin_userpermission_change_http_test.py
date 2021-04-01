from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

# Checks invalid token
def test_admin_userpermission_change_invalid_token(setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + '/auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + '/admin/userpermission/change/v1', json={
        'token': invalid_token,
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 403

# Checks invalid u_id
def test_admin_userpermission_change_invalid_uid(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.post(config.url + '/admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': "Invalid u_id",
        'permission_id': 2,
    }).status_code == 400

# Checks invalid owner access
def test_admin_userpermission_change_invalid_owner(setup_user_data):
    users = setup_user_data
    
    # Ensure AccessError
    assert requests.post(config.url + '/admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 403

# Checks invalid removal as user is the only owner
def test_admin_userpermission_change_only_owner(setup_user_data):
    users = setup_user_data
    
    # Ensure InputError
    assert requests.post(config.url + '/admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user1']['auth_user_id'],
        'permission_id': 2,
    }).status_code == 400

# Checks basic test of changing a member into owner
def test_admin_userpermission_change_basic(setup_user_data):
    users = setup_user_data

    channel_id1 = requests.post(config.url + '/channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    channel_id2 = requests.post(config.url + '/channels/create/v2', json={
        'token': users['user3']['token'],
        'name': "Test Channel",
        'is_public': False,
    }).json()

    requests.post(config.url + '/channels/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    requests.post(config.url + '/admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    requests.post(config.url + '/channels/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()

