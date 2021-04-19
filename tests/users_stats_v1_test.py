# PROJECT-BACKEND: Team Echo
# Written by Kellen

import pytest

from src.error import InputError, AccessError
from src.channel import channel_invite_v2, channel_join_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_invite_v1
from src.message import message_send_v2, message_senddm_v1
from src.data import retrieve_data
from src.user import users_stats_v1
from datetime import datetime
from src.other import clear_v1


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Messages that are sent using send_message are appended to the message list
# within the channel


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates channel_1 with member u_id = 1
def set_up_data():
    clear_v1()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    user2 = auth_register_v1('user2@gmail.com', 'password123', 'first2', 'last2')
    user3 = auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    user4 = auth_register_v1('user4@gmail.com', 'password123', 'first4', 'last4')

    setup = {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'user4': user4,
    }

    return setup

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################


# Default access error when token is invalid
def test_users_stats_v1_default_Access_Error():
    clear_v1()
    auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')

    with pytest.raises(AccessError):
        users_stats_v1("imposter")

############################ END EXCEPTION TESTING ############################


############################# TESTING USER STATS #############################

# Test stats when only users exist, but no boards of discussion
def test_users_stats_v1_empty():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_stamp}],
        'utilization_rate': 0,
    }

# Test stats with users and boards but no messages
def test_users_stats_v1_no_msg():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    user2 = auth_register_v1('user2@gmail.com', 'password123', 'first2', 'last2')

    channels_create_v2(user1['token'], 'Channel1', True)
    dm_create_v1(user1['token'], [user2['auth_user_id']])

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_stamp}],
        'utilization_rate': 1,
    }

# Test stats when there is only one active user contributing to full utilization and sending messages
def test_users_stats_v1_loner():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    message_send_v2(user1["token"], channel1['channel_id'], "Hello world! 1")
    message_send_v2(user1["token"], channel1['channel_id'], "Hello world! 2")
    message_send_v2(user1["token"], channel1['channel_id'], "Hello world! 3")
    message_send_v2(user1["token"], channel1['channel_id'], "Hello world! 4")

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 4, 'time_stamp': time_stamp}],
        'utilization_rate': 1,
    }

# Test stats to see if invited/joined users count towards utilization
def test_users_stats_v1_invite_join():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    user2 = auth_register_v1('user2@gmail.com', 'password123', 'first2', 'last2')
    user3 = auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    message_send_v2(user1["token"], channel1['channel_id'], "Hi i'm user1 ch")
    message_senddm_v1(user1['token'], dmid1['dm_id'], "Hi i'm user1 dm")
    message_senddm_v1(user2['token'], dmid1['dm_id'], "Hi i'm user2 dm")
    
    channel_invite_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])
    message_send_v2(user2["token"], channel1['channel_id'], "Hi i'm user2 ch")
    
    dm_invite_v1(user1['token'], dmid1['dm_id'], user3['auth_user_id'])
    channel_join_v2(user3['token'], channel1['channel_id'])
    message_send_v2(user3["token"], channel1['channel_id'], "Hi i'm user3 ch")
    message_senddm_v1(user3['token'], dmid1['dm_id'], "Hi i'm user3 dm")

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 6, 'time_stamp': time_stamp}],
        'utilization_rate': 1,
    }


# Test to see partial utilization rates
def test_users_stats_v1_partial_util():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    auth_register_v1('user2@gmail.com', 'password123', 'first2', 'last2')
    auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    auth_register_v1('user4@gmail.com', 'password123', 'first4', 'last4')

    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    message_send_v2(user1["token"], channel1['channel_id'], "Hi i'm user1 ch")

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 1, 'time_stamp': time_stamp}],
        'utilization_rate': 0.25,
    }

# Test stats to see if multiple users get the same stats
def test_users_stats_v1_active():
    clear_v1()
    user1 = auth_register_v1('user1@gmail.com', 'password123', 'first1', 'last1')
    user2 = auth_register_v1('user2@gmail.com', 'password123', 'first2', 'last2')
    user3 = auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    user4 = auth_register_v1('user4@gmail.com', 'password123', 'first4', 'last4')

    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    channels_create_v2(user1['token'], 'Channel2', True)
    channels_create_v2(user1['token'], 'Channel3', True)
    channels_create_v2(user1['token'], 'Channel4', True)
    channels_create_v2(user1['token'], 'Channel5', True)
    dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_create_v1(user1['token'], [user2['auth_user_id']])
    message_send_v2(user1["token"], channel1['channel_id'], "Message 1")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 2")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 3")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 4")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 5")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 6")
    message_send_v2(user1["token"], channel1['channel_id'], "Message 7")

    time_stamp = round(datetime.now().timestamp())
    assert users_stats_v1(user1['token']) == {
        'channels_exist': [{'num_channels_exist': 5, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 5, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 7, 'time_stamp': time_stamp}],
        'utilization_rate': 0.5,
    }
    assert users_stats_v1(user2['token']) == {
        'channels_exist': [{'num_channels_exist': 5, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 5, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 7, 'time_stamp': time_stamp}],
        'utilization_rate': 0.5,
    }

    assert users_stats_v1(user3['token']) == {
        'channels_exist': [{'num_channels_exist': 5, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 5, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 7, 'time_stamp': time_stamp}],
        'utilization_rate': 0.5,
    }

    assert users_stats_v1(user4['token']) == {
        'channels_exist': [{'num_channels_exist': 5, 'time_stamp': time_stamp}],
        'dms_exist': [{'num_dms_exist': 5, 'time_stamp': time_stamp}],
        'messages_exist': [{'num_messages_exist': 7, 'time_stamp': time_stamp}],
        'utilization_rate': 0.5,
    }
