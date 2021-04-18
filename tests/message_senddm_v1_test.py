# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye, edited by Nikki Yao, Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create_v1, dm_invite_v1, dm_messages_v1
from src.message import message_senddm_v1

###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Messages that are sent using message_senddm are appended to the message list
# within the dm


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for an invalid token
def test_channels_create_access_error(set_up_data):
    setup = set_up_data
    dm1 = setup['dm1']

    with pytest.raises(AccessError):
        message_senddm_v1("invalid a_u_id", dm1, True)


# Testing for when the user is not part of the dm (testing Access Error)
def test_message_senddm_v1_AccessError(set_up_data):
    setup = set_up_data
    user3, dm1 = setup['user3'], setup['dm1']
    
    # user3 who is not a part of dm1 tries to send message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_senddm_v1(user3['token'], dm1, "Hello")


# Testing to see if message is of valid length
def test_message_senddm_v1_InputError(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to dm 1
    with pytest.raises(InputError):
        assert message_senddm_v1(user1['token'], dm1, long_message)


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SEND #############################

# Testing for 1 message being sent by user1
def test_message_senddm_v1_send_one(set_up_data):
    setup = set_up_data

    user1, dm1 = setup['user1'], setup['dm1']
    
    msg_send_ans = message_senddm_v1(user1['token'], dm1, "Hello")['message_id']

    dm_msgs = dm_messages_v1(user1["token"], dm1, 0)

    assert msg_send_ans == dm_msgs['messages'][0]['message_id']


# Testing for 2 identical messages being sent by user1
def test_message_senddm_v1_user_sends_identical_messages(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']

    first_message_id = message_senddm_v1(user1['token'], dm1, "Hello")['message_id']
    second_message_id = message_senddm_v1(user1['token'], dm1, "Hello")['message_id']

    dm_msgs = dm_messages_v1(user1["token"], dm1, 0)

    assert first_message_id == dm_msgs["messages"][1]["message_id"]
    assert second_message_id == dm_msgs["messages"][0]["message_id"]

    assert first_message_id != second_message_id


# Testing for multiple messages with 2 users and that the correct messages are
# being sent
def test_message_senddm_v1_multiple_users_multiple_messages(set_up_data):
    setup = set_up_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])

    send_x_messages(user1['token'], user2['token'], dm1, 10)

    dm_msgs = dm_messages_v1(user1["token"], dm1, 0)

    assert dm_msgs["messages"][0]["message"] == "10"
    assert dm_msgs["messages"][5]["message"] == "5"
    assert dm_msgs["messages"][9]["message"] == "1"


# Testing for multiple messages with 2 users and that the correct message_ids
# are being returned by message_send
def test_message_senddm_v1_multiple_users_multiple_messages_message_id(set_up_data):
    setup = set_up_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])

    message_count = 0
    while message_count < 50:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_id = message_senddm_v1(user1['token'], dm1, str(message_num))['message_id']
        else:
            message_id = message_senddm_v1(user2['token'], dm1, str(message_num))['message_id']
        dm_msgs = dm_messages_v1(user1["token"], dm1, 0)
        reversed_dm_msgs = dm_msgs["messages"][::-1]
        assert message_id == reversed_dm_msgs[message_count]["message_id"]
        message_count += 1


# Same user sends the identical message to two different dms
# Message ids should be different
def test_message_senddm_v1_identical_message_to_2_dms(set_up_data):
    setup = set_up_data
    user1, dm1, user3 = setup['user1'], setup['dm1'], setup['user3']

    dm2 = dm_create_v1(user1['token'], [user3['auth_user_id']])['dm_id']

    send_x_messages_two_dms(user1['token'], dm1, dm2, 10)

    dm1_msgs = dm_messages_v1(user1['token'], dm1, 0)
    dm2_msgs = dm_messages_v1(user1['token'], dm2, 0)

    m_id0_ch1 = dm1_msgs["messages"][9]["message_id"]
    m_id0_ch2 = dm2_msgs["messages"][9]["message_id"]
    m_id5_ch1 = dm1_msgs["messages"][5]["message_id"]
    m_id5_ch2 = dm2_msgs["messages"][5]["message_id"]
    m_id9_ch1 = dm1_msgs["messages"][0]["message_id"]
    m_id9_ch2 = dm2_msgs["messages"][0]["message_id"]

    assert m_id0_ch1 != m_id0_ch2
    assert m_id5_ch1 != m_id5_ch2
    assert m_id9_ch1 != m_id9_ch2


# Test if data['messages'] list is in order 
def test_message_senddm_v1_data_messages_in_order(set_up_data):
    setup = set_up_data
    user1, dm1, user3 = setup['user1'], setup['dm1'], setup['user3']

    dm2 = dm_create_v1(user1['token'], [user3['auth_user_id']])['dm_id']

    send_x_messages_two_dms(user1['token'], dm1, dm2, 10)
    
    dm1_messages = dm_messages_v1(user1['token'], dm1, 0)
    dm2_messages = dm_messages_v1(user1['token'], dm2, 0)

    assert dm1_messages['messages'][9]['message'] == "1"
    assert dm2_messages['messages'][9]['message'] == "1"
    
    assert dm1_messages['messages'][5]['message'] == "5"
    assert dm2_messages['messages'][5]['message'] == "5"

    assert dm1_messages['messages'][0]['message'] == "10"
    assert dm2_messages['messages'][0]['message'] == "10"

    assert len(dm1_messages['messages']) + len(dm2_messages['messages']) == 20


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

def send_x_messages(user1, user2, dm1, num_messages):

    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_senddm_v1(user1, dm1, str(message_num))
        else:
            message_senddm_v1(user2, dm1, str(message_num))
        message_count += 1

    return {}

def send_x_messages_two_dms(user, dm1, dm2, num_messages):

    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_senddm_v1(user, dm1, str(message_num))
        message_senddm_v1(user, dm2, str(message_num))
        message_count += 1

    return {}
