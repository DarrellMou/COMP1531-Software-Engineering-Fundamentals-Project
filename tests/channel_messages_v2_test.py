# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.other import clear_v1


# ASSUMPTION: Start refers to the starting index of the
# data['channels'][channel_id]['messages'] list

# ASSUMPTION: An out of index message within the messages list of a channel
# (i.e data['channels'][channel_id]['messages']) will never be accessed and
# therefore, there is no need to raise an index error.
# E.g. trying to access data['channels'][channel_id]['messages'][1] when there
# is only 1 message in that specific channel_id, which has an index of 0.


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Add members 1 and 2 into channel 1 and add x messages with the message just being the message id
def add_x_messages(user1, user2, channel1, num_messages):

    # Add user 2 into the channel so user 1 and 2 can have a conversation
    channel_invite_v2(user1["token"], channel1, user2["auth_user_id"])

    # Physically creating num_messages amount of messages
    # The most recent message is at the beginning of the list as per spec
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_num % 2 == 1:
            message_send_v2(user1["token"], channel1, str(message_num))
        else:
            message_send_v2(user2["token"], channel1, str(message_num))
        message_count += 1

    return {}


###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user token is invalid (testing Access Error)
def test_channel_messages_v2_token_AccessError(set_up_data):
    setup = set_up_data
    channel1 = setup["channel1"]

    with pytest.raises(AccessError):
        assert channel_messages_v2("Invalid token", channel1, 0)

