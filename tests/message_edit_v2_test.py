import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v1
from src.data import reset_data, retrieve_data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.message import message_send_v2, message_remove_v2, message_edit_v2


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################




###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates channel_1 with member u_id = 1
def set_up_data():
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1 and
    # invite user2 to the channel
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])

    setup = {
        'user1': user1['token'],
        'user2': user2['token'],
        'channel1': channel1['channel_id']
    }

    return setup


# User sends x messages
def send_x_messages(user, channel, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_send_v2(user, channel, str(message_num))
        message_count += 1
    
    return data

# User removes x messages
def remove_x_messages(user, id_list=[]):
    data = retrieve_data()
    message_count = 0
    while message_count < len(id_list):
        message_remove_v2(user, id_list[message_count])
        message_count += 1
    
    return data



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if message is of valid length
def test_message_edit_v2_InputError_msg_too_long():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    with pytest.raises(InputError):
        assert message_edit_v2(user1, m_id, long_message)


# Testing to see if message being edited has already been removed
def test_message_edit_v2_InputError_msg_removed():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']
    m_id1 = message_send_v2(user1, channel1, "Hello")['message_id']
    m_id2 = message_send_v2(user1, channel1, "Hello")['message_id']

    message_remove_v2(user1, m_id2)

    with pytest.raises(InputError):
        assert message_edit_v2(user1, m_id2, "Hi")


# Access error when the user trying to edit the message did not send the
# message OR is not an owner of the channel/dreams
def test_message_edit_v2_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = message_send_v2(user1, channel1, "Hello")['message_id']
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not channel/dreams owner
    with pytest.raises(AccessError):
        assert message_edit_v2(user2, m_id, "Hi")


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE EDIT #############################

# Testing the edit of 1 message by user2
def test_message_edit_v2_edit_one():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)
    data = retrieve_data()
    m_id = data['channels'][channel1]['messages'][0]['message_id']
    messages_info = data['channels'][channel1]['messages'][0]
    message_edit_v2(user2, m_id, "HI")

    m_dict0 = {
        'message_id': messages_info['message_id'],
        'u_id': messages_info['u_id'],
        'message': 'HI',
        'time_created': messages_info['time_created'],
    }
    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict2 = data['channels'][channel1]['messages'][2]
    
    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user1, channel1, 0) == answer


# Testing the edit of multiple messages
def test_message_edit_v2_edit_multiple():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)
    data = retrieve_data()
    msg0 = data['channels'][channel1]['messages'][0]
    msg2 = data['channels'][channel1]['messages'][2]
    msg3 = data['channels'][channel1]['messages'][3]
    message_edit_v2(user2, msg0['message_id'], "Hi")
    message_edit_v2(user2, msg2['message_id'], "Hello")
    message_edit_v2(user2, msg3['message_id'], "Hey")

    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hi',
        'time_created': msg0['time_created'],
    }
    m_dict2 = {
        'message_id': msg2['message_id'],
        'u_id': msg2['u_id'],
        'message': 'Hello',
        'time_created': msg2['time_created'],
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Hey',
        'time_created': msg3['time_created'],
    }

    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict4 = data['channels'][channel1]['messages'][4]

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == answer


# Editing all messages in the channel
def test_message_edit_v2_edit_all_messages():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)
    data = retrieve_data()
    msg0 = data['channels'][channel1]['messages'][0]
    msg1 = data['channels'][channel1]['messages'][1]
    msg2 = data['channels'][channel1]['messages'][2]
    msg3 = data['channels'][channel1]['messages'][3]
    msg4 = data['channels'][channel1]['messages'][4]
    message_edit_v2(user2, msg0['message_id'], "Hi")
    message_edit_v2(user2, msg1['message_id'], "Hello")
    message_edit_v2(user2, msg2['message_id'], "Hey")
    message_edit_v2(user2, msg3['message_id'], "Goodbye")
    message_edit_v2(user2, msg4['message_id'], "Bye")


    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hi',
        'time_created': msg0['time_created'],
    }
    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Hello',
        'time_created': msg1['time_created'],
    }
    m_dict2 = {
        'message_id': msg2['message_id'],
        'u_id': msg2['u_id'],
        'message': 'Hey',
        'time_created': msg3['time_created'],
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Goodbye',
        'time_created': msg3['time_created'],
    }
    m_dict4 = {
        'message_id': msg4['message_id'],
        'u_id': msg4['u_id'],
        'message': 'Bye',
        'time_created': msg4['time_created'],
    }

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == answer


# Owner of the channel edits the message when the owner didn't send the message
def test_message_edit_v2_owner_edits_message():
    data = retrieve_data()
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])

    # user3 sends 3 messages and user2 edits the very first message sent
    send_x_messages(user3['token'], channel1, 3)
    msg1 = data['channels'][channel1]['messages'][1]
    message_edit_v2(user2['token'], msg1['message_id'], "Bao")

    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Bao',
        'time_created': msg1['time_created'],
    }
    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# The owner of dreams edits a message owner did not send the message and is not
# part of the channel
def test_message_edit_v2_dream_owner_edits_message():
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3['token'], channel1, 3)
    msg1 = data['channels'][channel1]['messages'][1]
    message_edit_v2(user1['token'], msg1['message_id'], "HELLO!")

    data = retrieve_data()
    
    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'HELLO!',
        'time_created': msg1['time_created'],
    }
    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# The owner of dreams edits a message when the owner did
# not send the message and is part of the channel
def test_message_edit_v2_dream_owner_edits_message_in_channel():
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])
    channel_invite_v1(user2['auth_user_id'], channel1, user1['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # edits the second message sent
    send_x_messages(user3['token'], channel1, 3)
    msg1 = data['channels'][channel1]['messages'][1]
    message_edit_v2(user1['token'], msg1['message_id'], "Testing")

    data = retrieve_data()

    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Testing',
        'time_created': msg1['time_created'],
    }
    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# Editing a message and replacing it with empty string to see if it
# removes the message
def test_message_edit_v2_edit_removes_1_msg():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)
    data = retrieve_data()
    m_id = data['channels'][channel1]['messages'][0]['message_id']
    messages_info = data['channels'][channel1]['messages'][0]
    message_edit_v2(user2, m_id, "")

    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict2 = data['channels'][channel1]['messages'][2]
    
    answer = {
        'messages': [m_dict2, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user1, channel1, 0) == answer


# Editing multiple messages and replacing them with empty string to see if it
# removes the message
def test_message_edit_v2_edit_removes_multiple_msg():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3 
    send_x_messages(user2, channel1, 5)
    data = retrieve_data()
    msg0 = data['channels'][channel1]['messages'][0]
    msg2 = data['channels'][channel1]['messages'][2]
    msg3 = data['channels'][channel1]['messages'][3]
    message_edit_v2(user2, msg0['message_id'], "")
    message_edit_v2(user2, msg2['message_id'], "")
    message_edit_v2(user2, msg3['message_id'], "")

    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict4 = data['channels'][channel1]['messages'][4]

    answer = {
        'messages': [m_dict4, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == answer
