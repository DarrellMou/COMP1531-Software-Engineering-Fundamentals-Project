import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v1, channel_invite_v1
from src.data import data, reset_data, retrieve_data
from src.auth import auth_register_v1
from src.channels import channels_create_v1


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; adds users 1 and 2, creates channel_1 with member u_id = 1
'''
def add_simple_data():
    # Get and clear the (global) data
    global data
    data = {
        "users" : {},
        "channels" : {}
    }
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')

    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    return data
'''

def add_1_message(user1, channel1):
    data = retrieve_data()
    #data = reset_data()
    #data = add_simple_data()

    # Physically creating messages because we don't have message_send available yet
    data['channels'][channel1['channel_id']]['messages'].append({'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "Test message", 'time_created': 1})
    
    return data


# Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id
def add_50_messages(user1, user2, channel1):
    data = retrieve_data()
    #data = reset_data()
    #data = add_simple_data()

    # Add user 2 into the channel so user 1 and 2 can have a conversation
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])

    # Physically creating 50 messages...
    # The most recent message is at the beginning of the list as per spec
    message_count = 0
    while message_count < 50:
        message_num = message_count + 1
        if message_num % 2 == 1:
            message = {'message_id': message_num, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        else:
            message = {'message_id': message_num, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        data['channels'][channel1['channel_id']]['messages'].append(message)
        message_count += 1

    return data


def add_111_messages(user1, user2, channel1):
    data = retrieve_data()
    #data = reset_data()
    #data = add_simple_data()

    # Add user 2 into the channel so user 1 and 2 can have a conversation
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])

    # Physically creating 111 messages...
    # The most recent message is at the beginning of the list as per spec
    message_count = 0
    while message_count < 111:
        message_num = message_count + 1
        if message_num % 2 == 1:
            message = {'message_id': message_num, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        else:
            message = {'message_id': message_num, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        data['channels'][channel1['channel_id']]['messages'].append(message)
        message_count += 1

    return data


def add_21_messages(user1, user2, channel1):
    data = retrieve_data()
    #data = reset_data()
    #data = add_simple_data()

    # Add user 2 into the channel so user 1 and 2 can have a conversation
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])

    # Physically creating 21 messages...
    message_count = 0
    while message_count < 21:
        message_num = message_count + 1
        if message_num % 2 == 1:
            message = {'message_id': message_num, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        else:
            message = {'message_id': message_num, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': str(message_num), 'time_created': message_num}
        data['channels'][channel1['channel_id']]['messages'].append(message)
        message_count += 1

    return data

###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################




###############################################################################
#                                   TESTING                                   #
###############################################################################

'''
global data
data = {
    "users" : {},
    "channels" : {}
}

# Populate data - create/register users 1 and 2 and have user 1 make
# channel1
user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')

channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
'''



############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the channel (testing Access Error)
def test_channel_messages_v1_AccessError():
    # Add member 1 into channel 1 and add 1 message
    #data = reset_data()
    # Get and clear the (global) data
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add 1 message to channel1
    data = add_1_message(user1, channel1)

    # auth_user_id: 2 is not part of channel_1 - should raise an access error
    with pytest.raises(AccessError):
        assert channel_messages_v1(user2['auth_user_id'], channel1['channel_id'], 0)


# Testing for when an invalid channel_id is used (testing input error)
def test_channel_messages_v1_InputError_invalid_channel():
    # Add member 1 into channel 1 and add 1 message
    # Data is already reset in add_1_message()    
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add 1 message to channel1
    data = add_1_message(user1, channel1)

    # 2 is an invalid channel_id in this case
    with pytest.raises(InputError):
        assert channel_messages_v1(user1['auth_user_id'], 2, 0)


# Testing for when an invalid start is used (start > num messages in channel)
def test_channel_messages_v1_InputError_invalid_start():
    # Add member 1 into channel 1 and add 1 message
    # Data is already reset in add_1_message()
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    # Add 1 message to channel1
    data = add_1_message(user1, channel1) # Only has 1 message

    with pytest.raises(InputError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 2)


# TODO: NOT SOMETHING THAT IS IN SPEC - CAN'T USE RAISE MUST RETURN SOMETHING ELSE
# ASSUMPTION: "Message with index 0 is the most recent message in the channel" - does not make sense to have a more recent message than the latest message
def test_channel_messages_v1_InputError_negative_start():
    # Add member 1 into channel 1 and add 1 message

    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    # Add 1 message to channel1
    data = add_1_message(user1, channel1) # Only has 1 message

    with pytest.raises(InputError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], -1)

############################ END EXCEPTION TESTING ############################


########################### TESTING CHANNEL MESSAGES ###########################


# Testing for when there are no messages - should return {'messages': [], 'start': 0, 'end': -1}
# ASSUMPTION: No messages mean that the most recent message has been returned - therefore end = -1
def test_channel_messages_v1_no_messages():
    # Add member 1 into channel 1 and add 1 message

    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    # Add 1 message to channel 1 and then use the clear function to remove all messages
    data = add_1_message(user1, channel1)
    data['channels'][channel1['channel_id']]['messages'].clear()

    # TODO: Create a better assertion error message
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0) == {'messages': [], 'start': 0, 'end': -1}, "No messages - should return end: -1"

    # Raise an index error if trying to access ['messages'][0] as it is empty
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][0]


