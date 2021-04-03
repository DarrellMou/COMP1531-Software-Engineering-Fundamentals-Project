from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

###      HELPER FUNCTIONS      ###

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        'token': user["token"],
        'u_ids': u_ids_list
    }

###     END HELPER FUNCTIONS   ###

# Testing for query when a user is not in the channel
def test_search_no_channel(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()

    search_none = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "A message in no channels"
    }).json()

    assert len(search_none) == 0

# Testing the standard case in returning queries for a user in both a channel and a dm
def test_search_standard(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()

    # User 1 invites User 2 to channel 1
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id']
    }).json()

    # User 2 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()

    # User 2 creates a dm to User 3. User 2 sends a message
    u_id_list = [users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user2'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "A message in channels",
    }).json()

    search_message = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "message"
    }).json()

    assert len(search_message) == 3

# Assumption: search_v2 is case sensitive
# Testing the function returns nothing evne when its the same letters
def test_search_case_sensitive(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()

    # User 1 invites User 2 to channel 1
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id']
    }).json()

    # User 2 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()

    search_message = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "Channels"
    }).json()

    assert len(search_message) == 0

# Testing a query of more than 1000 characters
def test_search_too_long(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "A message in no channels"
    }).json()    

    # Query over 1000 chars call input error
    assert requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "To manage the transition from trimesters to hexamesters in 2020, UNSW has \
                    established a new focus on building an in-house digital collaboration and \
                    communication tool for groups and teams to support the high intensity \
                    learning environment.Rather than re-invent the wheel, UNSW has decided that \
                    it finds the functionality of Microsoft Teams to be nearly exactly what it \
                    needs. For this reason, UNSW has contracted out Penguin Pty Ltd (a small \
                    software business run by Hayden) to build the new product. In UNSW's attempt \
                    to try and add a lighter not to the generally fatigued and cynical student \
                    body, they have named their UNSW-based product UNSW Dreams (or just Dreams \
                    for short). UNSW Dreams is the communication tool that allows you to share, \
                    communication, and collaborate to (attempt to) make dreams a reality.Penguin \
                    Pty Ltd has sub-contracted two software firms: BlueBottle Pty Ltd (two \
                    software developers, Andrea and Andrew, who will build the initial web-based \
                    GUI), YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in \
                    21T1), who will build the backend python server and possibly assist in the \
                    GUI later in the project"
    }).status_code == 400

# Testing that search_v2 no longer returns the query in the channel the user left
def test_search_leave_channel(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json()  

    # User 1 invites User 2 to channel 1
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id']
    }).json()

    # User 2 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Hi channel"
    }).json()

    # User 3 joins channel 1
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # User 3 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Hi channel"
    }).json()

    # User 2 creates a dm to User 3. User 2 sends a message
    u_id_list = [users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user2'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "A message in channels",
    }).json()

    search_message = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "channel"
    }).json()

    assert len(search_message) == 4

    # User 2 leaves channel 1
    requests.post(config.url + 'channel/leave/v1', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
    })

    search_again = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "channel"
    }).json()

    assert len(search_again) == 1

# Testing that search_v2 no longer returns the query in the dm the user left
def test_search_leave_dm(setup_user_data):
    users = setup_user_data

    # User 1 creates a channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Test Channel",
        'is_public': True,
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome to channel"
    }).json() 

    # User 1 invites User 2 to channel 1
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id']
    }).json()

    # User 2 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Hi channel"
    }).json()

    # User 3 joins channel 1
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # User 3 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Hi channel"
    }).json()

    # User 2 creates a dm to User 3. User 2 sends a message
    u_id_list = [users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user2'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "A message in channels",
    }).json()

    search_message = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "channel"
    }).json()

    assert len(search_message) == 4

    # User 2 leaves dm 1
    requests.post(config.url + 'dm/leave/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
    })

    search_again = requests.get(config.url + 'search/v2', json={
        'token': users['user2']['token'],
        'query_str': "channel"
    }).json()

    assert len(search_again) == 3