# Testing for when the user is not part of the channel (testing Access Error)
def test_channel_messages_v2_AccessError(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Add 1 message to channel1
    message_send_v2(user1["token"], channel1, "Test Message")

    # user2 is not part of channel_1 - should raise an access error
    with pytest.raises(AccessError):
        assert channel_messages_v2(user2["token"], channel1, 0)


# Testing for when an invalid channel_id is used (testing input error)
def test_channel_messages_v2_InputError_invalid_channel(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']
    
    # Add 1 message to channel1
    message_send_v2(user1["token"], channel1, "Test Message")

    # 2 is an invalid channel_id in this case
    with pytest.raises(InputError):
        assert channel_messages_v2(user1["token"], 2, 0)


# Testing for when an invalid start is used (start > num messages in channel)
def test_channel_messages_v2_InputError_invalid_start(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    # Add 1 message to channel1
    message_send_v2(user1["token"], channel1, "Test Message")

    with pytest.raises(InputError):
        assert channel_messages_v2(user1["token"], channel1, 2)


############################ END EXCEPTION TESTING ############################


########################### TESTING CHANNEL MESSAGES ###########################


# Testing for when there are no messages - should return {'messages': [], 'start': 0, 'end': -1}
# ASSUMPTION: No messages mean that the most recent message has been returned - therefore end = -1
def test_channel_messages_v2_no_messages(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    assert channel_messages_v2(user1["token"], channel1, 0) ==\
    {'messages': [], 'start': 0, 'end': -1}, "No messages - should return end: -1"


# Testing to see if the function is working for a single message
def test_channel_messages_v2_1_message(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    message_send_v2(user1["token"], channel1, "Test message")

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['start'] == 0,\
    "Start should not change"
    
    assert messages_list['end'] == -1,\
    "The most recent message has been reached - return 'end': -1"
    
    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "Test message"



# Testing for exactly 50 messages
# ASSUMPTION: 50th message IS the last message so return 'end': -1 rather than 'end': 50
# when there are 50 messages in the channel with start being 0
def test_channel_messages_v2_50_messages(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Add 50 messages
    add_x_messages(user1, user2, channel1, 50)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['start'] == 0,\
    "Start should not change"
    
    assert messages_list['end'] == -1,\
    "50th message IS the least recent message so it should return 'end': -1"
    
    assert len(messages_list['messages']) == 50



# Create 100 messages, with a given start of 50 (50th index means the 51st most
# recent message). Should return 50 messages (index 50 up to index 99 which
# corresponds with the 51st most recent message up to the least recent message,
# i.e. the 100th message) and an end of -1 as per the reasons in the test above
def test_channel_messages_v2_100_messages_start_50(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Add 100 messages
    add_x_messages(user1, user2, channel1, 100)

    messages_list = channel_messages_v2(user1["token"], channel1, 50)

    assert messages_list['start'] == 50, "Start should not change"

    assert messages_list['end'] == -1,\
    "50th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(messages_list['messages']) == 50

    assert messages_list['messages'][0]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "50"

    assert messages_list['messages'][49]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][49]["message"] == "1"


# Given a channel with 10 messages and a start of 9 (10th most recent message
# i.e. the least recent message), return that last message as the only one in
# the messages list and an end of -1
def test_channel_messages_start_is_last_message(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Add 10 messages
    add_x_messages(user1, user2, channel1, 10)

    messages_list = channel_messages_v2(user1["token"], channel1, 9)

    assert messages_list['start'] == 9, "Start should not change"
    
    assert messages_list['end'] == -1,\
    "10th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(messages_list['messages']) == 1

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "1"


# Given a start being equal to the number of messages in the given channel,
# return and empty messages list and an end of -1 as per spec and this
# forum post: https://edstem.org/courses/5306/discussion/384787
def test_start_equals_num_messages(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Add 10 messages
    add_x_messages(user1, user2, channel1, 10)

    messages_list = channel_messages_v2(user1["token"], channel1, 10)

    assert messages_list['start'] == 10, "Start should not change"
    
    assert messages_list['end'] == -1,\
    "No messages so the most recent message has been returned so function should return 'end': -1"
    
    assert len(messages_list['messages']) == 0

    assert messages_list['messages'] == []


# Testing for <50 messages (checking if 'end' returns -1)
def test_channel_messages_v2_48_messages(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Add members 1 and 2 into channel 1 and add 48 messages with the message just being the message id
    add_x_messages(user1, user2, channel1, 48)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['start'] == 0,\
        "Start should not change"

    assert messages_list['end'] == -1,\
        "48 < start + 50 so the funtion should return 'end': -1"

    assert messages_list['messages'][47]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][47]["message"] == "1"

    assert messages_list['messages'][0]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "48"


# Testing for >50 messages (checking if the correct final message is returned)
def test_channel_messages_v2_51_messages_start_0(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    add_x_messages(user1, user2, channel1, 51)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['start'] == 0, "Start should not change"

    assert messages_list['end'] == 50,\
        "51 > start + 50 so the funtion should return 'end': 50"

    assert messages_list['messages'][49]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][49]["message"] == "2"

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "51"


# Testing for >50 messages wit start being 50
def test_channel_messages_v2_51_messages_start_50(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    add_x_messages(user1, user2, channel1, 51)

    messages_list = channel_messages_v2(user1["token"], channel1, 50)

    assert messages_list['start'] == 50, "Start should not change"

    assert messages_list['end'] == -1,\
        "51 < start + 50 so the funtion should return 'end': -1"

    assert len(messages_list['messages']) == 1

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "1"


# Testing for between 100 and 150 messages with start being 0
def test_channel_messages_v2_111_messages_start_0(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1'] 
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    add_x_messages(user1, user2, channel1, 111)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['start'] == 0, "Start should not change"

    assert messages_list['end'] == 50,\
        "111 > start + 50 - function should return 'end': 50"

    assert len(messages_list['messages']) == 50,\
        "function should return 50 messages max"

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "111"

    assert messages_list['messages'][25]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][25]["message"] == "86"

    assert messages_list['messages'][49]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][49]["message"] == "62"


# Testing for between 100 and 150 messages with start being 50
def test_channel_messages_v2_111_messages_start_50(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    add_x_messages(user1, user2, channel1, 111)

    messages_list = channel_messages_v2(user1["token"], channel1, 50)

    assert messages_list['start'] == 50, "Start should not change"

    assert messages_list['end'] == 100,\
        "111 > start + 50 - function should return 'end': 100"

    assert len(messages_list['messages']) == 50,\
        "function should return 50 messages max"

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "61"

    assert messages_list['messages'][25]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][25]["message"] == "36"

    assert messages_list['messages'][49]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][49]["message"] == "12"


# Testing for between 100 and 150 messages with start being 100
def test_channel_messages_v2_111_messages_start_100(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    add_x_messages(user1, user2, channel1, 111)

    messages_list = channel_messages_v2(user1["token"], channel1, 100)

    assert messages_list['start'] == 100, "Start should not change"

    assert messages_list['end'] == -1,\
        "111 < start + 50 - function should return 'end': -1"

    assert len(messages_list['messages']) == 11,\
        "function should return remaining 11 messages"

    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "11"

    assert messages_list['messages'][5]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][5]["message"] == "6"

    assert messages_list['messages'][10]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][10]["message"] == "1"


# Test for when start is not a multiple of 50 and there are more than 50 messages remaining
def test_channel_messages_v2_start_21(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    add_x_messages(user1, user2, channel1, 111)

    messages_list = channel_messages_v2(user1["token"], channel1, 21)

    assert messages_list['start'] == 21, "Start should not change"

    assert messages_list['end'] == 71,\
        "End = start + 50 if the least recent message is not returned"

    # The 22nd most recent message of the whole channel is the first one to be returned
    assert messages_list['messages'][0]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "90"

    assert messages_list['messages'][25]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][25]["message"] == "65"

    assert messages_list['messages'][49]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][49]["message"] == "41"


# Test for when start is not a multiple of 50 and there are less than 50 messages remaining
def test_channel_messages_v2_start_21_end_neg1(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id 
    add_x_messages(user1, user2, channel1, 50)

    messages_list = channel_messages_v2(user1["token"], channel1, 21)

    assert messages_list['start'] == 21, "Start should not change"

    assert messages_list['end'] == -1,\
        "50 < start + 50 if so return 'end': -1"

    # The 22nd most recent message of the whole channel is the first one to be returned
    # (essentially data['messages'][21] - the 21st index)
    assert messages_list['messages'][0]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "29"

    assert messages_list['messages'][25]["u_id"] == user2["auth_user_id"]
    assert messages_list['messages'][25]["message"] == "4"
    
    assert messages_list['messages'][28]["u_id"] == user1["auth_user_id"]
    assert messages_list['messages'][28]["message"] == "1"
