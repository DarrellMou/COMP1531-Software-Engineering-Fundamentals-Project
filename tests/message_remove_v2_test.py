import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v1
from src.data import reset_data, retrieve_data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.message import message_send_v2, message_remove_v2

from uuid import uuid4


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# "Removing" a message just removes the text from the message and tags the
# message as removed

# It is impossible for a user to "remove" a message when there are no messages
# in the channel/dm (meaning nothing at all, not as in all messages are removed)

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

# Access error when the user trying to remove the message did not send the
# message OR is not an owner of the channel/dreams
def test_message_remove_v2_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = message_send_v2(user1, channel1, "Hello")['message_id']
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not owner/dreams member
    with pytest.raises(AccessError):
        assert message_remove_v2(user2, m_id)


# Input error when the message_id has already been removed
def test_message_remove_v2_InputError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']
    m_id1 = message_send_v2(user1, channel1, "Hello")['message_id']
    m_id2 = message_send_v2(user1, channel1, "Hello")['message_id']

    message_remove_v2(user1, m_id2)

    with pytest.raises(InputError):
        assert message_remove_v2(user1, m_id2)

############################ END EXCEPTION TESTING ############################


########################### TESTING MESSAGE REMOVE ############################


# Testing the removal of 1 message by user2
def test_message_remove_v2_remove_one():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and remove the very first message sent
    send_x_messages(user2, channel1, 3)
    data = retrieve_data()
    m_id = data['channels'][channel1]['messages'][0]['message_id']
    message_remove_v2(user2, m_id)

    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict2 = data['channels'][channel1]['messages'][2]
    
    answer = {
        'messages': [m_dict2, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user1, channel1, 0) == answer


# Testing the removal of multiple messages
def test_message_remove_v2_remove_multiple():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 5 messages and remove messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)
    data = retrieve_data()
    m_id0 = data['channels'][channel1]['messages'][0]['message_id']
    m_id2 = data['channels'][channel1]['messages'][2]['message_id']
    m_id3 = data['channels'][channel1]['messages'][3]['message_id']
    message_remove_v2(user2, m_id0)
    message_remove_v2(user2, m_id2)
    message_remove_v2(user2, m_id3)

    data=retrieve_data()
    m_dict1 = data['channels'][channel1]['messages'][1]
    m_dict4 = data['channels'][channel1]['messages'][4]

    answer = {
        'messages': [m_dict4, m_dict1],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == answer


# Testing the removal of all messages in the channel
def test_message_remove_v2_remove_all():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    data = retrieve_data()
    send_x_messages(user2, channel1, 25)
    m_ids = [data['channels'][channel1]['messages'][x]['message_id'] for x in range(0, 25)]
    remove_x_messages(user2, m_ids)

    answer = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == answer


# Testing the removal of a message by the owner of the channel when the owner
# didn't send the message
def test_message_remove_v2_owner_removes_message():
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])

    # user3 sends 3 messages and user2 removes the very first message sent
    send_x_messages(user3['token'], channel1, 3)
    m_id = data['channels'][channel1]['messages'][1]['message_id']
    message_remove_v2(user2['token'], m_id)

    data = retrieve_data()

    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# Testing the removal of a message by the owner of dreams when the owner did
# not send the message and is not part of the channel
def test_message_remove_v2_dream_owner_removes_message():
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3['token'], channel1, 3)
    m_id = data['channels'][channel1]['messages'][1]['message_id']
    message_remove_v2(user1['token'], m_id)

    data = retrieve_data()

    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# Testing the removal of a message by the owner of dreams when the owner did
# not send the message and is part of the channel
def test_message_remove_v2_dream_owner_removes_message_in_channel():
    data = reset_data()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder') # Dreams owner
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('thomas.tankengine@email.com', 'password123', 'Thomas', 'Tankengine')
    channel1 = channels_create_v1(user2['auth_user_id'], 'Channel1', True)['channel_id']
    channel_invite_v1(user2['auth_user_id'], channel1, user3['auth_user_id'])
    channel_invite_v1(user2['auth_user_id'], channel1, user1['auth_user_id'])

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3['token'], channel1, 3)
    m_id = data['channels'][channel1]['messages'][1]['message_id']
    message_remove_v2(user1['token'], m_id)

    data = retrieve_data()

    m_dict0 = data['channels'][channel1]['messages'][0]
    m_dict2 = data['channels'][channel1]['messages'][2]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2['token'], channel1, 0) == answer


# Testing the removal of the same message in 2 different channels (different
# message_ids though)
def test_message_remove_v2_remove_same_msg_diff_channels():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    u_id2 = auth_decode_token(user2)
    channel2 = channels_create_v1(u_id2, 'Channel2', True)['channel_id']

    data = retrieve_data()
    # Have user2 send the same message to channel1 and channel2 and then
    # remove both the messages
    message_send_v2(user2, channel1, "Hello")
    message_send_v2(user2, channel2, "Hello")
    m_id_ch1 = data['channels'][channel1]['messages'][0]['message_id']
    m_id_ch2 = data['channels'][channel2]['messages'][0]['message_id']
    message_remove_v2(user2, m_id_ch1)
    message_remove_v2(user2, m_id_ch2)

    ans1 = {
        'messages': [],
        'start': 0,
        'end': -1
    }
    ans2 = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    assert channel_messages_v2(user2, channel1, 0) == ans1
    assert channel_messages_v2(user2, channel2, 0) == ans2