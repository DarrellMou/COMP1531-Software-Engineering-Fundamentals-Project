# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2
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
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)

    setup = {
        'user1': user1,
        'user2': user2,
        'channel1': channel1['channel_id']
    }

    return setup


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

def send_x_messages_two_channels(user, channel1, channel2, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_send_v2(user["token"], channel1, str(message_num))
        message_send_v2(user["token"], channel2, str(message_num))
        message_count += 1
    return {}


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the channel (testing Access Error)
def test_message_send_v2_AccessError():
    setup = set_up_data()
    user2, channel1 = setup['user2'], setup['channel1']
    
    # user2 who is not a part of channel_1 tries to send message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_send_v2(user2["token"], channel1, "Hello")


# Testing to see if message is of valid length
def test_message_send_v2_InputError():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    with pytest.raises(InputError):
        assert message_send_v2(user1["token"], channel1, long_message)


# Default access error when token is invalid
def test_message_send_v2_default_Access_Error():

    with pytest.raises(AccessError):
        message_send_v2("invalid token", "channel1", "Wrong")

############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SEND #############################

# Testing for 1 message being sent by user1
def test_message_send_v2_send_one():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    message_send_ans = message_send_v2(user1["token"], channel1, "Hello")

    channel_msgs = channel_messages_v2(user1["token"], channel1, 0)

    assert message_send_ans["message_id"] == channel_msgs["messages"][0]["message_id"]
    assert channel_msgs["messages"][0]["message"] == "Hello"


# Testing for 2 identical messages being sent by user1
def test_message_send_v2_user_sends_identical_messages():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']


    first_message_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']
    second_message_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    channel_msgs = channel_messages_v2(user1["token"], channel1, 0)

    assert first_message_id == channel_msgs["messages"][1]["message_id"]
    assert second_message_id == channel_msgs["messages"][0]["message_id"]

    assert first_message_id != second_message_id


# Testing for multiple messages with 2 users and that the correct messages are
# being sent
def test_message_send_v2_multiple_users_multiple_messages():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    channel_invite_v2(user1["token"], channel1, user2["auth_user_id"])

    send_x_messages(user1, user2, channel1, 10)

    channel_msgs = channel_messages_v2(user1["token"], channel1, 0)

    assert channel_msgs["messages"][0]["message"] == "10"
    assert channel_msgs["messages"][5]["message"] == "5"
    assert channel_msgs["messages"][9]["message"] == "1"


# Testing for multiple messages with 2 users and that the correct message_ids
# are being returned by message_send
def test_message_send_v2_multiple_users_multiple_messages_message_id():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    channel_invite_v2(user1["token"], channel1, user2["auth_user_id"])

    message_count = 0
    while message_count < 50:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_id = message_send_v2(user1["token"], channel1, str(message_num))['message_id']
        else:
            message_id = message_send_v2(user2["token"], channel1, str(message_num))['message_id']
        channel_msgs = channel_messages_v2(user1["token"], channel1, 0)
        reversed_channel_msgs = channel_msgs["messages"][::-1]
        assert message_id == reversed_channel_msgs[message_count]["message_id"]
        message_count += 1


# Same user sends the identical message to two different channels
# Message ids should be different
def test_message_send_v2_identical_message_to_2_channels():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = channels_create_v2(user1["token"], 'Channel2', True)['channel_id']


    send_x_messages_two_channels(user1, channel1, channel2, 10)

    channel1_msgs = channel_messages_v2(user1["token"], channel1, 0)
    channel2_msgs = channel_messages_v2(user1["token"], channel2, 0)

    m_id0_ch1 = channel1_msgs["messages"][9]["message_id"]
    m_id0_ch2 = channel2_msgs["messages"][9]["message_id"]
    m_id5_ch1 = channel1_msgs["messages"][5]["message_id"]
    m_id5_ch2 = channel2_msgs["messages"][5]["message_id"]
    m_id9_ch1 = channel1_msgs["messages"][0]["message_id"]
    m_id9_ch2 = channel2_msgs["messages"][0]["message_id"]

    assert m_id0_ch1 != m_id0_ch2
    assert m_id5_ch1 != m_id5_ch2
    assert m_id9_ch1 != m_id9_ch2

# Test if message_send also appends message to the data['messages'] list
def test_message_send_v2_appends_to_data_messages():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = channels_create_v2(user1["token"], 'Channel2', True)['channel_id']
    
    send_x_messages_two_channels(user1, channel1, channel2, 10)
    
    channel1_msgs = channel_messages_v2(user1["token"], channel1, 0)
    channel2_msgs = channel_messages_v2(user1["token"], channel2, 0)

    assert len(channel1_msgs['messages']) + len(channel2_msgs['messages']) == 20

'''
# Test if data['messages'] list is in order
def test_message_send_v2_data_messages_in_order():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = channels_create_v2(user1["token"], 'Channel2', True)['channel_id']

    send_x_messages_two_channels(user1, channel1, channel2, 10)
    
    channel1_msgs = channel_messages_v2(user1["token"], channel1, 0)
    channel2_msgs = channel_messages_v2(user1["token"], channel2, 0)

    m_id0_ch1 = channel1_messages['messages'][0]
    m_id0_ch2 = channel2_messages['messages'][0]
    m_id5_ch1 = channel1_messages['messages'][5]
    m_id5_ch2 = channel2_messages['messages'][5]
    m_id9_ch1 = channel1_messages['messages'][9]
    m_id9_ch2 = channel2_messages['messages'][9]

    assert data['messages'][0]['message_id'] == m_id0_ch1['message_id']
    assert data['messages'][0]['message'] == m_id0_ch1['message']
'''