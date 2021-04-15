# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

#################### Tests admin_user_remove route #######################
                                                         
#   * uses pytest fixtures from http_tests/conftest.py                                  
                                                                                                                                                
##########################################################################

###                         HELPER FUNCTIONS                           ###

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        'token': user["token"],
        'u_ids': u_ids_list
    }

###                       END HELPER FUNCTIONS                         ###


# Checks invalid token
def test_admin_user_remove_invalid_token(setup_user_data):
    users = setup_user_data
    
    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    requests.post(config.url + 'auth/logout/v1', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': invalid_token,
        'u_id': users['user2']['auth_user_id'],
    }).status_code == 403


# Checks invalid auth_user_id
def test_admin_user_remove_invalid_uid(setup_user_data):
    users = setup_user_data
    
    # Ensure InputError
    assert requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': users['user1']['token'],
        'u_id': 1234,
    }).status_code == 400


# Checks invalid owner access
def test_admin_user_remove_invalid_owner(setup_user_data):
    users = setup_user_data

    # Ensure AccessError
    assert requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 403


# Checks invalid removal as user is the only owner
def test_admin_user_remove_only_owner(setup_user_data):
    users = setup_user_data

    # Ensure InputError
    assert requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).status_code == 400


# Asserts that channel_messages 'Removed user'
def test_admin_user_remove_channel_messages(setup_user_data):
    users = setup_user_data

    # User 1 makes channel 1 
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    # User 3 joins the public channel
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # User 1 makes User 3 an owner
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user3']['auth_user_id']
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': 'Nice day'
    }).json()

    # Set up variables to test function outputs
    # user_profile_id1 = user_profile_v2(users['user1']['token'],users['user1']['auth_user_id'])
    messages_channel_id1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

     # Ensure the correct output
    #assert user_profile_id1['auth_user_id'][0]['first_name'] == "user1_first"
    assert messages_channel_id1['messages'][0]['message'] == "Nice day"

    # Global User 1 makes User 2 Global
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    # Global User 2 makes User 3 Global
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user3']['auth_user_id'],
        'permission_id': 1,
    }).json()

    # Global User 2 removes User 1
    requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).json()

    messages_channel_id1a = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    assert messages_channel_id1a['messages'][0]['message'] == "Removed user"


# Asserts that user_profile, channel_messages, dm_messages are changed to 'Removed user'
def test_admin_user_remove(setup_user_data):
    users = setup_user_data

    # User 1 makes channel 1 
    channel_id1 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).json()

    # User 3 joins the public channel
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
    }).json()

    # User 1 makes User 3 an owner
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'u_id': users['user3']['auth_user_id']
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id1['channel_id'],
        'message': 'Nice day'
    }).json()

    # User 2 makes channel 2 
    channel_id2 = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user2']['token'],
        'name': "Private Channel",
        'is_public': False,
    }).json()

    # User 1 joins the private channel as global owner
    requests.post(config.url + 'channel/join/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()

    # User 1 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id2['channel_id'],
        'message': 'Hello user2'
    }).json()

    # User 2 sends a message
    requests.post(config.url + 'message/send/v2', json={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
        'message': 'Hello user1'
    }).json()

    # User 1 creates a dm to User 2 and User 3. User 1 sends a message
    u_id_list = [users['user2'],users['user3']]
    dm_id1 = requests.post(config.url + 'dm/create/v1', json=dm_create_body(users['user1'],u_id_list)).json()

    requests.post(config.url + 'message/senddm/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id1['dm_id'],
        'message': "Hi guys",
    }).json()

    # Set up variables to test function outputs
    user_profile_id1 = requests.get(config.url + 'user/profile/v2', params={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).json()
    print(user_profile_id1)

    messages_channel_id1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    messages_channel_id2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
        'start': 0
    }).json()

    messages_dm_id1 = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0
    }).json()
    
    # Ensure the correct output
    assert user_profile_id1['user']['name_first'] == "user1_first"
    assert messages_channel_id1['messages'][0]['message'] == "Nice day"
    assert messages_channel_id2['messages'][0]['message'] == "Hello user1"
    assert messages_channel_id2['messages'][1]['message'] == "Hello user2"
    assert messages_dm_id1['messages'][0]['message'] == "Hi guys"
    
    # Global User 1 makes User 2 Global
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user1']['token'],
        'u_id': users['user2']['auth_user_id'],
        'permission_id': 1,
    }).json()

    # Global User 2 makes User 3 Global
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user3']['auth_user_id'],
        'permission_id': 1,
    }).json()

    channel_details = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()
    print(channel_details)
    print("\n\n")

    # Global User 2 removes User 1
    requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).json()

    channel_details = requests.get(config.url + 'channel/details/v2', params={
        'token': users['user1']['token'],
        'channel_id': channel_id2['channel_id'],
    }).json()
    print(channel_details)

    # Set up variables to test function outputs
    user_profile_id1a = requests.get(config.url + 'user/profile/v2', params={
        'token': users['user2']['token'],
        'u_id': users['user1']['auth_user_id'],
    }).json()

    messages_channel_id1a = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user3']['token'],
        'channel_id': channel_id1['channel_id'],
        'start': 0
    }).json()

    messages_channel_id2a = requests.get(config.url + 'channel/messages/v2', params={
        'token': users['user2']['token'],
        'channel_id': channel_id2['channel_id'],
        'start': 0
    }).json()

    messages_dm_id1a = requests.get(config.url + 'dm/messages/v1', params={
        'token': users['user2']['token'],
        'dm_id': dm_id1['dm_id'],
        'start': 0
    }).json()
    
    # Ensure the correct output after calling admin_user_remove
    assert user_profile_id1a['user']['name_first'] == "Removed"
    assert user_profile_id1a['user']['handle_str'] == "Removed user"
    assert messages_channel_id1a['messages'][0]['message'] == "Removed user"
    assert messages_channel_id2a['messages'][0]['message'] == "Hello user1"
    assert messages_channel_id2a['messages'][1]['message'] == "Removed user"
    assert messages_dm_id1a['messages'][0]['message'] == "Removed user"
