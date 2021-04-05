# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from http_tests import * # import fixtures for pytest

import json
import requests
import pytest
from src import config

# Test invite to channel notifications
def test_notifications_channel_invite(setup_user_data):
    users = setup_user_data

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': users['user1']['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Invite user2
    requests.post(config.url + 'channel/invite/v2', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': users['user2']['auth_user_id'],
    }).json()

    # Get notifications for user2
    notifications = requests.get(config.url + 'notifications/get/v1', params={
        'token': users['user2']['token'],
    }).json()

    assert notifications == {
        'notifications': [
            {
                'channel_id' : channel_id['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'user1_firstuser1_las added you to Public',
            },
        ]
    }

# Test dm_create notifications
def test_notifications_dm_create(setup_user_data):
    users = setup_user_data

    # Creating a dm
    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': users['user1']['token'],
        'u_ids': [users['user2']['auth_user_id']],
    }).json()

    # Get notifications for user2
    notifications = requests.get(config.url + 'notifications/get/v1', params={
        'token': users['user2']['token'],
    }).json()

    assert notifications == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dm_id['dm_id'],
                'notification_message' : 'user1_firstuser1_las added you to user1_firstuser1_las, user2_firstuser2_las',
            },
        ]
    }

# Test dm_invite notifications
def test_notifications_dm_invite(setup_user_data):
    users = setup_user_data

    # Creating a dm
    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': users['user1']['token'],
        'u_ids': [users['user2']['auth_user_id']],
    }).json()

    # Invite user 3 to dm's
    requests.post(config.url + 'dm/invite/v1', json={
        'token': users['user1']['token'],
        'dm_id': dm_id['dm_id'],
        'u_id': users['user3']['auth_user_id'],
    }).json()

    # Get notifications for user3
    notifications = requests.get(config.url + 'notifications/get/v1', params={
        'token': users['user3']['token'],
    }).json()

    assert notifications == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dm_id['dm_id'],
                'notification_message' : 'user1_firstuser1_las added you to user1_firstuser1_las, user2_firstuser2_las',
            },
        ]
    }

def test_notifications_channel_tag(setup_user_data):

    # Create user 1
    user1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@gmail.com',
        'password': 'password123',
        'name_first': 'first1',
        'name_last': 'last1',
    }).json()

    # Create user 2
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@gmail.com',
        'password': 'password123',
        'name_first': 'first2',
        'name_last': 'last2',
    }).json()

    # Creating a public channel
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': user1['token'],
        'name': 'Public',
        'is_public': True,
    }).json()

    # Invite user2
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user1['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': user2['auth_user_id'],
    }).json()

    # Tag user2
    requests.post(config.url + 'message/send/v2', json={
        'token': user1['token'],
        'channel_id': channel_id['channel_id'],
        'message': '@first2last2 1v1me',
    }).json()

    # Get notifications for user2
    notifications = requests.get(config.url + 'notifications/get/v1', params={
        'token': user2['token'],
    }).json()

    assert notifications == {
        'notifications': [
            {
                'channel_id' : channel_id['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 added you to Public',
            },
            {
                'channel_id' : channel_id['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in Public: @first2last2 1v1me',
            },
        ]
    }

def test_notifications_dm_tag(setup_user_data):

    # Create user 1
    user1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@gmail.com',
        'password': 'password123',
        'name_first': 'first1',
        'name_last': 'last1',
    }).json()

    # Create user 2
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@gmail.com',
        'password': 'password123',
        'name_first': 'first2',
        'name_last': 'last2',
    }).json()

    # Creating a dm
    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    }).json()

    # Tag user2
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'],
        'dm_id': dm_id['dm_id'],
        'message': '@first2last2 1v1me',
    }).json()

    # Get notifications for user2
    notifications = requests.get(config.url + 'notifications/get/v1', params={
        'token': user2['token'],
    }).json()

    assert notifications == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dm_id['dm_id'],
                'notification_message' : 'first1last1 added you to first1last1, first2last2',
            },
            {
                'channel_id' : -1,
                'dm_id' : dm_id['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me',
            },
        ]
    }