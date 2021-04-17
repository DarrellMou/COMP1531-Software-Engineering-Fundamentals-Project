# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import json
import requests
import urllib

from src.config import url


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################
# Testing for when the user is not part of the channel
def test_http_message_unpin_v1_AccessError(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    m_id = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "HEY EVERYBODY")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    # user2 who is not a part of channel1 tries to unpin message 
    # - should raise an access error
    response = requests.post(f"{url}message/unpin/v1", json=message_pin_body(user2, m_id["message_id"]))
    assert response.status_code == 403


# Testing for when the user is not part of the dm
def test_http_message_unpin_v1_AccessError_dm(set_up_data):
    setup = set_up_data
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']

    m_id = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, "HEY EVERYBODY")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    # user3 who is not a part of dm1 tries to unpin message 
    # - should raise an access error
    response = requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user3, m_id["message_id"]))
    assert response.status_code == 403


# Testing for when the user is not an owner of the channel but is within it
def test_http_message_unpin_v1_AccessError_non_owner(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    requests.post(f"{url}channel/invite/v2", json = channel_invite_body(user1, channel1, user2)).json()

    m_id = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "HEY EVERYBODY")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    # user2 who is not a part of channel1 tries to unpin message 
    # - should raise an access error
    response = requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user2, m_id["message_id"]))
    assert response.status_code == 403


# Testing for when the user is not an owner of the dm but is within it
def test_http_message_unpin_v1_AccessError_dm_non_owner(set_up_data):
    setup = set_up_data
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    m_id = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, "HEY EVERYBODY")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    # user2 who is not an owner of dm1 tries to unpin the message 
    # - should raise an access error
    response = requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user2, m_id["message_id"]))
    assert response.status_code == 403


# Message id is not a real message id
def test_http_message_unpin_v1_InputError_non_valid_id(set_up_data):
    setup = set_up_data
    user1 = setup['user1']
    
    # user1 (the channel owner) tries to unpin a non existent message
    response = requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, 742))
    assert response.status_code == 400


# Message id is already pinned
def test_http_message_unpin_v1_InputError_already_pinned(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    m_id = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "HEY EVERYBODY")).json()

    # user1 (the channel owner) tries to unpin an already unpinned message
    response = requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user1, m_id["message_id"]))
    assert response.status_code == 400


# Default access error when token is invalid
def test_http_message_unpin_v1_default_Access_Error(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    m_id = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Hello")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    assert requests.post(f"{url}message/unpin/v1", json = 
    {
        "token": "invalid token",
        "message_id": m_id["message_id"]
    }).status_code == 403

############################ END EXCEPTION TESTING ############################


############################# TESTING MESSAGE PIN #############################

# Testing to see if one message is pinned correctly
def test_http_message_unpin_v1_pin_one(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    # Send a message to a channel and then pin that message and check that everything is correct
    m_id = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Hello")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    channel_messages = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages['messages']) == 1
    assert channel_messages['messages'][0]['message'] == "Hello"
    assert channel_messages['messages'][0]['is_pinned'] == True
    assert channel_messages['messages'][0]['message_id'] == m_id['message_id']

    # Now unpin the message and check that the message was unpinned correctly
    requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user1, m_id["message_id"]))

    channel_messages_answer = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()
    
    assert len(channel_messages_answer['messages']) == 1
    assert channel_messages_answer['messages'][0]['message'] == "Hello"
    assert channel_messages_answer['messages'][0]['is_pinned'] == False
    assert channel_messages_answer['messages'][0]['message_id'] == m_id['message_id']


