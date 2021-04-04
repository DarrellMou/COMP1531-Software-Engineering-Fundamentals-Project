import json
import requests
import pytest
from src.config import url


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
def set_up_data():
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = {
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

    channel1 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "u_id": user2["auth_user_id"]
    }).json()

    dm1 = requests.post(f"{url}dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [user2["auth_user_id"]]
    }).json()

    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1["channel_id"],
        "dm1": dm1["dm_id"]
    }


    return setup

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


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Access error when the user trying to remove the message did not send the
# message OR is not an owner of the channel/dreams
def test_http_message_remove_v1_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    print(str(channel1) + "\n\n\n")
    m_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not owner/dreams member
    assert requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id["message_id"]
    }).status_code == 403


# Input error when the message_id has already been removed
def test_http_message_remove_v1_InputError():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']
    
    msg1 = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": msg1["message_id"],
    }).json()

    assert requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": msg1["message_id"],
    }).status_code == 400


def test_message_remove_v1_AccessError_not_dm_owner():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    msg1 = requests.post(f"{url}message/senddm/v1", json= {
        "token": user1["token"],
        "dm_id": dm1,
        "message": "Hello"
    }).json()
    
    # user2 who did not send the message with m_id tries to remove the message 
    # - should raise an access error as they are not owner/dreams member
    assert requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": msg1["message_id"],
    }).status_code == 403

############################ END EXCEPTION TESTING ############################


########################### TESTING MESSAGE REMOVE ############################

# Testing the removal of 1 message by user2
def test_http_message_remove_v1_remove_one():
    setup = set_up_data()
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 3 messages and remove the very first message sent
    send_x_messages(user2, channel1, 3)

    channel_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    m_id = channel_messages["messages"][2]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id,
    }).json()

    channel_msgs1 = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()
    m_dict1 = channel_msgs1["messages"][0]

    channel_msgs2 = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()
    m_dict2 = channel_msgs2["messages"][1]
    
    answer = {
        'messages': [m_dict1, m_dict2],
        'start': 0,
        'end': -1
    }

    channel_messages_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages_answer == answer


# Testing the removal of multiple messages
def test_http_message_remove_v1_remove_multiple():
    setup = set_up_data()
    user2, channel1 = setup['user2'], setup['channel1']

    # Send 5 messages and remove messages with index 0, 2, 3 (in the channel
    # messages list, not the list created by channel_messages function)
    send_x_messages(user2, channel1, 5)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    m_id0 = channel_msgs["messages"][4]["message_id"]
    m_id2 = channel_msgs["messages"][2]["message_id"]
    m_id3 = channel_msgs["messages"][1]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id0,
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id2,
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id3,
    }).json()

    m_dict1 = channel_msgs["messages"][3]
    m_dict4 = channel_msgs["messages"][0]

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


# Testing the removal of all messages in the channel
def test_http_message_remove_v1_remove_all():
    setup = set_up_data()
    user2, channel1 = setup['user2'], setup['channel1']

    send_x_messages(user2, channel1, 25)

    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()
    reversed_channel_msgs = channel_msgs["messages"][::-1]
    m_ids = [reversed_channel_msgs[i]["message_id"] for i in range(25)]
    remove_x_messages(user2, m_ids)

    answer = {
        'messages': [],
        'start': 0,
        'end': -1
    }

    channel_msgs_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_msgs_answer == answer


# Testing the removal of a message by the owner of the channel when the owner
# didn't send the message
def test_http_message_remove_v1_owner_removes_message():
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

    # User2 makes channel1 and invites user3 and user 1
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

    # user3 sends 3 messages and user2 removes the very first message sent
    send_x_messages(user3, channel1["channel_id"], 3)
    
    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    m_id = channel_msgs["messages"][1]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id,
    }).json()


    m_dict0 = channel_msgs["messages"][2]
    m_dict2 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_msgs_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_msgs_answer == answer


# Testing the removal of a message by the owner of dreams when the owner did
# not send the message and is not part of the channel
def test_http_message_remove_v1_dream_owner_removes_message():

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

    m_id = channel_msgs["messages"][1]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": m_id,
    }).json()


    m_dict0 = channel_msgs["messages"][2]
    m_dict2 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_msgs_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_msgs_answer == answer


# Testing the removal of a message by the owner of dreams when the owner did
# not send the message and is part of the channel
def test_http_message_remove_v1_dream_owner_removes_message_in_channel():
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

    # user3 sends 3 messages and user1 (dreams owner) who is not in the channel
    # removes the very first message sent
    send_x_messages(user3, channel1["channel_id"], 3)
    channel_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    m_id = channel_msgs["messages"][1]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": m_id,
    }).json()

    m_dict0 = channel_msgs["messages"][2]
    m_dict2 = channel_msgs["messages"][0]

    answer = {
        'messages': [m_dict2, m_dict0],
        'start': 0,
        'end': -1
    }

    channel_msgs_answer = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert channel_msgs_answer == answer


# Testing the removal of the same message in 2 different channels (different
# message_ids though)
def test_http_message_remove_v1_remove_same_msg_diff_channels():
    setup = set_up_data()
    user2, channel1 = setup['user2'], setup['channel1']

    channel2 = requests.post(f"{url}channels/create/v2", json = {
        "token": user2["token"],
        "name": "Channel2",
        "is_public": True
    }).json()

    # Have user2 send the same message to channel1 and channel2 and then
    # remove both the messages
    requests.post(f"{url}message/send/v2", json= {
        "token": user2["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    requests.post(f"{url}message/send/v2", json= {
        "token": user2["token"],
        "channel_id": channel2["channel_id"],
        "message": "Hello"
    }).json()


    channel1_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_msgs = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel2["channel_id"],
        "start": 0
    }).json()

    m_id_ch1 = channel1_msgs["messages"][0]["message_id"]
    m_id_ch2 = channel2_msgs["messages"][0]["message_id"]

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id_ch1,
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user2["token"],
        "message_id": m_id_ch2,
    }).json()

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


    channel1_msgs_ans = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel1,
        "start": 0
    }).json()


    channel2_msgs_ans = requests.get(f"{url}channel/messages/v2", params= {
        "token": user2["token"],
        "channel_id": channel2["channel_id"],
        "start": 0
    }).json()

    assert channel1_msgs_ans == ans1
    assert channel2_msgs_ans == ans2


# Testing the removal of messages within a dm
def test_message_edit_v2_edit_msg_in_dm():
    setup = set_up_data()
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

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": msg0["message_id"]
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": msg2["message_id"]
    }).json()

    requests.delete(f"{url}message/remove/v1", json={
        "token": user1["token"],
        "message_id": msg3["message_id"]
    }).json()

    m_dict1 = dm_msgs['messages'][3]
    m_dict4 = dm_msgs['messages'][0]

    answer = {
        'messages': [m_dict4, m_dict1],
        'start': 0,
        'end': -1
    }

    dm_messages_answer = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    print(dm_messages_answer)
    print("\n\n\n\n")
    print(answer)

    assert dm_messages_answer == answer
