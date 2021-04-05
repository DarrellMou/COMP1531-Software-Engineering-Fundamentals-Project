# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.dm import dm_create_v1, dm_invite_v1
from src.data import data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v2
from src.message import message_send_v2, message_senddm_v1
from src.notifications import notifications_get_v1
from src.other import clear_v1

# Test for added to channel notifications through invite
def test_channelinvite_notif():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')

    chid1 = channels_create_v2(user1['token'], 'Channel1', True)
    channel_invite_v2(user1['token'], chid1['channel_id'], user2['auth_user_id'])
    channel_invite_v2(user2['token'], chid1['channel_id'], user3['auth_user_id'])

    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first_name1last_name added you to Channel1',
            },
        ]
    }
    assert notifications_get_v1(user3['token']) == {
        'notifications': [
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first_name2last_name added you to Channel1',
            },
        ]
    }

# Test for tagged in channel notifications
def test_channeltag_notif():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')

    chid1 = channels_create_v2(user1['token'], 'Channel1', True)
    channel_invite_v2(user1['token'], chid1['channel_id'], user2['auth_user_id'])
    message_send_v2(user1['token'], chid1['channel_id'], 'wbu @first2last2')
    message_send_v2(user1['token'], chid1['channel_id'], '@first2last2 1v1me')
    message_send_v2(user1['token'], chid1['channel_id'], '@first2last2 1v1me but longer')

    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 added you to Channel1',
            },
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in Channel1: wbu @first2last2',
            },
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in Channel1: @first2last2 1v1me',
            },
            {
                'channel_id' : chid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in Channel1: @first2last2 1v1me b',
            },
        ]
    }

# Test for added to dm notifications via dm creation
def test_dmcreate_notif():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first3', 'last3')

    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id'], user3['auth_user_id']])
    
    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 added you to first1last1, first2last2, first3last3',
            },
        ]
    }
    assert notifications_get_v1(user3['token']) == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 added you to first1last1, first2last2, first3last3',
            },
        ]
    }

# Test for added to dm notifications via dm invite
def test_dminvite_notif():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first3', 'last3')

    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_invite_v1(user2['token'], dmid1['dm_id'], user3['auth_user_id'])
    
    assert notifications_get_v1(user3['token']) == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first2last2 added you to first1last1, first2last2',
            },
        ]
    }

# Test for tagged in dm notifications
def test_dmtag_notif():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')

    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    message_senddm_v1(user1['token'], dmid1['dm_id'], '@first2last2 1v1me')
    message_senddm_v1(user1['token'], dmid1['dm_id'], '@first2last2 1v1me but longer')

    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 added you to first1last1, first2last2',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me',
            },
            # Test to see if message cuts off at 20 characters
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me b',
            },
        ]
    }

# Test for maxing out notifications in dms and popping the queue
def test_notif_dms_max():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')

    channelid1 = channels_create_v2(user1['token'], "lesgobro", True)

    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    for x in range(22):
        message_senddm_v1(user1['token'], dmid1['dm_id'], '@first2last2 1v1me' + str(x))

    channel_invite_v2(user1['token'], channelid1['channel_id'], user2['auth_user_id'])

    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me3',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me4',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me5',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me6',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me7',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me8',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me9',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me10',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me11',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me12',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me13',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me14',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me15',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me16',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me17',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me18',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me19',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me20',
            },
            {
                'channel_id' : -1,
                'dm_id' : dmid1['dm_id'],
                'notification_message' : 'first1last1 tagged you in first1last1, first2last2: @first2last2 1v1me21',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 added you to lesgobro',
            },
        ]
    }


# Test for maxing out notifications and popping the queue
def test_notif_channels_max():
    clear_v1()
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first1', 'last1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first2', 'last2')

    channelid1 = channels_create_v2(user1['token'], "lesgobro", True)
    channel_invite_v2(user1['token'], channelid1['channel_id'], user2['auth_user_id'])

    for x in range(22):
        message_send_v2(user1['token'], channelid1['channel_id'], '@first2last2 1v1me' + str(x))

    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me2',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me3',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me4',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me5',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me6',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me7',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me8',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me9',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me10',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me11',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me12',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me13',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me14',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me15',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me16',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me17',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me18',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me19',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me20',
            },
            {
                'channel_id' : channelid1['channel_id'],
                'dm_id' : -1,
                'notification_message' : 'first1last1 tagged you in lesgobro: @first2last2 1v1me21',
            },
        ]
    }