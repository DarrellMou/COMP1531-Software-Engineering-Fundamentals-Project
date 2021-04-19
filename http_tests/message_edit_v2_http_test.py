# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import json
import requests
import pytest
from src.config import url


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if message is of valid length
def test_http_message_edit_v2_InputError_msg_too_long(set_up_message_data):
    setup = set_up_message_data
    user1, channel1 = setup['user1'], setup['channel1']
    m_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    assert requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": m_id["message_id"],
        "message": long_message
    }).status_code == 400


# Testing to see if message being edited has already been removed
def test_http_message_edit_v2_InputError_msg_removed(set_up_message_data):
    setup = set_up_message_data
    user1, channel1 = setup['user1'], setup['channel1']
    
    m_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": m_id["message_id"]
    }).json()


    assert requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": m_id["message_id"],
        "message": "Hi"
    }).status_code == 400


# Access error when the user trying to edit the message did not send the
# message OR is not an owner of the channel/dreams
def test_http_message_edit_v2_AccessError(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not channel/dreams owner
    assert requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id["message_id"],
        "message": "Hi"
    }).status_code == 403


def test_message_edit_v2_AccessError_not_dm_owner(set_up_message_data):
    setup = set_up_message_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    m_id = requests.post(f"{url}message/senddm/v1", json= {
        "token": user1["token"],
        "dm_id": dm1,
        "message": "Hello"
    }).json()
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not dm owner/dreams member
    assert requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id["message_id"],
        "message": "Hi"
    }).status_code == 403



# Default access error when token is invalid
def test_http_message_edit_v2_default_Access_Error():

    assert requests.put(f"{url}message/edit/v2", json={
        "token": "Invalid",
        "message_id": 123,
        "message": "Hi"
    }).status_code == 403


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE EDIT #############################

