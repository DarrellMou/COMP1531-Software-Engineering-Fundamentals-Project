# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config
from datetime import datetime

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

# Time stamp 


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################


# Default access error when token is invalid
def test_user_stats_v1_default_Access_Error():

    requests.get(config.url + 'users/stats/v1', params={
        'token': "imposter",
    }).status_code = 403


############################ END EXCEPTION TESTING ############################


############################# TESTING USER STATS #############################

# Test stats when only users exist, but no boards of discussion
def test_users_stats_v1_empty(setup_user_data):
    users = setup_user_data
    print(users['user1'])
    time_stamp = round(datetime.now().timestamp())
    dreams_stats = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert dreams_stats['channels_exist'] == [{'num_channels_exist': 0,'time_stamp': time_stamp}]
    assert dreams_stats['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time_stamp}]
    assert dreams_stats['messages_exist'] == [{'num_messages_exist': 0, 'time_stamp': time_stamp}]
    assert dreams_stats['utilization_rate'] == 0


# Test stats with users and boards but no messages
def test_users_stats_v1_no_msg(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Creating a dm
    u_id_list = [users['user2']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    time_stamp = round(datetime.now().timestamp())
    dreams_stats = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert dreams_stats['channels_exist'] == [{'num_channels_exist': 1,'time_stamp': time_stamp}]
    assert dreams_stats['dms_exist'] == [{'num_dms_exist': 1, 'time_stamp': time_stamp}]
    assert dreams_stats['messages_exist'] == [{'num_messages_exist': 0, 'time_stamp': time_stamp}]
    assert dreams_stats['utilization_rate'] == 0.4


# Test stats when there is only one active user contributing to full utilization and sending messages
def test_users_stats_v1_loner(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # User 1 sends four messages in channel_id1
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

    time_stamp = round(datetime.now().timestamp())
    dreams_stats = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert dreams_stats['channels_exist'] == [{'num_channels_exist': 1,'time_stamp': time_stamp}]
    assert dreams_stats['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time_stamp}]
    assert dreams_stats['messages_exist'] == [{'num_messages_exist': 4, 'time_stamp': time_stamp}]
    assert dreams_stats['utilization_rate'] == 0.2


# Test stats to see if invited/joined users count towards utilization
def test_users_stats_v1_invite_join(setup_user_data):
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

    # User 1 invites user 2 to channel_id1
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

    # User 3 joins channel 1
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
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
  
    time_stamp = round(datetime.now().timestamp())
    dreams_stats = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert dreams_stats['channels_exist'] == [{'num_channels_exist': 1,'time_stamp': time_stamp}]
    assert dreams_stats['dms_exist'] == [{'num_dms_exist': 1, 'time_stamp': time_stamp}]
    assert dreams_stats['messages_exist'] == [{'num_messages_exist': 6, 'time_stamp': time_stamp}]
    assert dreams_stats['utilization_rate'] == 0.6


# Test to see partial utilization rates
def test_users_stats_v1_partial_util(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # User 1 sends four messages in channel_id1
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': "Welcome 1"
    }).json() 

    time_stamp = round(datetime.now().timestamp())
    dreams_stats = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token'],
    }).json()

    assert dreams_stats['channels_exist'] == [{'num_channels_exist': 1,'time_stamp': time_stamp}]
    assert dreams_stats['dms_exist'] == [{'num_dms_exist': 0, 'time_stamp': time_stamp}]
    assert dreams_stats['messages_exist'] == [{'num_messages_exist': 1, 'time_stamp': time_stamp}]
    assert dreams_stats['utilization_rate'] == 0.2


# Test stats to see if multiple users get the same stats
def test_users_stats_v1_active(setup_user_data):
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

    # Observe dreams stats
    time_stamp = round(datetime.now().timestamp())
    dreams_stats1 = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user1']['token']
    }).json()

    assert dreams_stats1['channels_exist'] == [{'num_channels_exist': 5,'time_stamp': time_stamp}]
    assert dreams_stats1['dms_exist'] == [{'num_dms_exist': 5, 'time_stamp': time_stamp}]
    assert dreams_stats1['messages_exist'] == [{'num_messages_exist': 7, 'time_stamp': time_stamp}]
    assert dreams_stats1['utilization_rate'] == 0.4

    time_stamp = round(datetime.now().timestamp())
    dreams_stats2 = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user2']['token'],
    }).json()

    assert dreams_stats2['channels_exist'] == [{'num_channels_exist': 5,'time_stamp': time_stamp}]
    assert dreams_stats2['dms_exist'] == [{'num_dms_exist': 5, 'time_stamp': time_stamp}]
    assert dreams_stats2['messages_exist'] == [{'num_messages_exist': 7, 'time_stamp': time_stamp}]
    assert dreams_stats2['utilization_rate'] == 0.4
    
    time_stamp = round(datetime.now().timestamp())
    dreams_stats3 = requests.get(config.url + 'users/stats/v1', params={
        'token': users['user3']['token'],
    }).json()

    assert dreams_stats3['channels_exist'] == [{'num_channels_exist': 5,'time_stamp': time_stamp}]
    assert dreams_stats3['dms_exist'] == [{'num_dms_exist': 5, 'time_stamp': time_stamp}]
    assert dreams_stats3['messages_exist'] == [{'num_messages_exist': 7, 'time_stamp': time_stamp}]
    assert dreams_stats3['utilization_rate'] == 0.4