# Testing to see if multiple messages are unpinned correctly
def test_http_message_unpin_v1_pin_multiple(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    requests.post(f"{url}channel/invite/v2", json = channel_invite_body(user1, channel1, user2)).json()

    # Send 1 message and then pin it
    m_id1 = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Hello")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id1["message_id"])).json()

    # Send 20 messages after the pinned message
    send_x_messages(user1, user2, channel1, 20)

    # Now send 2 more messages and pin the first of the two that was sent. Check that
    # everything is working as intended
    m_id2 = requests.post(f"{url}message/send/v2", json=message_send_body(user2, channel1, "Bao")).json()
    m_id3 = requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Bye")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id2["message_id"])).json()

    # Unpin the very first pinned msg and check that everything is working correctly
    requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user1, m_id1["message_id"]))

    channel_messages = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages['messages']) == 23
    assert channel_messages['messages'][22]['message'] == "Hello"
    assert channel_messages['messages'][22]['is_pinned'] == False
    assert channel_messages['messages'][22]['message_id'] == m_id1['message_id']
    
    assert channel_messages['messages'][1]['message'] == "Bao"
    assert channel_messages['messages'][1]['is_pinned'] == True
    assert channel_messages['messages'][1]['message_id'] == m_id2['message_id']
    assert channel_messages['messages'][1]['u_id'] == user2["auth_user_id"]

    assert channel_messages['messages'][2]['message'] == "20"
    assert channel_messages['messages'][2]['is_pinned'] == False

    assert channel_messages['messages'][0]['message'] == "Bye"
    assert channel_messages['messages'][0]['is_pinned'] == False
    assert channel_messages['messages'][0]['message_id'] == m_id3['message_id']


    # Unpin the second pinned message and check that everything is working as intended
    requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user1, m_id2["message_id"]))

    channel_messages_ans = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages_ans['messages']) == 23
    assert channel_messages_ans['messages'][22]['message'] == "Hello"
    
    # Make sure every message in the channel is unpinned
    for i in range(23):
        assert channel_messages_ans['messages'][i]['is_pinned'] == False


# Testing to see if one message is pinned correctly to a dm
def test_http_message_unpin_v1_pin_one_dm(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']

    # Send a message to a dm and then pin that message and check that everything is correct
    m_id = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, "Hello")).json()
    requests.post(f"{url}message/pin/v1", json=message_pin_body(user1, m_id["message_id"])).json()

    dm_messages = requests.get(f"{url}dm/messages/v1",\
                    params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages['messages']) == 1
    assert dm_messages['messages'][0]['message'] == "Hello"
    assert dm_messages['messages'][0]['is_pinned'] == True
    assert dm_messages['messages'][0]['message_id'] == m_id['message_id']

    # Unpin the pinned message and check that the message was unpinned correctly
    requests.post(f"{url}message/unpin/v1", json=message_unpin_body(user1, m_id["message_id"]))

    dm_messages_ans = requests.get(f"{url}dm/messages/v1",\
                    params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages_ans['messages']) == 1
    assert dm_messages_ans['messages'][0]['message'] == "Hello"
    assert dm_messages_ans['messages'][0]['is_pinned'] == False
    assert dm_messages_ans['messages'][0]['message_id'] == m_id['message_id']


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

def user_body(num):
    return {
        "email": f"example{num}@hotmail.com",
        "password": f"password{num}",
        "name_first": f"first_name{num}",
        "name_last": f"last_name{num}"
    }

def channels_create_body(user, name):
    return {
        "token": user["token"],
        "name": name,
        "is_public": True
    }

def message_send_body(user, channel_id, message):
    return {
        "token": user["token"],
        "channel_id": channel_id,
        "message": message
    }

def message_senddm_body(user, dm, message): 
    return {
        "token": user["token"],
        "dm_id": dm,
        "message": message
    }

def message_pin_body(user, message_id): 
    return {
        "token": user["token"],
        "message_id": message_id
    }

def message_unpin_body(user, message_id): 
    return {
        "token": user["token"],
        "message_id": message_id
    }

def channel_messages_body(user, channel_id, start):
    return {
        "token": user["token"],
        "channel_id": channel_id,
        "start": start
    }

def dm_messages_body(user, dm_id, start):
    return {
        "token": user["token"],
        "dm_id": dm_id,
        "start": start
    }

def channel_invite_body(user, channel_id, user_id):
    return {
        "token": user["token"],
        "channel_id": channel_id,
        "u_id": user_id["auth_user_id"]
    }

# Helper function to send x messages from 2 users to a channel
def send_x_messages(user1, user2, channel1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, str(message_num))).json()
        else:
            requests.post(f"{url}message/send/v2", json=message_send_body(user2, channel1, str(message_num))).json()
        message_count += 1
    
    return {}
