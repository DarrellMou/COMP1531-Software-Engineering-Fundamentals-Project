# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

###################### Tests message_unreact route ########################
                                                         
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

# Define 'like' react
like = 1
unlike = 1

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ###############################

# The user attempts to unreact to a message id that doesn't exist in any of his channels
def test_unreact_v1_invalid_message_id_nonexistent_InputError(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in channel_id1
    will_remove = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 1 sends a message in dm_id1
    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    requests.delete(config.url + 'message/remove/v1', json={
        "token": users['user1']['token'],
        "message_id": will_remove["message_id"],
    }).json()
    
    # Ensure input error: Invalid message_id
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user1']['token'],
        'message_id': will_remove["message_id"],
        'react_id': unlike,
    }).status_code == 400


# The react id the user sends is not valid (currently only id 1 is valid)
def test_unreact_v1_invalid_react_id_InputError(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # User 1 sends a message in channel_id1
    message = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 1 likes his own message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user1']['token'],
        'message_id': message["message_id"],
        'react_id': like,
    }).json()

    # Ensure input error: Invalid message_id
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user1']['token'],
        'message_id': message["message_id"],
        'react_id': -99999,
    }).status_code == 400


# User has already reacted to the same message id with the same react id
def test_unreact_v1_repeat_react_InputError(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # User 1 sends a message in channel_id1
    message = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # user1 tries to unreact a message that they didn't react
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user1']['token'],
        'message_id': message["message_id"],
        'react_id': unlike,
    }).status_code == 400


# The user attempts to react to an existing message, but is not in the corresponding channel
def test_unreact_v1_invalid_message_id_inaccessible_channel_AccessError(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # User 1 sends a message in channel_id1
    message = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # user2 tries to unreact a message in a channel they not in
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user2']['token'],
        'message_id': message["message_id"],
        'react_id': unlike,
    }).status_code == 403


# The user attempts to react to an existing message, but is not in the corresponding dm
def test_unreact_v1_invalid_message_id_inaccessible_dm_AccessError(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in dm_id1
    dm_message = requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    # user4 tries to unreact a message in a dm they not in
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user4']['token'],
        'message_id': dm_message["message_id"],
        'react_id': unlike,
    }).status_code == 403


# Default access error when token is invalid
def test_message_unreact_v1_default_Access_Error(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in dm_id1
    dm_message = requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    # User 2 reacts
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user2']['token'],
        'message_id': dm_message["message_id"],
        'react_id': like,
    }).json()

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user2']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # user2 tries to react
    assert requests.post(config.url + 'message/unreact/v1', json={
        'token': invalid_token,
        'message_id': dm_message["message_id"],
        'react_id': unlike,
    }).status_code == 403

############################ END EXCEPTION TESTING ############################


########################## TESTING MESSAGE UNREACT ############################

# Testing for user unreacting to another user's in channel
def test_message_unreact_v1_channel(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # Join user2
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id']
    }).json()

    # User 1 sends a message in channel_id1
    message = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 2 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user2']['token'],
        'message_id': message["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()
    print(channel1_messages)
    assert channel1_messages['messages'][0]["reacts"][0]["u_ids"] == [users['user2']["auth_user_id"]]
    assert channel1_messages['messages'][0]["reacts"][0]["react_id"] == 1
    assert channel1_messages['messages'][0]["reacts"][0]["is_this_user_reacted"] == False

    # User 2 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user2']['token'],
        'message_id': message["message_id"],
        'react_id': unlike,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert len(channel1_messages2['messages'][0]["reacts"][0]["u_ids"]) == 0

# Testing for user unreacting to another user's in dm
def test_message_unreact_v1_dm(setup_user_data):
    users = setup_user_data

    # Creating a dm
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in dm_id1
    dm_message = requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    # User 3 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user3']['token'],
        'message_id': dm_message["message_id"],
        'react_id': like,
    }).json()

    # Check that dm details have all been set correctly
    dm1_messages = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0
    }).json()

    assert dm1_messages['messages'][0]["reacts"][0]["u_ids"] == [users['user3']["auth_user_id"]]
    assert dm1_messages['messages'][0]["reacts"][0]["react_id"] == 1
    assert dm1_messages['messages'][0]["reacts"][0]["is_this_user_reacted"] == False

    # User 3 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user3']['token'],
        'message_id': dm_message["message_id"],
        'react_id': unlike,
    }).json()

    # Check that dm details have all been set correctly
    dm1_messages2 = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0
    }).json()

    assert len(dm1_messages2['messages'][0]["reacts"][0]["u_ids"]) == 0


