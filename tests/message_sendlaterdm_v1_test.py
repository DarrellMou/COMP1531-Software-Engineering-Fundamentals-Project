# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.message import message_senddm_v1, message_sendlaterdm_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1, dm_leave_v1
from src.other import clear_v1
from datetime import datetime

from src.data import retrieve_data

import time # Used for time.sleep

###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# If a user leaves a dm after using message_sendlater before the message is
# sent, then the message is still sent after they leave the dm


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates dm_1 with member u_id = 1
def set_up_data():
    clear_v1()
    
    # Populate data - create/register users 1 and 2 and have user 1 make dm1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password12345', 'Thomas', 'Tankengine')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    setup = {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'dm1': dm1['dm_id']
    }

    return setup


# Helper function to send x messages from 2 users to a dm
def send_x_messages(user1, user2, dm1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_senddm_v1(user1["token"], dm1, str(message_num))
        else:
            message_senddm_v1(user2["token"], dm1, str(message_num))
        message_count += 1
    
    return {}

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the dm (testing Access Error)
def test_message_sendlaterdm_v1_AccessError():
    setup = set_up_data()
    user3, dm1 = setup['user3'], setup['dm1']

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # user3 who is not a part of dm1 tries to send message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_sendlaterdm_v1(user3["token"], dm1, "Hello", send_time)


# Testing to see if message is of valid length
def test_message_sendlaterdm_v1_InputError():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to dm1
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user1["token"], dm1, long_message, send_time)


# Test input error when dm_id is not a valid dm
def test_message_sendlaterdm_v1_InputError_invalid_dm():
    setup = set_up_data()
    user1 = setup['user1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    # user1 tries to send a message that is too long to dm 1
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user1["token"], 123321, "Hello", send_time)


# Test input error when time _sent is in the past
def test_message_sendlaterdm_v1_InputError_invalid_time():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time - 10

    # user1 tries to send a message that is too long to dm 1
    with pytest.raises(InputError):
        assert message_sendlaterdm_v1(user1["token"], dm1, "Hello", send_time)


# Default access error when token is invalid
def test_message_sendlaterdm_v1_default_Access_Error():

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    with pytest.raises(AccessError):
        message_sendlaterdm_v1("invalid token", "dm1", "Wrong", send_time)

############################ END EXCEPTION TESTING ############################


######################### TESTING MESSAGE SEND LATER ##########################

# Testing 1 message being sent in the future
def test_message_send_later_v1_1_message():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']

    # Assert that there are no messages within the dm
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 0

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    message_sendlaterdm_v1(user1["token"], dm1, "Hello", send_time)

    # 1 second hasn't passed yet, so the number of messages should still be 0
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 0

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)

    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 1
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message'] == "Hello"
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['u_id'] == user1['auth_user_id']


# Testing one message being sent later and then sending multiple afterwards
def test_message_send_later_v1_send_multiple_after():
    setup = set_up_data()
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    dm_invite_v1(user1["token"], dm1, user3["auth_user_id"])
    
    # Assert that there are no messages within the dm
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 0

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    message_sendlaterdm_v1(user1["token"], dm1, "Hello", send_time)

    send_x_messages(user1, user3, dm1, 20)
    # 1 second hasn't passed yet, so the number of messages should just be 20
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 20

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)
    message_senddm_v1(user3['token'], dm1, "Bye!")

    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 22
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][1]['message'] == "Hello"
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][1]['u_id'] == user1['auth_user_id']
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message'] == "Bye!"
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['u_id'] == user3['auth_user_id']


# Testing user3 sending a message later and then leaving the dm before
# the message is sent
def test_message_send_later_v1_leave_dm_before_message_sent():
    setup = set_up_data()
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    dm_invite_v1(user1["token"], dm1, user3["auth_user_id"])

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    message_senddm_v1(user1['token'], dm1, "Hi!")

    message_sendlaterdm_v1(user3["token"], dm1, "I'm leaving.", send_time)
    dm_leave_v1(user3['token'], dm1)

    message_senddm_v1(user1['token'], dm1, "Nice to meet you")
    
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 2
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message'] == "Nice to meet you"
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][1]['message'] == "Hi!"

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)
    assert len(dm_messages_v1(user1['token'], dm1, 0)['messages']) == 3
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['message'] == "I'm leaving."
    assert dm_messages_v1(user1['token'], dm1, 0)['messages'][0]['u_id'] == user3['auth_user_id']