# Testing to see if the function is working for a single message
def test_channel_messages_v1_1_message():
    # Add member 1 into channel 1 and add 1 message
    
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    data = add_1_message(user1, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['start'] == 0, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['end'] == -1, "The most recent message has been reached - return 'end': -1"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][0] == {'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "Test message", 'time_created': 1}

    # Raise an index error if trying to access beyond index 0 of ['messages']
    # as index 1 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][1]



# Testing for exactly 50 messages
# ASSUMPTION: 50th message IS the last message so return 'end': -1 rather than 'end': 50
# ASSUMPTION: Message id starts from 1
def test_channel_messages_v1_50_messages():
    # Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id

    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    # Add 50 messages
    data = add_50_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['start'] == 0, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['end'] == -1, "50th message IS the least recent message so it should return 'end': -1"
    assert len(channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages']) == 50
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'] == [
    {'message_id': 50, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '50', 'time_created': 50},
    {'message_id': 49, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '49', 'time_created': 49},
    {'message_id': 48, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '48', 'time_created': 48},
    {'message_id': 47, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '47', 'time_created': 47},
    {'message_id': 46, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '46', 'time_created': 46},
    {'message_id': 45, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '45', 'time_created': 45},
    {'message_id': 44, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '44', 'time_created': 44},
    {'message_id': 43, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '43', 'time_created': 43},
    {'message_id': 42, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '42', 'time_created': 42},
    {'message_id': 41, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '41', 'time_created': 41},
    {'message_id': 40, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '40', 'time_created': 40},
    {'message_id': 39, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '39', 'time_created': 39},
    {'message_id': 38, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '38', 'time_created': 38},
    {'message_id': 37, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '37', 'time_created': 37},
    {'message_id': 36, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '36', 'time_created': 36},
    {'message_id': 35, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '35', 'time_created': 35},
    {'message_id': 34, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '34', 'time_created': 34},
    {'message_id': 33, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '33', 'time_created': 33},
    {'message_id': 32, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '32', 'time_created': 32},
    {'message_id': 31, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '31', 'time_created': 31},
    {'message_id': 30, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '30', 'time_created': 30},
    {'message_id': 29, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '29', 'time_created': 29},
    {'message_id': 28, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '28', 'time_created': 28},
    {'message_id': 27, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '27', 'time_created': 27},
    {'message_id': 26, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '26', 'time_created': 26},
    {'message_id': 25, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '25', 'time_created': 25},
    {'message_id': 24, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '24', 'time_created': 24},
    {'message_id': 23, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '23', 'time_created': 23},
    {'message_id': 22, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '22', 'time_created': 22},
    {'message_id': 21, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '21', 'time_created': 21},
    {'message_id': 20, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '20', 'time_created': 20},
    {'message_id': 19, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '19', 'time_created': 19},
    {'message_id': 18, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '18', 'time_created': 18},
    {'message_id': 17, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '17', 'time_created': 17},
    {'message_id': 16, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '16', 'time_created': 16},
    {'message_id': 15, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '15', 'time_created': 15},
    {'message_id': 14, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '14', 'time_created': 14},
    {'message_id': 13, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '13', 'time_created': 13},
    {'message_id': 12, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '12', 'time_created': 12},
    {'message_id': 11, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '11', 'time_created': 11},
    {'message_id': 10, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '10', 'time_created': 10},
    {'message_id': 9, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '9', 'time_created': 9},
    {'message_id': 8, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '8', 'time_created': 8},
    {'message_id': 7, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '7', 'time_created': 7},
    {'message_id': 6, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '6', 'time_created': 6},
    {'message_id': 5, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '5', 'time_created': 5},
    {'message_id': 4, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '4', 'time_created': 4},
    {'message_id': 3, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '3', 'time_created': 3},
    {'message_id': 2, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '2', 'time_created': 2},
    {'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '1', 'time_created': 1}
    ], "Error, messages do not match"

    # Raise an index error if trying to access beyond index 49 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][50]



# Testing for <50 messages (checking if 'end' returns -1)
def test_channel_messages_v1_48_messages():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id
    data = add_50_messages(user1, user2, channel1)

    # Delete the two most recent messages
    del data['channels'][channel1['channel_id']]['messages'][48:50] # This deletes index 48 and 49 (id 49 and 50)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['start'] == 0, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['end'] == -1, "48 < start + 50 so the funtion should return 'end': -1"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][47] == {'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '1', 'time_created': 1}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][0] == {'message_id': 48, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '48', 'time_created': 48}

    # Raise an index error if trying to access beyond index 47 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][48]


# Testing for >50 messages (checking if the correct final message is returned)
def test_channel_messages_v1_51_messages():
    # Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id

    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    data = add_50_messages(user1, user2, channel1)

    message_51 = {'message_id': 51, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "51", 'time_created': 51}
    data['channels'][channel1['channel_id']]['messages'].append(message_51)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['start'] == 0, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['end'] == 50, "51 > start + 50 so the funtion should return 'end': 50"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][49] == {'message_id': 2, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '2', 'time_created': 2}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][0] == {'message_id': 51, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "51", 'time_created': 51}
    
    # Raise an index error if trying to access beyond index 49 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][50]

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['start'] == 50, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['end'] == -1, "51 < start + 50 so the funtion should return 'end': -1"
    assert len(channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages']) == 1
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages'] == [{'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '1', 'time_created': 1}]


