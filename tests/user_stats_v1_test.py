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
from src.user import user_stats_v1
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

    setup = {
        'user1': user1,
        'user2': user2,
        'user3': user3,
    }

    return setup

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################


# Default access error when token is invalid
def test_user_stats_v1_default_Access_Error():
    setup = set_up_data()
    user1 = setup['user1']

    with pytest.raises(AccessError):
        user_stats_v1("imposter")

############################ END EXCEPTION TESTING ############################


############################# TESTING USER STATS #############################

# Test stats when only users exist, but no boards of discussion
def test_user_stats_v1_empty():
    setup = set_up_data()
    user1 = setup['user1']

    assert user_stats_v1(user1['token']) == {
        'num_channels_joined': 0,
        'num_dms_joined': 0,
        'num_msgs_sent': 0,
        'involvement': 0,
    }

# Test stats when one user has all of the involvement
def test_user_stats_v1_full():
    setup = set_up_data()
    user1 = setup['user1']
    channels_create_v2(user1['token'], 'Channel1', True)

    assert user_stats_v1(user1['token']) == {
        'num_channels_joined': 1,
        'num_dms_joined': 0,
        'num_msgs_sent': 0,
        'involvement': 1,
    }

# Test stats with user involved in all types of activity
def test_user_stats_v1_all():
    setup = set_up_data()
    user1, user2 = setup['user1'], setup['user2']
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    message_send_v2(user1["token"], channel1["channel_id"], "Hello world!_ch")
    message_senddm_v1(user1['token'], dmid1['dm_id'], "Hello world!_dm")

    assert user_stats_v1(user1['token']) == {
        'num_channels_joined': 1,
        'num_dms_joined': 1,
        'num_msgs_sent': 2,
        'involvement': 1,
    }
    assert user_stats_v1(user2['token']) == {
        'num_channels_joined': 0,
        'num_dms_joined': 1,
        'num_msgs_sent': 0,
        'involvement': 0.25,
    }

# Test stats to see if invited/joined channels count
def test_user_stats_v1_invite_join():
    setup = set_up_data()
    user1, user2, user3 = setup['user1'], setup['user2'], setup['user3']
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

    assert user_stats_v1(user1['token']) == {
        'num_channels_joined': 1,
        'num_dms_joined': 1,
        'num_msgs_sent': 2,
        'involvement': 0.5,
    }
    assert user_stats_v1(user2['token']) == {
        'num_channels_joined': 1,
        'num_dms_joined': 1,
        'num_msgs_sent': 2,
        'involvement': 0.5,
    }
    assert user_stats_v1(user2['token']) == {
        'num_channels_joined': 1,
        'num_dms_joined': 1,
        'num_msgs_sent': 2,
        'involvement': 0.5,
    }

# Test a really active user
# Test stats with user involved in all types of activity
def test_user_stats_v1_active():
    setup = set_up_data()
    user1, user2 = setup['user1'], setup['user2']
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    channels_create_v2(user1['token'], 'Channel2', True)
    channels_create_v2(user1['token'], 'Channel3', True)
    channels_create_v2(user1['token'], 'Channel4', True)
    channels_create_v2(user1['token'], 'Channel5', True)
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
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

    assert user_stats_v1(user1['token']) == {
        'num_channels_joined': 5,
        'num_dms_joined': 5,
        'num_msgs_sent': 7,
        'involvement': 1,
    }