# Testing for user unreacting to themselves
def test_message_unreact_v1_self(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # User 1 sends a message in channel_id1
    message = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 1 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user1']['token'],
        'message_id': message["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert channel1_messages['messages'][0]["reacts"][0]["u_ids"] == [users['user1']["auth_user_id"]]
    assert channel1_messages['messages'][0]["reacts"][0]["react_id"] == 1

    # User 2 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user1']['token'],
        'message_id': message["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert len(channel1_messages2['messages'][0]["reacts"][0]["u_ids"]) == 0


# Testing for reacts on different messages
def test_message_unreact_v1_different_messages(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # Join user2
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id']
    }).json()

    # User 1 sends a message in channel_id1
    message1 = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 2 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user2']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # User 2 sends a message in channel_id1
    message2 = requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "hello sir pooh"
    }).json() 

    # User 1 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user1']['token'],
        'message_id': message2["message_id"],
        'react_id': like,
    }).json()

    # User 1 sends a message in channel_id1
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "moo me honey"
    }).json() 

    # Check that channel details have all been set correctly
    channel1_messages = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    print(channel1_messages['messages'][2])
    assert channel1_messages['messages'][0]["reacts"] == []

    assert channel1_messages['messages'][1]["reacts"][0]["u_ids"] == [users['user1']["auth_user_id"]]
    assert channel1_messages['messages'][1]["reacts"][0]["react_id"] == 1

    assert channel1_messages['messages'][2]["reacts"][0]["u_ids"] == [users['user2']["auth_user_id"]]
    assert channel1_messages['messages'][2]["reacts"][0]["react_id"] == 1

    # User 2 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user2']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert len(channel1_messages2['messages'][0]["reacts"]) == 0
    assert len(channel1_messages2['messages'][1]["reacts"][0]['u_ids']) == 1

# Testing for multiple reacts on the same message
def test_message_unreact_v1_multiple_reacts(setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).json()

    # Join user2
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id']
    }).json()

    # Join user3
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id']
    }).json()

    # User 1 sends a message in channel_id1
    message1 = requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "3 likes on this message and I die"
    }).json() 

    # User 1 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user1']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # User 2 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user2']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # User 3 likes the message
    requests.post(config.url + 'message/react/v1', json={
        'token': users['user3']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()
    print(channel1_messages['messages'][0]["reacts"][0])
    assert channel1_messages['messages'][0]["reacts"][0]["u_ids"][0] == users['user1']["auth_user_id"]
    assert channel1_messages['messages'][0]["reacts"][0]["u_ids"][1] == users['user2']["auth_user_id"]
    assert channel1_messages['messages'][0]["reacts"][0]["u_ids"][2] == users['user3']["auth_user_id"]
    assert channel1_messages['messages'][0]["reacts"][0]["react_id"] == 1

    # User 2 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user2']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # User 3 unlikes the message
    requests.post(config.url + 'message/unreact/v1', json={
        'token': users['user3']['token'],
        'message_id': message1["message_id"],
        'react_id': like,
    }).json()

    # Check that channel details have all been set correctly
    channel1_messages2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert channel1_messages2['messages'][0]["reacts"][0]["u_ids"] == [users['user1']["auth_user_id"]]