# Testing for between 100 and 150 messages with start being 0
def test_channel_messages_v1_111_messages_start_0():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)    
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    data = add_111_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['start'] == 0, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['end'] == 50, "111 > start + 50 - function should return 'end': 50"
    assert len(channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages']) == 50, "function should return 50 messages max"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][0] == {'message_id': 111, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "111", 'time_created': 111}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][25] == {'message_id': 86, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '86', 'time_created': 86}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][49] == {'message_id': 62, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '62', 'time_created': 62}

    # Raise an index error if trying to access beyond index 49 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 0)['messages'][50]


# Testing for between 100 and 150 messages with start being 50
def test_channel_messages_v1_111_messages_start_50():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    data = add_111_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['start'] == 50, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['end'] == 100, "111 > start + 50 - function should return 'end': 100"
    assert len(channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages']) == 50, "function should return 50 messages max"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages'][0] == {'message_id': 61, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "61", 'time_created': 61}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages'][25] == {'message_id': 36, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': "36", 'time_created': 36}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages'][49] == {'message_id': 12, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '12', 'time_created': 12}

    # Raise an index error if trying to access beyond index 49 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 50)['messages'][50]


# Testing for between 100 and 150 messages with start being 100
def test_channel_messages_v1_111_messages_start_100():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    data = add_111_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['start'] == 100, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['end'] == -1, "111 < start + 50 - function should return 'end': -1"
    assert len(channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['messages']) == 11, "function should return remaining 11 messages"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['messages'][0] == {'message_id': 11, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "11", 'time_created': 11}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['messages'][5] == {'message_id': 6, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '6', 'time_created': 6}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['messages'][10] == {'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '1', 'time_created': 1}

    # Raise an index error if trying to access beyond index 10 of ['messages']
    # as index 11 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 100)['messages'][11]

# TODO: Create a test for when start is not 0, 50, 100, 150 etc (e.g. start = 21) - should act normal with end being 71
# Test for when start is not a multiple of 50 and there are more than 50 messages remaining
def test_channel_messages_v1_start_21():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add members 1 and 2 into channel 1 and add 111 messages with the message just being the message id
    data = add_111_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['start'] == 21, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['end'] == 71, "End = start + 50 if the least recent message is not returned"

    # The 22nd most recent message of the whole channel is the first one to be returned
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][0] == {'message_id': 90, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '90', 'time_created': 90}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][25] == {'message_id': 65, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '65', 'time_created': 65}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][49] == {'message_id': 41, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '41', 'time_created': 41}

    # Raise an index error if trying to access beyond index 49 of ['messages']
    # as index 50 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][50]


# Test for when start is not a multiple of 50 and there are less than 50 messages remaining
def test_channel_messages_v1_start_21_end_neg1():
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    
    # Add members 1 and 2 into channel 1 and add 50 messages with the message just being the message id 
    data = add_50_messages(user1, user2, channel1)

    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['start'] == 21, "Start should not change"
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['end'] == -1, "50 < start + 50 if so return 'end': -1"

    # The 22nd most recent message of the whole channel is the first one to be returned
    # (essentially data['messages'][21] - the 21st index)
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][0] == {'message_id': 29, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '29', 'time_created': 29}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][25] == {'message_id': 4, 'u_id': data['users'][user2['auth_user_id']]['u_id'], 'message': '4', 'time_created': 4}
    assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][28] == {'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': '1', 'time_created': 1}

    # Raise an index error if trying to access beyond index 28 of ['messages']
    # as index 29 is meant to be out of range
    with pytest.raises(IndexError):
        assert channel_messages_v1(user1['auth_user_id'], channel1['channel_id'], 21)['messages'][29]
