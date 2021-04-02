from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        'token': user["token"],
        'u_ids': u_ids_list
    }

def test_channels_create_access_error(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    print(u_id_list)
    print(dm_create_body(users['user1'],u_id_list))
    dm_id1 = requests.post(config.url + '/dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    print(dm_id1)

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + '/auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + '/message/senddm/v1', json={
        'token': invalid_token,
        'dm_id': dm_id1,
        'message': "Hello",
    }).status_code == 403

# error when creating a channel name longer than 20 characters
def test_channels_create_input_error(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + '/dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # Ensure input error: Message over 1000 characters
    requests.post(config.url + '/message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': long_message,
    }).status_code == 400

# Testing for 1 message being sent by user1
def test_message_senddm_v1_send_one(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + '/dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + '/message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    dm1_messages = requests.get(config.url + '/dm/messages/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0,
    }).json()

    assert dm1_messages['messages'][0]['message'] == "Hello"