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

# Testing for when the user is not part of the dm (testing Access Error)
def test_http_message_sendlaterdm_v1_AccessError(set_up_data):
    setup = set_up_data
    user3, dm1 = setup['user3'], setup['dm1']

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # user3 who is not a part of dm_1 tries to send message 
    # - should raise an access error
    response = requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user3, dm1, "Hello", send_time))
    assert response.status_code == 403


# Testing to see if message is of valid length
def test_http_message_sendlaterdm_v1_InputError(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to md 1
    response = requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user1, dm1, long_message, send_time))
    assert response.status_code == 400


# Test input error when dm_id is not a valid dm
def test_http_message_sendlaterdm_v1_InputError_invalid_dm(set_up_data):
    setup = set_up_data
    user1 = setup['user1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    # user1 tries to send a message that is too long to dm 1
    response = requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user1, 123321, "Hello", send_time))
    assert response.status_code == 400


# Test input error when time _sent is in the past
def test_http_message_sendlaterdm_v1_InputError_invalid_time(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']
    
    current_time = round(datetime.now().timestamp())
    send_time = current_time - 10

    # user1 tries to send a message to the past
    response = requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user1, dm1, "Hello", send_time))
    assert response.status_code == 400


# Default access error when token is invalid
def test_http_message_sendlaterdm_v1_default_Access_Error():

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    response = requests.post(f"{url}message/sendlaterdm/v1", json={
        "token": "inval",
        "dm_id": "dm",
        "message": "wrong",
        "time_sent": send_time
    })
    assert response.status_code == 403

############################ END EXCEPTION TESTING ############################


######################### TESTING MESSAGE SEND LATER ##########################

# Testing 1 message being sent in the future
def test_http_message_sendlaterdm_v1_1_message(set_up_data):
    setup = set_up_data
    user1, dm1 = setup['user1'], setup['dm1']

    dm_messages = requests.get(f"{url}dm/messages/v1",\
                        params=dm_messages_body(user1, dm1, 0)).json()

    # Assert that there are no messages within the dm
    assert len(dm_messages['messages']) == 0

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user1, dm1, "Hello", send_time)).json()

    dm_messages1 = requests.get(f"{url}dm/messages/v1",\
                        params=dm_messages_body(user1, dm1, 0)).json()

    # 1 second hasn't passed yet, so the number of messages should still be 0
    assert len(dm_messages1['messages']) == 0

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)

    dm_messages_ans = requests.get(f"{url}dm/messages/v1",\
                            params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages_ans['messages']) == 1
    assert dm_messages_ans['messages'][0]['message'] == "Hello"
    assert dm_messages_ans['messages'][0]['u_id'] == user1['auth_user_id']


# Testing one message being sent later and then sending multiple afterwards
def test_http_message_sendlaterdm_v1_send_multiple_after(set_up_data):
    setup = set_up_data
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    requests.post(f"{url}dm/invite/v1", json=dm_invite_body(user1, dm1, user3)).json()
    
    # Assert that there are no messages within the dm
    dm_messages = requests.get(f"{url}dm/messages/v1",\
                    params=dm_messages_body(user1, dm1, 0)).json()
    assert len(dm_messages['messages']) == 0

    # Delay 1 message by 1 second
    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1
    requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user1, dm1, "Hello", send_time)).json()

    send_x_messages(user1, user3, dm1, 20)
    # 1 second hasn't passed yet, so the number of messages should just be 20
    dm_msgs = requests.get(f"{url}dm/messages/v1",\
                    params=dm_messages_body(user1, dm1, 0)).json()
    assert len(dm_msgs['messages']) == 20

    # Put the current test to sleep for 1.5 seconds, send another message and
    # then check that message send later worked properly
    time.sleep(1.5)
    requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user3, dm1, "Bye!")).json()

    dm_messages_ans = requests.get(f"{url}dm/messages/v1",\
                            params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages_ans['messages']) == 22
    assert dm_messages_ans['messages'][1]['message'] == "Hello"
    assert dm_messages_ans['messages'][1]['u_id'] == user1['auth_user_id']
    assert dm_messages_ans['messages'][0]['message'] == "Bye!"
    assert dm_messages_ans['messages'][0]['u_id'] == user3['auth_user_id']


# Testing user3 sending a message later and then leaving the dm before
# the message is sent
def test_http_message_sendlaterdm_v1_leave_dm_before_message_sent(set_up_data):
    setup = set_up_data
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    requests.post(f"{url}dm/invite/v1", json=dm_invite_body(user1, dm1, user3)).json()

    current_time = round(datetime.now().timestamp())
    send_time = current_time + 1

    requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, "Hi!")).json()

    requests.post(f"{url}message/sendlaterdm/v1", json=message_sendlaterdm_body(user3, dm1, "I'm leaving.", send_time)).json()

    requests.post(f"{url}dm/leave/v1", json=dm_leave_body(user3, dm1)).json()
    
    requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, "Nice to meet you")).json()

    dm_messages = requests.get(f"{url}dm/messages/v1",\
                            params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages['messages']) == 2
    assert dm_messages['messages'][0]['message'] == "Nice to meet you"
    assert dm_messages['messages'][1]['message'] == "Hi!"

    # Put the current test to sleep for 1.5 seconds and then check that the message was
    # correctly sent
    time.sleep(1.5)

    dm_messages_ans = requests.get(f"{url}dm/messages/v1",\
                            params=dm_messages_body(user1, dm1, 0)).json()

    assert len(dm_messages_ans['messages']) == 3
    assert dm_messages_ans['messages'][0]['message'] == "I'm leaving."
    assert dm_messages_ans['messages'][0]['u_id'] == user3['auth_user_id']


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

def message_sendlaterdm_body(user, dm, message, time): 
    return {
        "token": user["token"],
        "dm_id": dm,
        "message": message,
        "time_sent": time
    }

def dm_create_body(user, u_ids):
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        "token": user["token"],
        "u_ids": u_ids_list
    }

def message_senddm_body(user, dm_id, message):
    return {
        "token": user["token"],
        "dm_id": dm_id,
        "message": message
    }

def dm_messages_body(user, dm_id, start):
    return {
        "token": user["token"],
        "dm_id": dm_id,
        "start": start
}

def dm_invite_body(user, dm_id, user_id):
    return {
        "token": user["token"],
        "dm_id": dm_id,
        "u_id": user_id["auth_user_id"]
}

def dm_leave_body(user, dm_id):
    return {
        "token": user["token"],
        "dm_id": dm_id
}


# Helper function to send x messages from 2 users to a dm
def send_x_messages(user1, user2, dm1, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm1, str(message_num))).json()
        else:
            requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user2, dm1, str(message_num))).json()
        message_count += 1
    
    return {}