# Testing the edit of 1 message by user2
def test_http_message_edit_v2_edit_one(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)

    channel_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    m_id = channel_messages["messages"][2]["message_id"]

    messages_info = channel_messages["messages"][2]

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id,
        "message": "Hi"
    }).json()

    m_dict0 = {
        'message_id': messages_info['message_id'],
        'u_id': messages_info['u_id'],
        'message': 'Hi',
        'time_created': messages_info['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict1 = channel_messages["messages"][1]
    m_dict2 = channel_messages["messages"][0]
    
    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Testing the edit of multiple messages
def test_http_message_edit_v2_edit_multiple(set_up_message_data):
    setup = set_up_message_data
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    m_id0 = channel_msgs["messages"][4]
    m_id2 = channel_msgs["messages"][2]
    m_id3 = channel_msgs["messages"][1]

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id0["message_id"],
        "message": "Hi"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id2["message_id"],
        "message": "Hello"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id3["message_id"],
        "message": "Hey"
    }).json()

    m_dict0 = {
        'message_id': m_id0['message_id'],
        'u_id': m_id0['u_id'],
        'message': 'Hi',
        'time_created': m_id0['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict2 = {
        'message_id': m_id2['message_id'],
        'u_id': m_id2['u_id'],
        'message': 'Hello',
        'time_created': m_id2['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict3 = {
        'message_id': m_id3['message_id'],
        'u_id': m_id3['u_id'],
        'message': 'Hey',
        'time_created': m_id3['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    m_dict1 = channel_msgs["messages"][3]
    m_dict4 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }
    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Editing all messages in the channel
def test_http_message_edit_v2_edit_all_messages(set_up_message_data):
    setup = set_up_message_data
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3
    send_x_messages(user2, channel1, 5)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    m_id0 = channel_msgs["messages"][4]
    m_id1 = channel_msgs["messages"][3]
    m_id2 = channel_msgs["messages"][2]
    m_id3 = channel_msgs["messages"][1]
    m_id4 = channel_msgs["messages"][0]

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id0["message_id"],
        "message": "Hi"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id1["message_id"],
        "message": "Hello"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id2["message_id"],
        "message": "Hey"
    }).json()    
    
    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id3["message_id"],
        "message": "Goodbye"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": m_id4["message_id"],
        "message": "Bye"
    }).json()


    m_dict0 = {
        'message_id': m_id0['message_id'],
        'u_id': m_id0['u_id'],
        'message': 'Hi',
        'time_created': m_id0['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    m_dict1 = {
        'message_id': m_id1['message_id'],
        'u_id': m_id1['u_id'],
        'message': 'Hello',
        'time_created': m_id1['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    m_dict2 = {
        'message_id': m_id2['message_id'],
        'u_id': m_id2['u_id'],
        'message': 'Hey',
        'time_created': m_id2['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    m_dict3 = {
        'message_id': m_id3['message_id'],
        'u_id': m_id3['u_id'],
        'message': 'Goodbye',
        'time_created': m_id3['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    m_dict4 = {
        'message_id': m_id4['message_id'],
        'u_id': m_id4['u_id'],
        'message': 'Bye',
        'time_created': m_id4['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    answer = {
        'messages': [m_dict4, m_dict3, m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Owner of the channel edits the message when the owner didn't send the message
def test_http_message_edit_v2_owner_edits_message():
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { # Dreams owner
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    }).json()

    user2 = requests.post(f"{url}auth/register/v2", json = {
        "email": "shaun.sheep@email.com",
        "password": "password123",
        "name_first": "Shaun",
        "name_last": "Sheep"
    }).json()

    user3 = requests.post(f"{url}auth/register/v2", json = {
        "email": "thomas.tankengine@email.com",
        "password": "password123",
        "name_first": "Thomas",
        "name_last": "Tankengine"
    }).json()

    # User2 makes channel1 and invites user3
    channel1 = requests.post(f"{url}channels/create/v2", json = {
        "token": user2["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user3["auth_user_id"]
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user1["auth_user_id"]
    }).json()

    # user3 sends 3 messages and user2 edits the very first message sent
    send_x_messages(user3, channel1["channel_id"], 3)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    msg1 = channel_msgs['messages'][1]
    
    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": msg1["message_id"],
        "message": "Bao"
    }).json()

    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Bao',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict0 = channel_msgs['messages'][2]
    m_dict2 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }
    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# The owner of dreams edits a message owner did not send the message and is not
# part of the channel
def test_http_message_edit_v2_dream_owner_edits_message():
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { # Dreams owner
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    }).json()

    user2 = requests.post(f"{url}auth/register/v2", json = {
        "email": "shaun.sheep@email.com",
        "password": "password123",
        "name_first": "Shaun",
        "name_last": "Sheep"
    }).json()

    user3 = requests.post(f"{url}auth/register/v2", json = {
        "email": "thomas.tankengine@email.com",
        "password": "password123",
        "name_first": "Thomas",
        "name_last": "Tankengine"
    }).json()

    # User2 makes channel1 and invites user3
    channel1 = requests.post(f"{url}channels/create/v2", json = {
        "token": user2["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user3["auth_user_id"]
    }).json()

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3, channel1["channel_id"], 3)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    msg1 = channel_msgs['messages'][1]

    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg1["message_id"],
        "message": "HELLO!"
    }).json()

    
    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'HELLO!',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict0 = channel_msgs['messages'][2]
    m_dict2 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# The owner of dreams edits a message when the owner did
# not send the message and is part of the channel
def test_http_message_edit_v2_dream_owner_edits_message_in_channel():
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { # Dreams owner
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    }).json()

    user2 = requests.post(f"{url}auth/register/v2", json = {
        "email": "shaun.sheep@email.com",
        "password": "password123",
        "name_first": "Shaun",
        "name_last": "Sheep"
    }).json()

    user3 = requests.post(f"{url}auth/register/v2", json = {
        "email": "thomas.tankengine@email.com",
        "password": "password123",
        "name_first": "Thomas",
        "name_last": "Tankengine"
    }).json()

    # User2 makes channel1 and invites user3 and user1
    channel1 = requests.post(f"{url}channels/create/v2", json = {
        "token": user2["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user3["auth_user_id"]
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user1["auth_user_id"]
    }).json()


    # user3 sends 3 messages and user1 (dreams owner) who is in the channel
    # edits the second message sent (which they did not send)
    send_x_messages(user3, channel1["channel_id"], 3)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    msg1 = channel_msgs['messages'][1]

    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg1["message_id"],
        "message": "Testing?"
    }).json()


    m_dict1 = {
        'message_id': msg1['message_id'],
        'u_id': msg1['u_id'],
        'message': 'Testing?',
        'time_created': msg1['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict0 = channel_msgs['messages'][2]
    m_dict2 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict2, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Editing a message and replacing it with empty string to see if it
# removes the message
def test_http_message_edit_v2_edit_removes_1_msg(set_up_message_data):
    setup = set_up_message_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # Send 3 messages and edit the very first message sent
    send_x_messages(user2, channel1, 3)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    msg1 = channel_msgs['messages'][2]

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": msg1["message_id"],
        "message": ""
    }).json()

    m_dict1 = channel_msgs['messages'][1]
    m_dict2 = channel_msgs['messages'][0]
    
    answer = {
        'messages': [m_dict2, m_dict1],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Editing multiple messages and replacing them with empty string to see if it
# removes the message
def test_http_message_edit_v2_edit_removes_multiple_msg(set_up_message_data):
    setup = set_up_message_data
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and edit messages with index 0, 2, 3 
    send_x_messages(user2, channel1, 5)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    msg0 = channel_msgs['messages'][4]
    msg2 = channel_msgs['messages'][2]
    msg3 = channel_msgs['messages'][1]

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": msg0["message_id"],
        "message": ""
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": msg2["message_id"],
        "message": ""
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user2["token"],
        "message_id": msg3["message_id"],
        "message": ""
    }).json()

    m_dict1 = channel_msgs['messages'][3]
    m_dict4 = channel_msgs['messages'][0]

    answer = {
        'messages': [m_dict4, m_dict1],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer



# Edit messages within a dm
def test_message_edit_v2_edit_msg_in_dm(set_up_message_data):
    setup = set_up_message_data
    user1, dm1 = setup['user1'], setup['dm1']

    message_count = 0
    while message_count < 5:
        message_num = message_count + 1
        requests.post(f"{url}message/senddm/v1", json= {
            "token": user1["token"],
            "dm_id": dm1,
            "message": str(message_num)
        }).json()
        message_count += 1

    dm_msgs = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    msg0 = dm_msgs['messages'][4]
    msg2 = dm_msgs['messages'][2]
    msg3 = dm_msgs['messages'][1]

    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg0["message_id"],
        "message": "Hey"
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg2["message_id"],
        "message": ""
    }).json()

    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg3["message_id"],
        "message": "Hello"
    }).json()

    m_dict1 = dm_msgs['messages'][3]
    m_dict4 = dm_msgs['messages'][0]

    m_dict0 = {
        'message_id': msg0['message_id'],
        'u_id': msg0['u_id'],
        'message': 'Hey',
        'time_created': msg0['time_created'],
        'reacts': [],
        'is_pinned': False,
    }
    m_dict3 = {
        'message_id': msg3['message_id'],
        'u_id': msg3['u_id'],
        'message': 'Hello',
        'time_created': msg3['time_created'],
        'reacts': [],
        'is_pinned': False,
    }

    answer = {
        'messages': [m_dict4, m_dict3, m_dict1, m_dict0],
        'start': 0,
        'end': -1
    }


    dm_messages_answer = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    assert dm_messages_answer == answer


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################
# User sends x messages
def send_x_messages(user1, channel1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        requests.post(f"{url}message/send/v2", json= {
            "token": user1["token"],
            "channel_id": channel1,
            "message": str(message_num)
        }).json()
        message_count += 1

    return {}


# User removes x messages
def remove_x_messages(user, id_list=[]):
    message_count = 0
    while message_count < len(id_list):
        requests.delete(f"{url}message/remove/v1", json= {
            "token": user["token"],
            "message_id": id_list[message_count]
        }).json()
        message_count += 1
    
    return {}
