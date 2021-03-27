import pytest

from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1
from src.data import reset_data, retrieve_data
from src.auth import auth_register_v2, auth_decode_token
from src.message import message_senddm_v1

###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates dm_1 with member u_id = 1
def set_up_data():
    reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make dm1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    dm1 = dm_create_v1(user1['auth_user_id'], [user1['auth_user_id']])

    setup = {
        'user1': user1['token'],
        'user2': user2['token'],
        'dm1': dm1['dm_id']
    }

    return setup


# User sends x messages
def send_x_messages(user, dm, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_senddm_v1(user, channel, str(message_num))
        message_count += 1
    
    return data



def send_x_messages_two_users(user1, user2, dm, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_senddm_v1(user1, dm, str(message_num))
        else:
            message_senddm_v1(user2, dm, str(message_num))
        message_count += 1
    
    return data


###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the dm (testing Access Error)
def test_dm_messages_v2_AccessError():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Add 1 message to dm1
    send_x_message(user1, dm1, 1)

    # user2 is not part of dm_1 - should raise an access error
    with pytest.raises(AccessError):
        assert dm_messages_v2(user2, dm1, 0)


# Testing for when an invalid dm_id is used (testing input error)
def test_dm_messages_v2_InputError_invalid_dm():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']
    
    # Add 1 message to dm1
    send_x_message(user1, dm1, 1)

    # 2 is an invalid dm_id in this case
    with pytest.raises(InputError):
        assert dm_messages_v2(user1, 2, 0)


# Testing for when an invalid start is used (start > num messages in dm)
def test_dm_messages_v2_InputError_invalid_start():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']

    # Add 1 message to dm1
    send_x_message(user1, dm1, 1)

    with pytest.raises(InputError):
        assert dm_messages_v2(user1, dm1, 2)


############################ END EXCEPTION TESTING ############################


########################### TESTING dm MESSAGES ###########################


# Testing for when there are no messages - should return {'messages': [], 'start': 0, 'end': -1}
# ASSUMPTION: No messages mean that the most recent message has been returned - therefore end = -1
def test_dm_messages_v2_no_messages():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']

    assert dm_messages_v2(user1, dm1, 0) ==\
    {'messages': [], 'start': 0, 'end': -1}, "No messages - should return end: -1"


# Testing to see if the function is working for a single message
def test_dm_messages_v2_1_message():
    setup = set_up_data()
    user1, dm1 = setup['user1'], setup['dm1']

    send_x_message(user1, dm1, 1)

    assert dm_messages_v2(user1, dm1, 0)['start'] == 0,\
    "Start should not change"
    
    assert dm_messages_v2(user1, dm1, 0)['end'] == -1,\
    "The most recent message has been reached - return 'end': -1"
    
    assert dm_messages_v2(user1, dm1, 0)['messages'][0] ==\
    {'message_id': 1, 'u_id': user1, 'message': "Test message", 'time_created': 1}



# Testing for exactly 50 messages
# ASSUMPTION: 50th message IS the last message so return 'end': -1 rather than 'end': 50
# when there are 50 messages in the dm with start being 0
def test_dm_messages_v2_50_messages():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    # Add 50 messages
    send_x_messages_two_users(user1, user2, dm1, 50)

    assert dm_messages_v2(user1, dm1, 0)['start'] == 0,\
    "Start should not change"
    
    assert dm_messages_v2(user1, dm1, 0)['end'] == -1,\
    "50th message IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages_v2(user1, dm1, 0)['messages']) == 50

    message_list = []
    for i in range(50,0,-1):
        if i % 2 == 0:
            message_list.append({'message_id': i, 'u_id': user2, 'message': f'{i}', 'time_created': i})
        else:
            message_list.append({'message_id': i, 'u_id': user1, 'message': f'{i}', 'time_created': i})
    
    assert dm_messages_v2(user1, dm1, 0)['messages'] == message_list, "Error, messages do not match"

# Create 100 messages, with a given start of 50 (50th index means the 51st most
# recent message). Should return 50 messages (index 50 up to index 99 which
# corresponds with the 51st most recent message up to the least recent message,
# i.e. the 100th message) and an end of -1 as per the reasons in the test above
def test_dm_messages_v2_100_messages_start_50():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    # Add 100 messages
    send_x_messages_two_users(user1, user2, dm1, 100)

    assert dm_messages_v2(user1, dm1, 50)['start'] == 50,\
    "Start should not change"
    
    assert dm_messages_v2(user1, dm1, 50)['end'] == -1,\
    "50th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages_v2(user1, dm1, 50)['messages']) == 50

    assert dm_messages_v2(user1, dm1, 50)['messages'][0] ==\
        {'message_id': 50, 'u_id': user2, 'message': '50', 'time_created': 50}

    assert dm_messages_v2(user1, dm1, 50)['messages'][49] ==\
        {'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}


# Given a dm with 10 messages and a start of 9 (10th most recent message
# i.e. the least recent message), return that last message as the only one in
# the messages list and an end of -1
def test_dm_messages_start_is_last_message():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    # Add 10 messages
    send_x_messages_two_users(user1, user2, dm1, 10)

    assert dm_messages_v2(user1, dm1, 9)['start'] == 9,\
    "Start should not change"
    
    assert dm_messages_v2(user1, dm1, 9)['end'] == -1,\
    "50th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages_v2(user1, dm1, 9)['messages']) == 1

    assert dm_messages_v2(user1, dm1, 9)['messages'] ==\
        [{'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}]


# Given a start being equal to the number of messages in the given dm,
# return and empty messages list and an end of -1 as per spec and this
# forum post: https://edstem.org/courses/5306/discussion/384787
def test_start_equals_num_messages():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    # Add 10 messages
    send_x_messages_two_users(user1, user2, dm1, 10)

    assert dm_messages_v2(user1, dm1, 10)['start'] == 10,\
    "Start should not change"
    
    assert dm_messages_v2(user1, dm1, 10)['end'] == -1,\
    "No messages so the most recent message has been returned so function should return 'end': -1"
    
    assert len(dm_messages_v2(user1, dm1, 10)['messages']) == 0

    assert dm_messages_v2(user1, dm1, 10)['messages'] == []


# Testing for <50 messages (checking if 'end' returns -1)
def test_dm_messages_v2_48_messages():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Add members 1 and 2 into dm 1 and add 48 messages with the message just being the message id
    send_x_messages_two_users(user1, user2, dm1, 48)

    assert dm_messages_v2(user1, dm1, 0)['start'] == 0,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 0)['end'] == -1,\
        "48 < start + 50 so the funtion should return 'end': -1"

    assert dm_messages_v2(user1, dm1, 0)['messages'][47] ==\
        {'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}

    assert dm_messages_v2(user1, dm1, 0)['messages'][0] ==\
        {'message_id': 48, 'u_id': user2, 'message': '48', 'time_created': 48}


# Testing for >50 messages (checking if the correct final message is returned)
def test_dm_messages_v2_51_messages_start_0():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    send_x_messages_two_users(user1, user2, dm1, 51)

    assert dm_messages_v2(user1, dm1, 0)['start'] == 0,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 0)['end'] == 50,\
        "51 > start + 50 so the funtion should return 'end': 50"

    assert dm_messages_v2(user1, dm1, 0)['messages'][49] ==\
        {'message_id': 2, 'u_id': user2, 'message': '2', 'time_created': 2}

    assert dm_messages_v2(user1, dm1, 0)['messages'][0] ==\
        {'message_id': 51, 'u_id': user1, 'message': "51", 'time_created': 51}


# Testing for >50 messages wit start being 50
def test_dm_messages_v2_51_messages_start_50():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    send_x_messages_two_users(user1, user2, dm1, 51)

    assert dm_messages_v2(user1, dm1, 50)['start'] == 50,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 50)['end'] == -1,\
        "51 < start + 50 so the funtion should return 'end': -1"

    assert len(dm_messages_v2(user1, dm1, 50)['messages']) == 1

    assert dm_messages_v2(user1, dm1, 50)['messages'] ==\
        [{'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}]


# Testing for between 100 and 150 messages with start being 0
def test_dm_messages_v2_111_messages_start_0():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1'] 
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user1, user2, dm1, 111)

    assert dm_messages_v2(user1, dm1, 0)['start'] == 0,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 0)['end'] == 50,\
        "111 > start + 50 - function should return 'end': 50"

    assert len(dm_messages_v2(user1, dm1, 0)['messages']) == 50,\
        "function should return 50 messages max"

    assert dm_messages_v2(user1, dm1, 0)['messages'][0] ==\
        {'message_id': 111, 'u_id': user1, 'message': "111", 'time_created': 111}

    assert dm_messages_v2(user1, dm1, 0)['messages'][25] ==\
        {'message_id': 86, 'u_id': user2, 'message': '86', 'time_created': 86}

    assert dm_messages_v2(user1, dm1, 0)['messages'][49] ==\
        {'message_id': 62, 'u_id': user2, 'message': '62', 'time_created': 62}


# Testing for between 100 and 150 messages with start being 50
def test_dm_messages_v2_111_messages_start_50():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user1, user2, dm1, 111)

    assert dm_messages_v2(user1, dm1, 50)['start'] == 50,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 50)['end'] == 100,\
        "111 > start + 50 - function should return 'end': 100"

    assert len(dm_messages_v2(user1, dm1, 50)['messages']) == 50,\
        "function should return 50 messages max"

    assert dm_messages_v2(user1, dm1, 50)['messages'][0] ==\
        {'message_id': 61, 'u_id': user1, 'message': "61", 'time_created': 61}

    assert dm_messages_v2(user1, dm1, 50)['messages'][25] ==\
        {'message_id': 36, 'u_id': user2, 'message': "36", 'time_created': 36}

    assert dm_messages_v2(user1, dm1, 50)['messages'][49] ==\
        {'message_id': 12, 'u_id': user2, 'message': '12', 'time_created': 12}


# Testing for between 100 and 150 messages with start being 100
def test_dm_messages_v2_111_messages_start_100():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user1, user2, dm1, 111)

    assert dm_messages_v2(user1, dm1, 100)['start'] == 100,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 100)['end'] == -1,\
        "111 < start + 50 - function should return 'end': -1"

    assert len(dm_messages_v2(user1, dm1, 100)['messages']) == 11,\
        "function should return remaining 11 messages"

    assert dm_messages_v2(user1, dm1, 100)['messages'][0] ==\
        {'message_id': 11, 'u_id': user1, 'message': "11", 'time_created': 11}

    assert dm_messages_v2(user1, dm1, 100)['messages'][5] ==\
        {'message_id': 6, 'u_id': user2, 'message': '6', 'time_created': 6}

    assert dm_messages_v2(user1, dm1, 100)['messages'][10] ==\
        {'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}


# Test for when start is not a multiple of 50 and there are more than 50 messages remaining
def test_dm_messages_v2_start_21():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user1, user2, dm1, 111)

    assert dm_messages_v2(user1, dm1, 21)['start'] == 21,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 21)['end'] == 71,\
        "End = start + 50 if the least recent message is not returned"

    # The 22nd most recent message of the whole dm is the first one to be returned
    assert dm_messages_v2(user1, dm1, 21)['messages'][0] ==\
        {'message_id': 90, 'u_id': user2, 'message': '90', 'time_created': 90}

    assert dm_messages_v2(user1, dm1, 21)['messages'][25] ==\
        {'message_id': 65, 'u_id': user1, 'message': '65', 'time_created': 65}

    assert dm_messages_v2(user1, dm1, 21)['messages'][49] ==\
        {'message_id': 41, 'u_id': user1, 'message': '41', 'time_created': 41}


# Test for when start is not a multiple of 50 and there are less than 50 messages remaining
def test_dm_messages_v2_start_21_end_neg1():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Add members 1 and 2 into dm 1 and add 50 messages with the message just being the message id 
    send_x_messages_two_users(user1, user2, dm1, 50)

    assert dm_messages_v2(user1, dm1, 21)['start'] == 21,\
        "Start should not change"

    assert dm_messages_v2(user1, dm1, 21)['end'] == -1,\
        "50 < start + 50 if so return 'end': -1"

    # The 22nd most recent message of the whole dm is the first one to be returned
    # (essentially data['messages'][21] - the 21st index)
    assert dm_messages_v2(user1, dm1, 21)['messages'][0] ==\
        {'message_id': 29, 'u_id': user1, 'message': '29', 'time_created': 29}

    assert dm_messages_v2(user1, dm1, 21)['messages'][25] ==\
        {'message_id': 4, 'u_id': user2, 'message': '4', 'time_created': 4}
    
    assert dm_messages_v2(user1, dm1, 21)['messages'][28] ==\
        {'message_id': 1, 'u_id': user1, 'message': '1', 'time_created': 1}
