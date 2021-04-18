# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

###################### Tests message_senddm route #########################
                                                         
#   * uses pytest fixtures from http_tests/conftest.py                                 
                                                                                                                                                
###########################################################################

###                         HELPER FUNCTIONS                           ###

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        'token': user["token"],
        'u_ids': u_ids_list
    }

###                       END HELPER FUNCTIONS                         ###
 

def test_message_senddm_v1_access_error(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.post(config.url + 'message/senddm/v1', json={
        'token': invalid_token,
        'dm_id': dm_id1,
        'message': "Hello",
    }).status_code == 403


# error when creating a channel name longer than 20 characters
def test_message_senddm_v1_input_error(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # Ensure input error: Message over 1000 characters
    assert requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': long_message,
    }).status_code == 400


# Testing for 1 message being sent by user1
def test_message_senddm_v1_send_one(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    dm1_messages = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0,
    }).json()

    assert dm1_messages['messages'][0]['message'] == "Hello"


# Testing for 2 identical messages being sent by user1
def test_message_senddm_v1_user_sends_identical_messages(setup_user_data):
    users = setup_user_data

    # Creating dm1
    u_id_list1 = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list1)).json()

    first_message_id = requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    # Creating dm2
    u_id_list2 = [users['user3']]
    dm_id2 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list2)).json()

    second_message_id = requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id2['dm_id'],
        'message': "Hello",
    }).json()

    # Ensure they are different dms
    assert first_message_id != second_message_id


# Testing for messages sent by multiple users
def test_message_senddm_v1_send_multiple(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello2",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user3']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello3",
    }).json()

    dm1_messages = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0,
    }).json()

    assert dm1_messages['messages'][0]['message'] == "Hello3"
    assert dm1_messages['messages'][1]['message'] == "Hello2"
    assert dm1_messages['messages'][2]['message'] == "Hello"


# Testing for messages sent by multiple users in multiple dms
def test_message_senddm_v1_send_two(setup_user_data):
    users = setup_user_data

    # Creat dm1
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello2",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user3']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello3",
    }).json()

    # Creat dm2
    u_id_list = [users['user3'],users['user4']]
    dm_id2 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id2['dm_id'],
        'message': "Bye",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user3']['token'],
        'dm_id': dm_id2['dm_id'],
        'message': "Bye2",
    }).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user4']['token'],
        'dm_id': dm_id2['dm_id'],
        'message': "Bye3",
    }).json()

    # Call dm/messages to view details
    dm1_messages = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0,
    }).json()

    # Call dm/messages to view details
    dm2_messages = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id2['dm_id'],
        'start': 0,
    }).json()

    assert dm1_messages['messages'][0]['message'] == "Hello3"
    assert dm1_messages['messages'][1]['message'] == "Hello2"
    assert dm1_messages['messages'][2]['message'] == "Hello"

    assert dm2_messages['messages'][0]['message'] == "Bye3"
    assert dm2_messages['messages'][1]['message'] == "Bye2"
    assert dm2_messages['messages'][2]['message'] == "Bye"
    