from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

# Checks invalid token
def test_admin_user_remove_invalid_token(setup_user_data):
    users = setup_user_data
    
    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + '/auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.delete(config.url + '/admin/user/remove/v1', json={
        'token': invalid_token,
        'u_id': users['user2']['auth_user_id'],
    }).status_code == 403

# Checks invalid auth_user_id
def test_admin_user_remove_invalid_uid(setup_user_data):
    users = setup_user_data
    
    # Ensure InputError
    assert requests.delete(config.url + '/admin/user/remove/v1', json={
        'token': users['user1']['token'],
        'u_id': "Invalid user",
    }).status_code == 400

# Checks invalid owner access
def test_admin_user_remove_invalid_owner(setup_user_data):
    users = setup_user_data

    # Ensure AccessError
    assert requests.post(config.url + '/admin/user/remove/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 403

# Checks invalid removal as user is the only owner
def test_admin_user_remove_only_owner(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.delete(config.url + '/admin/user/remove/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 400
'''
# Checks invalid removal as user is the only channel owner
def test_admin_user_remove_only_channel_owner(setup_user_data):
    users = setup_user_data

    channel_id1 = channels_create_v2(users['user1']['token'],'Test Channel',True)
    channel_id2 = channels_create_v2(users['user2']['token'],'Test Channel',False)
    channel_join_v2(users['user3']['token'], channel_id1['channel_id'])
    channel_join_v2(users['user1']['token'], channel_id2['channel_id'])

    with pytest.raises(InputError):
        admin_user_remove_v1(users['user1']['token'], users['user2']['auth_user_id'])
'''