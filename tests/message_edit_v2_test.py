# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_senddm_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# User sends x messages
def send_x_messages(user, channel, num_messages):
    message_count = 0
    msg_list = []
    while message_count < num_messages:
        message_num = message_count + 1
        m_id = message_send_v2(user["token"], channel, str(message_num))
        msg_list.append(m_id)
        message_count += 1
    
    return msg_list

# User removes x messages
def remove_x_messages(user, id_list=[]):
    message_count = 0
    while message_count < len(id_list):
        message_remove_v1(user["token"], id_list[message_count])
        message_count += 1
    
    return {}



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if message is of valid length
def test_message_edit_v2_InputError_msg_too_long(set_up_message_data):
    setup = set_up_message_data
    user1, channel1 = setup['user1'], setup['channel1']
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    with pytest.raises(InputError):
        assert message_edit_v2(user1["token"], m_id, long_message)


# Testing to see if message being edited has already been removed
def test_message_edit_v2_InputError_msg_removed(set_up_message_data):
    setup = set_up_message_data
    user1, channel1 = setup['user1'], setup['channel1']
    
    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']

    message_remove_v1(user1["token"], m_id)

    with pytest.raises(InputError):
        assert message_edit_v2(user1["token"], m_id, "Hi")


def test_message_edit_v2_AccessError_not_dm_owner(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    m_id = message_senddm_v1(user1["token"], dm1, "Hello")['message_id']
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not dm owner/dreams member
    with pytest.raises(AccessError):
        assert message_edit_v2(user2["token"], m_id, "Hi")


# Access error when the user trying to edit the message did not send the
# message OR is not an owner of the channel/dreams
def test_message_edit_v2_AccessError(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = message_send_v2(user1["token"], channel1, "Hello")['message_id']
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not channel/dreams owner
    with pytest.raises(AccessError):
        assert message_edit_v2(user2["token"], m_id, "Hi")


# Default access error when token is invalid
def test_message_edit_v2_default_Access_Error():

    with pytest.raises(AccessError):
        message_edit_v2("invalid token", 123, "hello")


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE EDIT #############################

# Testing the edit of 1 message by user2
def test_message_edit_v2_edit_one(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)

    channel_msgs = channel_messages_v2(user1["token"], channel1, 0)

    m_id = channel_msgs["messages"][2]["message_id"]
    messages_info = channel_msgs["messages"][2]
    message_edit_v2(user2["token"], m_id, "HI")

    m_dict0 = {
        'message_id': messages_info['message_id'],
        'u_id': messages_info['u_id'],
        'message': 'HI',
        'time_created': messages_info['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict1 = channel_msgs["messages"][1]
    m_dict2 = channel_msgs["messages"][0]
    
    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user1["token"], channel1, 0) == answer


# Testing the edit of multiple messages
def test_message_edit_v2_edit_multiple(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)

    channel_msgs = channel_messages_v2(user1["token"], channel1, 0)
    msg0 = channel_msgs["messages"][4]
    msg2 = channel_msgs["messages"][2]
    msg3 = channel_msgs["messages"][1]
    message_edit_v2(user2["token"], msg0['message_id'], "Hi")
    message_edit_v2(user2["token"], msg2['message_id'], "Hello")
    message_edit_v2(user2["token"], msg3['message_id'], "Hey")

    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hi',
        'time_created': msg0['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict2 = {
        'message_id': msg2['message_id'],
        'u_id': msg2['u_id'],
        'message': 'Hello',
        'time_created': msg2['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Hey',
        'time_created': msg3['time_created'],
        'reacts': [],
        'is_pinned': False
    }

    m_dict1 = channel_msgs["messages"][3]
    m_dict4 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2["token"], channel1, 0) == answer


# Editing all messages in the channel
def test_message_edit_v2_edit_all_messages(set_up_message_data):
    setup = set_up_message_data
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)

    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)
    msg0 = channel_msgs["messages"][4]
    msg1 = channel_msgs["messages"][3]
    msg2 = channel_msgs["messages"][2]
    msg3 = channel_msgs["messages"][1]
    msg4 = channel_msgs["messages"][0]
    message_edit_v2(user2["token"], msg0['message_id'], "Hi")
    message_edit_v2(user2["token"], msg1['message_id'], "Hello")
    message_edit_v2(user2["token"], msg2['message_id'], "Hey")
    message_edit_v2(user2["token"], msg3['message_id'], "Goodbye")
    message_edit_v2(user2["token"], msg4['message_id'], "Bye")


    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hi',
        'time_created': msg0['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Hello',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict2 = {
        'message_id': msg2['message_id'],
        'u_id': msg2['u_id'],
        'message': 'Hey',
        'time_created': msg3['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Goodbye',
        'time_created': msg3['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict4 = {
        'message_id': msg4['message_id'],
        'u_id': msg4['u_id'],
        'message': 'Bye',
        'time_created': msg4['time_created'],
        'reacts': [],
        'is_pinned': False
    }

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2["token"], channel1, 0) == answer


# Owner of the channel edits the message when the owner didn't send the message
def test_message_edit_v2_owner_edits_message():
    clear_v1()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v2(user2['token'], 'Channel1', True)['channel_id']
    channel_invite_v2(user2['token'], channel1, user3['auth_user_id'])
    channel_invite_v2(user2['token'], channel1, user1['auth_user_id'])


    # user3 sends 3 messages and user2 edits the second message sent
    send_x_messages(user3, channel1, 3)

    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)    
    msg1 = channel_msgs["messages"][1]
    message_edit_v2(user2['token'], msg1['message_id'], "Bao")

    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Bao',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict0 = channel_msgs['messages'][2]
    m_dict2 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# The owner of dreams edits a message owner did not send the message and is not
# part of the channel
def test_message_edit_v2_dream_owner_edits_message():
    clear_v1()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v2(user2['token'], 'Channel1', True)['channel_id']
    channel_invite_v2(user2['token'], channel1, user3['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3, channel1, 3)
    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)
    msg1 = channel_msgs["messages"][1]
    message_edit_v2(user1['token'], msg1['message_id'], "HELLO!")
    
    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'HELLO!',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict0 = channel_msgs["messages"][2]
    m_dict2 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# The owner of dreams edits a message when the owner did
# not send the message and is part of the channel
def test_message_edit_v2_dream_owner_edits_message_in_channel():
    clear_v1()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v2(user2["token"], 'Channel1', True)['channel_id']
    channel_invite_v2(user2['token'], channel1, user3['auth_user_id'])
    channel_invite_v2(user2['token'], channel1, user1['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # edits the second message sent
    send_x_messages(user3, channel1, 3)
    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)
    msg1 = channel_msgs["messages"][1]
    message_edit_v2(user1['token'], msg1['message_id'], "Testing")

    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Testing',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict0 = channel_msgs["messages"][2]
    m_dict2 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# Editing a message and replacing it with empty string to see if it
# removes the message
def test_message_edit_v2_edit_removes_1_msg(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)
    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)
    msg1 = channel_msgs["messages"][2]
    message_edit_v2(user2["token"], msg1["message_id"], "")

    m_dict1 = channel_msgs['messages'][1]
    m_dict2 = channel_msgs['messages'][0]
    
    answer = {
        'messages': [m_dict2, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user1["token"], channel1, 0) == answer


# Editing multiple messages and replacing them with empty string to see if it
# removes the message
def test_message_edit_v2_edit_removes_multiple_msg(set_up_message_data):
    setup = set_up_message_data
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3 
    send_x_messages(user2, channel1, 5)
    channel_msgs = channel_messages_v2(user2["token"], channel1, 0)
    msg0 = channel_msgs['messages'][4]
    msg2 = channel_msgs['messages'][2]
    msg3 = channel_msgs['messages'][1]
    message_edit_v2(user2["token"], msg0['message_id'], "")
    message_edit_v2(user2["token"], msg2['message_id'], "")
    message_edit_v2(user2["token"], msg3['message_id'], "")

    m_dict1 = channel_msgs['messages'][3]
    m_dict4 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict4, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2["token"], channel1, 0) == answer


# Edit messages within a dm
def test_message_edit_v2_edit_msg_in_dm(set_up_message_data):
    setup = set_up_message_data
    user1, dm1 = setup['user1'], setup['dm1']

    message_count = 0
    while message_count < 5:
        message_num = message_count + 1
        message_senddm_v1(user1["token"], dm1, str(message_num))
        message_count += 1

    dm_msgs = dm_messages_v1(user1["token"], dm1, 0)

    msg0 = dm_msgs['messages'][4]
    msg2 = dm_msgs['messages'][2]
    msg3 = dm_msgs['messages'][1]
    message_edit_v2(user1["token"], msg0['message_id'], "Hey")
    message_edit_v2(user1["token"], msg2['message_id'], "")
    message_edit_v2(user1["token"], msg3['message_id'], "Hello")

    m_dict1 = dm_msgs['messages'][3]
    m_dict4 = dm_msgs['messages'][0]

    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hey',
        'time_created': msg0['time_created'],
        'reacts': [],
        'is_pinned': False
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Hello',
        'time_created': msg3['time_created'],
        'reacts': [],
        'is_pinned': False
    }

    answer = {
        'messages': [m_dict4, m_dict3, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    assert dm_messages_v1(user1["token"], dm1, 0) == answer
