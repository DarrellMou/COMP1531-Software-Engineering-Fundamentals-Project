# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

########################## Tests user_stats route #########################
                                                         
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

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################


# Default access error when token is invalid
def test_user_stats_v1_default_Access_Error():

    requests.get(config.url + 'user/stats/v1', params={
        'token': "imposter",
    }).status_code = 403


############################ END EXCEPTION TESTING ############################


############################# TESTING USER STATS #############################

# Test stats when only users exist, but no boards of discussion
def test_user_stats_v1_empty(setup_user_data):
    users = setup_user_data

    user_stats = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user1']['token'],
    }).json()
    assert user_stats['num_channels_joined'] == 0
    assert user_stats['num_dms_joined'] == 0
    assert user_stats['num_msgs_sent'] == 0
    assert user_stats['involvement'] == 0


# Test stats when one user has all of the involvement
def test_user_stats_v1_full(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    user_stats = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert user_stats['num_channels_joined'] == 1
    assert user_stats['num_dms_joined'] == 0
    assert user_stats['num_msgs_sent'] == 0
    assert user_stats['involvement'] == 1

# Test stats with user involved in all types of activity
def test_user_stats_v1_all(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Creating a dm
    u_id_list = [users['user2']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in channel_id1
    requests.post(config.url + 'message/send/v2', json={
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

    user_stats1 = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    user_stats2 = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user2']['token'],
    }).json()

    assert user_stats1['num_channels_joined'] == 1
    assert user_stats1['num_dms_joined'] == 1
    assert user_stats1['num_msgs_sent'] == 2
    assert user_stats1['involvement'] == 1

    assert user_stats2['num_channels_joined'] == 0
    assert user_stats2['num_dms_joined'] == 1
    assert user_stats2['num_msgs_sent'] == 0
    assert user_stats2['involvement'] == 0.25


# Test stats to see if invited/joined channels count
def test_user_stats_v1_invite_join(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Creating a dm
    u_id_list = [users['user2']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends a message in channel_id1
    requests.post(config.url + 'message/send/v2', json={
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

    # User 2 sends a message in dm_id1
    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()

    # User 1 invites user 2 to channel
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()

    # User 2 sends a message in channel_id1
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "hi to channel"
    }).json() 
    
    # User 1 invites user 3 to dm
    requests.post(config.url + 'dm/invite/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'u_id': users['user3']['auth_user_id'],
    }).json()

    # User 1 invites user 3 to channel
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user3']['auth_user_id'],
    }).json()

    # User 3 sends a message in channel_id1
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "hi to channel"
    }).json()

    # User 3 sends a message in dm_id1
    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user3']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hello",
    }).json()
  
    user_stats1 = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    user_stats2 = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user2']['token'],
    }).json()

    assert user_stats1['num_channels_joined'] == 1
    assert user_stats1['num_dms_joined'] == 1
    assert user_stats1['num_msgs_sent'] == 2
    assert user_stats1['involvement'] == 0.5

    assert user_stats2['num_channels_joined'] == 1
    assert user_stats2['num_dms_joined'] == 1
    assert user_stats2['num_msgs_sent'] == 2
    assert user_stats2['involvement'] == 0.5

# Test a really active user
# Test stats with user involved in all types of activity
def test_user_stats_v1_active(setup_user_data):
    users = setup_user_data

    # User 1 creates 5 channels
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'C1',
        'is_public': True,
    }).json()

    requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'C2',
        'is_public': True,
    }).json()

    requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'C3',
        'is_public': True,
    }).json()

    requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'C4',
        'is_public': True,
    }).json()

    requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'C5',
        'is_public': True,
    }).json()

    # User 1 creates five dms to user 2
    u_id_list = [users['user2']]
    requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()
    requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()
    requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()
    requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()
    requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    # User 1 sends seven messages in channel_id1
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 1"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 2"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 3"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 4"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 5"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 6"
    }).json() 

    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 7"
    }).json() 
  
    user_stats1 = requests.get(config.url + 'user/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert user_stats1['num_channels_joined'] == 5
    assert user_stats1['num_dms_joined'] == 5
    assert user_stats1['num_msgs_sent'] == 7
    assert user_stats1['involvement'] == 1
