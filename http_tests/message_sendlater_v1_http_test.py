# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import json
import requests
import urllib

from src.config import url

from datetime import datetime
import time


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the channel (testing Access Error)
def test_http_message_sendlater_v1_AccessError(set_up_data):
    setup = set_up_data
    user2, channel1 = setup['user2'], setup['channel1']

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # user2 who is not a part of channel_1 tries to send message 
    # - should raise an access error
    response = requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user2, channel1, "Hello", send_time))
    assert response.status_code == 403


# Testing to see if message is of valid length
def test_http_message_sendlater_v1_InputError(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    response = requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user1, channel1, long_message, send_time))
    assert response.status_code == 400


# Test input error when channel_id is not a valid channel
def test_http_message_sendlater_v1_InputError_invalid_channel(set_up_data):
    setup = set_up_data
    user1 = setup['user1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    # user1 tries to send a message that is too long to channel 1
    response = requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user1, 123321, "Hello", send_time))
    assert response.status_code == 400


# Test input error when time _sent is in the past
def test_http_message_sendlater_v1_InputError_invalid_time(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time - 10

    # user1 tries to send a message to the past
    response = requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user1, channel1, "Hello", send_time))
    assert response.status_code == 400


# Default access error when token is invalid
def test_http_message_sendlater_v1_default_Access_Error():

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    response = requests.post(f"{url}message/sendlater/v1", json={
        "token": "inval",
        "channel_id": "channel",
        "message": "wrong",
        "time_sent": send_time
    })
    assert response.status_code == 403

############################ END EXCEPTION TESTING ############################


######################### TESTING MESSAGE SEND LATER ##########################

# Testing 1 message being sent in the future
def test_http_message_send_later_v1_1_message(set_up_data):
    setup = set_up_data
    user1, channel1 = setup['user1'], setup['channel1']

    channel_messages = requests.get(f"{url}channel/messages/v2",\
                        params=channel_messages_body(user1, channel1, 0)).json()

    # Assert that there are no messages within the channel
    assert len(channel_messages['messages']) == 0

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user1, channel1, "Hello", send_time)).json()

    channel_messages1 = requests.get(f"{url}channel/messages/v2",\
                        params=channel_messages_body(user1, channel1, 0)).json()

    # 1 second hasn't passed yet, so the number of messages should still be 0
    assert len(channel_messages1['messages']) == 0

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)

    channel_messages_ans = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages_ans['messages']) == 1
    assert channel_messages_ans['messages'][0]['message'] == "Hello"
    assert channel_messages_ans['messages'][0]['u_id'] == user1['auth_user_id']


# Testing one message being sent later and then sending multiple afterwards
def test_http_message_send_later_v1_send_multiple_after(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(user1, channel1, user2)).json()
    
    # Assert that there are no messages within the channel
    channel_messages = requests.get(f"{url}channel/messages/v2",\
                    params=channel_messages_body(user1, channel1, 0)).json()
    assert len(channel_messages['messages']) == 0

    # Delay 1 message by 1 second
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user1, channel1, "Hello", send_time)).json()

    send_x_messages(user1, user2, channel1, 20)
    # 1 second hasn't passed yet, so the number of messages should just be 20
    channel_msgs = requests.get(f"{url}channel/messages/v2",\
                    params=channel_messages_body(user1, channel1, 0)).json()
    assert len(channel_msgs['messages']) == 20

    # Put the current test to sleep for 1.5 seconds, send another message and
    # then check that message send later worked properly
    time.sleep(1.5)
    requests.post(f"{url}message/send/v2", json=message_send_body(user2, channel1, "Bye!")).json()

    channel_messages_ans = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages_ans['messages']) == 22
    assert channel_messages_ans['messages'][1]['message'] == "Hello"
    assert channel_messages_ans['messages'][1]['u_id'] == user1['auth_user_id']
    assert channel_messages_ans['messages'][0]['message'] == "Bye!"
    assert channel_messages_ans['messages'][0]['u_id'] == user2['auth_user_id']


# Testing user2 sending a message later and then leaving the channel before
# the message is sent
def test_http_message_send_later_v1_leave_channel_before_message_sent(set_up_data):
    setup = set_up_data
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(user1, channel1, user2)).json()

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Hi!")).json()

    requests.post(f"{url}message/sendlater/v1", json=message_sendlater_body(user2, channel1, "I'm leaving.", send_time)).json()

    requests.post(f"{url}channel/leave/v1", json=channel_leave_body(user2, channel1)).json()
    
    requests.post(f"{url}message/send/v2", json=message_send_body(user1, channel1, "Nice to meet you")).json()

    channel_messages = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages['messages']) == 2
    assert channel_messages['messages'][0]['message'] == "Nice to meet you"
    assert channel_messages['messages'][1]['message'] == "Hi!"

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)

    channel_messages_ans = requests.get(f"{url}channel/messages/v2",\
                            params=channel_messages_body(user1, channel1, 0)).json()

    assert len(channel_messages_ans['messages']) == 3
    assert channel_messages_ans['messages'][0]['message'] == "I'm leaving."
    assert channel_messages_ans['messages'][0]['u_id'] == user2['auth_user_id']


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

def message_sendlater_body(user, channel, message, time): 
    return {
        "token": user["token"],
        "channel_id": channel,
        "message": message,
        "time_sent": time
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

def channel_messages_body(user, channel_id, start):
    return {
        "token": user["token"],
        "channel_id": channel_id,
        "start": start
}

def channel_invite_body(user, channel_id, user_id):
    return {
        "token": user["token"],
        "channel_id": channel_id,
        "u_id": user_id["auth_user_id"]
}

def channel_leave_body(user, channel_id):
    return {
        "token": user["token"],
        "channel_id": channel_id
}


# Helper function to send x messages from 2 users to a dm
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
