# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2, message_edit_v2, message_share_v1, message_senddm_v1
from src.dm import dm_messages_v1, dm_create_v1
from src.other import clear_v1


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Sharing a message will add a new message to the data['messages'] list and to
# the channel's or dm's messages list

# The way messages are shared in the http://Dreams-unsw.herokuapp.com/ app is
# the correct way of sharing messages


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if the user who is sharing the message to a channel is
# actually in that channel
def test_message_share_v1_AccessError(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    channel3 = channels_create_v2(user1["token"], "ch3", True)['channel_id']

    with pytest.raises(AccessError):
        assert message_share_v1(user2["token"], m_id, "Optional Message", channel3, -1)

# Testing to see if the user who is sharing the message to a dm is
# actually in that dm
def test_message_share_v1_AccessError_dm(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    m_id = message_senddm_v1(user1["token"], dm1, "Hello")['message_id']

    dm3 = dm_create_v1(user1["token"], [user3["auth_user_id"]])['dm_id']

    with pytest.raises(AccessError):
        assert message_share_v1(user2["token"], m_id, "Optional Message", -1, dm3)


# Default access error when token is invalid
def test_message_share_v1_default_Access_Error():

    with pytest.raises(AccessError):
        message_share_v1("invalid token", 123, "Wrong", 456654, -1)

############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SHARE ############################

# Testing user1 sharing one message to channel
def test_message_share_v1_share_one_to_channel(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    shared_m_id = message_share_v1(user2["token"], m_id, "Shared Message 1", channel2, -1)['shared_message_id']

    channel1_messages = channel_messages_v2(user1["token"], channel1, 0)
    channel2_messages = channel_messages_v2(user1["token"], channel2, 0)

    assert channel1_messages["messages"][0]["message_id"] == m_id
    assert channel1_messages["messages"][0]["message"] == "Hello"
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id
    assert channel2_messages["messages"][0]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert len(channel1_messages["messages"]) == 1
    assert len(channel2_messages["messages"]) == 1


# Sharing and resharing the message a few times to differing channels
def test_message_share_v1_share_one_multiple_times(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2["token"], m_id, "Shared Message 1", channel2, -1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "Shared Message 2", channel1, -1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Shared Message 3", channel2, -1)['shared_message_id']
    
    channel1_messages = channel_messages_v2(user1["token"], channel1, 0)
    channel2_messages = channel_messages_v2(user1["token"], channel2, 0)

    assert channel1_messages["messages"][1]["message_id"] == m_id
    assert channel1_messages["messages"][1]["message"] == "Hello"
    assert channel2_messages["messages"][1]["message_id"] == shared_m_id1
    assert channel2_messages["messages"][1]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel2_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n\t\n\t"""\n\tShared Message 1\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'

    assert len(channel2_messages["messages"]) == 2
    assert len(channel1_messages["messages"]) == 2

# Sharing to the same channel
def test_message_share_v1_share_one_multiple_times_same_channel(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2["token"], m_id, "Shared Message 1", channel1, -1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "Shared Message 2", channel1, -1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Shared Message 3", channel1, -1)['shared_message_id']
    
    channel_messages = channel_messages_v2(user1["token"], channel1, 0)

    assert channel_messages["messages"][3]["message_id"] == m_id
    assert channel_messages["messages"][3]["message"] == "Hello"
    assert channel_messages["messages"][2]["message_id"] == shared_m_id1
    assert channel_messages["messages"][2]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert channel_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n\t\n\t"""\n\tShared Message 1\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'
    assert len(channel_messages["messages"]) == 4


# There is no additional message that is attached to the og message
# This follows the way it is shared at http://Dreams-unsw.herokuapp.com/ when
# no optional message is added to the shared message
def test_message_share_v1_share_with_no_added_msg(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2["token"], m_id, "", channel1, -1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "", channel2, -1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Hi", channel1, -1)['shared_message_id']

    channel1_messages = channel_messages_v2(user1["token"], channel1, 0)
    channel2_messages = channel_messages_v2(user1["token"], channel2, 0)

    assert channel1_messages["messages"][2]["message_id"] == m_id
    assert channel1_messages["messages"][2]["message"] == "Hello"
    assert channel1_messages["messages"][1]["message_id"] == shared_m_id1
    assert channel1_messages["messages"][1]["message"] == '\n\n"""\nHello\n"""'
    assert channel1_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel1_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n\t\n\t"""\n\t\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'
    assert len(channel1_messages["messages"]) == 3
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id2
    assert channel2_messages["messages"][0]["message"] == '\n\n"""\n\n\t\n\t"""\n\tHello\n\t"""\n"""'
    assert len(channel2_messages["messages"]) == 1

# Testing user1 sharing one message from channel to dm

def test_message_share_v1_share_from_channel_to_dm(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1, dm1 = setup['user1'], setup['user2'], setup['channel1'], setup["dm1"]
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']
    shared_m_id1 = message_share_v1(user2["token"], m_id, "Shared Message 1", -1, dm1)['shared_message_id']

    channel_messages = channel_messages_v2(user1["token"], channel1, 0)
    dm_messages = dm_messages_v1(user1["token"], dm1, 0)

    assert channel_messages["messages"][0]["message_id"] == m_id
    assert channel_messages["messages"][0]["message"] == "Hello"
    assert channel_messages["messages"][0]["time_created"] <= dm_messages["messages"][0]["time_created"]
    assert len(channel_messages["messages"]) == 1
    assert dm_messages["messages"][0]["message_id"] == shared_m_id1
    assert dm_messages["messages"][0]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert len(dm_messages["messages"]) == 1


# Sharing and resharing the message a few times to differing dms. Message is
# originally sent to a dm
def test_http_message_share_v1_share_dm_multiple_times(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1, dm2 = setup['user1'], setup['user2'], setup['dm1'], setup['dm2']
    m_id = message_senddm_v1(user1["token"], dm1, "Hello")['message_id']
    shared_m_id1 = message_share_v1(user2["token"], m_id, "Shared Message 1", -1, dm1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "Shared Message 2", -1, dm2)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Shared Message 3", -1, dm1)['shared_message_id']

    dm1_messages = dm_messages_v1(user1["token"], dm1, 0)
    dm2_messages = dm_messages_v1(user1["token"], dm2, 0)

    assert dm1_messages["messages"][2]["message_id"] == m_id
    assert dm1_messages["messages"][2]["message"] == "Hello"
    assert dm1_messages["messages"][1]["message_id"] == shared_m_id1
    assert dm1_messages["messages"][1]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert dm1_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm1_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n\t\n\t"""\n\tShared Message 1\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'
    assert len(dm1_messages["messages"]) == 3

    assert dm2_messages["messages"][0]["message_id"] == shared_m_id2
    assert dm2_messages["messages"][0]["message"] == 'Shared Message 2\n\n"""\nShared Message 1\n\t\n\t"""\n\tHello\n\t"""\n"""'
    assert len(dm2_messages["messages"]) == 1

# There is no additional message that is attached to the og message which was
# sent from dm
def test_http_message_share_v1_share_dm_with_no_added_msg(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    m_id = message_senddm_v1(user1["token"], dm1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2["token"], m_id, "", -1, dm1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "", -1, dm1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Hi", -1, dm1)['shared_message_id']

    dm_messages = dm_messages_v1(user1["token"], dm1, 0)

    assert dm_messages["messages"][3]["message_id"] == m_id
    assert dm_messages["messages"][3]["message"] == "Hello"
    assert dm_messages["messages"][2]["message_id"] == shared_m_id1
    assert dm_messages["messages"][2]["message"] == '\n\n"""\nHello\n"""'
    assert dm_messages["messages"][1]["message_id"] == shared_m_id2
    assert dm_messages["messages"][1]["message"] == '\n\n"""\n\n\t\n\t"""\n\tHello\n\t"""\n"""'
    assert dm_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n\t\n\t"""\n\t\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'
    assert len(dm_messages["messages"]) == 4

# There is no additional message that is attached to the og message which was
# sent from dm - this time shared between multiple dms
def test_http_message_share_v1_share_dm_with_no_added_msg_2_dms(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1, dm2 = setup['user1'], setup['user2'], setup['dm1'], setup['dm2']
    m_id = message_senddm_v1(user1["token"], dm1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2["token"], m_id, "", -1, dm1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2["token"], shared_m_id1, "", -1, dm2)['shared_message_id']
    shared_m_id3 = message_share_v1(user2["token"], shared_m_id2, "Hi", -1, dm1)['shared_message_id']

    dm1_messages = dm_messages_v1(user1["token"], dm1, 0)
    dm2_messages = dm_messages_v1(user1["token"], dm2, 0)

    assert dm1_messages["messages"][2]["message_id"] == m_id
    assert dm1_messages["messages"][2]["message"] == "Hello"
    assert dm1_messages["messages"][1]["message_id"] == shared_m_id1
    assert dm1_messages["messages"][1]["message"] == '\n\n"""\nHello\n"""'
    assert dm1_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm1_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n\t\n\t"""\n\t\n\t\t\n\t\t"""\n\t\tHello\n\t\t"""\n\t"""\n"""'
    assert len(dm1_messages["messages"]) == 3
    assert dm2_messages["messages"][0]["message_id"] == shared_m_id2
    assert dm2_messages["messages"][0]["message"] == '\n\n"""\n\n\t\n\t"""\n\tHello\n\t"""\n"""'
    assert len(dm2_messages["messages"]) == 1
