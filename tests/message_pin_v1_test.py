# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2, message_senddm_v1, message_pin_v1, message_remove_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# A removed message cannot be pinned - they're considered as non-valid messages


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################
# Testing for when the user is not part of the channel
def test_message_pin_v1_AccessError(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = message_send_v2(user1['token'], channel1, "HEY EVERYBODY")
    
    # user2 who is not a part of channel1 tries to pin message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_pin_v1(user2["token"], m_id["message_id"])


# Testing for when the user is not part of the dm
def test_message_pin_v1_AccessError_dm(set_up_data):
    setup = set_up_data
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']

    m_id = message_senddm_v1(user1['token'], dm1, "HEY EVERYBODY")

    # user3 who is not a part of dm1 tries to pin message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_pin_v1(user3["token"], m_id["message_id"])


# Testing for when the user is not an owner of the channel but is within it
def test_message_pin_v1_AccessError_non_owner(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    channel_invite_v2(user1["token"], channel1, user2["auth_user_id"])

    m_id = message_send_v2(user1['token'], channel1, "HEY EVERYBODY")
    
    # user2 who is not a part of channel1 tries to pin message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_pin_v1(user2["token"], m_id["message_id"])


# Testing for when the user is not an owner of the dm but is within it
def test_message_pin_v1_AccessError_dm_non_owner(set_up_data):
    setup = set_up_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    m_id = message_senddm_v1(user1['token'], dm1, "HEY EVERYBODY")

    # user2 who is not an owner of dm1 tries to pin the message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_pin_v1(user2["token"], m_id["message_id"])


# Message id is not a real message id
def test_message_pin_v1_InputError_non_valid_id(set_up_data):
    setup = set_up_data
    user1 = setup['user1']
    
    # user1 (the channel owner) tries to pin a non existent message
    with pytest.raises(InputError):
        assert message_pin_v1(user1["token"], 742)


# Message id is already pinned
def test_message_pin_v1_InputError_already_pinned(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    m_id = message_send_v2(user1['token'], channel1, "HEY EVERYBODY")
    message_pin_v1(user1["token"], m_id["message_id"])

    # user1 (the channel owner) tries to pin an already pinned message
    with pytest.raises(InputError):
        assert message_pin_v1(user1["token"], m_id["message_id"])


# Default access error when token is invalid
def test_message_pin_v1_default_Access_Error(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    m_id = message_send_v2(user1['token'], channel1, "Hello")

    with pytest.raises(AccessError):
        message_pin_v1("invalid token", m_id["message_id"])


# Testing for pinning a message which has been removed
def test_message_pin_v1_InputError_pin_removed_msg(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    m_id = message_send_v2(user1['token'], channel1, "Hello")
    message_remove_v1(user1['token'], m_id['message_id'])

    with pytest.raises(InputError):
        message_pin_v1(user1['token'], m_id["message_id"])


############################ END EXCEPTION TESTING ############################


############################# TESTING MESSAGE PIN #############################

# Testing to see if one message is pinned correctly
def test_message_pin_v1_pin_one(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    # Send a message to a channel and then pin that message and check that everything is correct
    m_id = message_send_v2(user1['token'], channel1, "Hello")
    message_pin_v1(user1["token"], m_id["message_id"])

    assert len(channel_messages_v2(user1['token'], channel1, 0)['messages']) == 1
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['message'] == "Hello"
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['is_pinned'] == True
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['message_id'] == m_id['message_id']


# Testing to see if multiple messages are pinned correctly
def test_message_pin_v1_pin_multiple(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    channel_invite_v2(user1["token"], channel1, user2["auth_user_id"])

    # Send 1 message and then pin it
    m_id1 = message_send_v2(user1['token'], channel1, "Hello")
    message_pin_v1(user1["token"], m_id1["message_id"])

    # Send 20 messages after the pinned message
    send_x_messages(user1, user2, channel1, 20)

    # Now send 2 more messages and pin the first of the two that was sent. Check that
    # everything is working as intended
    m_id2 = message_send_v2(user2['token'], channel1, "Bao")
    m_id3 = message_send_v2(user1['token'], channel1, "Bye")
    message_pin_v1(user1["token"], m_id2["message_id"])

    assert len(channel_messages_v2(user1['token'], channel1, 0)['messages']) == 23
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][22]['message'] == "Hello"
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][22]['is_pinned'] == True
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][22]['message_id'] == m_id1['message_id']
    
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][1]['message'] == "Bao"
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][1]['is_pinned'] == True
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][1]['message_id'] == m_id2['message_id']
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][1]['u_id'] == user2["auth_user_id"]

    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][2]['message'] == "20"
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][2]['is_pinned'] == False

    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['message'] == "Bye"
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['is_pinned'] == False
    assert channel_messages_v2(user1['token'], channel1, 0)['messages'][0]['message_id'] == m_id3['message_id']


# Testing to see if one message is pinned correctly to a dm
def test_message_pin_v1_pin_one_dm(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']

    # Send a message to a dm and then pin that message and check that everything is correct
    m_id = message_senddm_v1(user1['token'], dm1, "Hello")
    message_pin_v1(user1["token"], m_id["message_id"])

    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 1
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message'] == "Hello"
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['is_pinned'] == True
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message_id'] == m_id['message_id']


# Testing to see if multiple messages are pinned correctly to a dm
def test_message_pin_v1_pin_multiple_dm(set_up_data):
    setup = set_up_data
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    dm_invite_v1(user1["token"], dm1, user3["auth_user_id"])

    # Send 1 message and then pin it
    m_id1 = message_senddm_v1(user1['token'], dm1, "Hello")
    message_pin_v1(user1["token"], m_id1["message_id"])

    # Send 20 messages after the pinned message
    send_x_messages_dm(user1, user3, dm1, 20)

    # Now send 2 more messages and pin the first of the two that was sent. Check that
    # everything is working as intended
    m_id2 = message_senddm_v1(user3['token'], dm1, "Bao")
    m_id3 = message_senddm_v1(user1['token'], dm1, "Bye")
    message_pin_v1(user1["token"], m_id2["message_id"])

    dm_messages_ans = dm_messages_v1(user1['token'], dm1, 0)

    assert len(dm_messages_ans['messages']) == 23
    assert dm_messages_ans['messages'][22]['message'] == "Hello"
    assert dm_messages_ans['messages'][22]['is_pinned'] == True
    assert dm_messages_ans['messages'][22]['message_id'] == m_id1['message_id']
    
    assert dm_messages_ans['messages'][1]['message'] == "Bao"
    assert dm_messages_ans['messages'][1]['is_pinned'] == True
    assert dm_messages_ans['messages'][1]['message_id'] == m_id2['message_id']
    assert dm_messages_ans['messages'][1]['u_id'] == user3["auth_user_id"]

    assert dm_messages_ans['messages'][2]['message'] == "20"
    assert dm_messages_ans['messages'][2]['is_pinned'] == False

    assert dm_messages_ans['messages'][0]['message'] == "Bye"
    assert dm_messages_ans['messages'][0]['is_pinned'] == False
    assert dm_messages_ans['messages'][0]['message_id'] == m_id3['message_id']


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

def send_x_messages(user1, user2, channel1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_send_v2(user1["token"], channel1, str(message_num))
        else:
            message_send_v2(user2["token"], channel1, str(message_num))
        message_count += 1
    
    return {}

def send_x_messages_dm(user1, user2, dm1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_senddm_v1(user1["token"], dm1, str(message_num))
        else:
            message_senddm_v1(user2["token"], dm1, str(message_num))
        message_count += 1
    
    return {}
