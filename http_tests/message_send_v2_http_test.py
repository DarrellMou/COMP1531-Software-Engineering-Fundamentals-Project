import json
import requests
import pytest
from src.data import retrieve_data
from src.auth import auth_decode_token
from src.config import url


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

def set_up_data():
    requests.delete(f"{url}clear/v1")
    r = requests.post(f"{url}auth/register/v2", json = {
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    })
    user1 = r.json()

    r = requests.post(f"{url}auth/register/v2", json = {
        "email": "shaun.sheep@email.com",
        "password": "password123",
        "name_first": "Shaun",
        "name_last": "Sheep"
    })
    user2 = r.json()

    r = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel1",
        "is_public": True
    })
    channel1 = r.json()

    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1["channel_id"]
    }

    return setup


def send_x_messages(user1, user2, channel1, num_messages):

    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            requests.post(f"{url}message/send/v2", json= {
                "token": user1["token"],
                "channel_id": channel1,
                "message": str(message_num)
            }).json()
        else:
            requests.post(f"{url}message/send/v2", json= {
                "token": user2["token"],
                "channel_id": channel1,
                "message": str(message_num)
            }).json()
        message_count += 1

    return {}

def send_x_messages_two_channels(user, channel1, channel2, num_messages):
    
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        requests.post(f"{url}message/send/v2", json= {
            "token": user["token"],
            "channel_id": channel1,
            "message": str(message_num)
        }).json()
        requests.post(f"{url}message/send/v2", json= {
            "token": user["token"],
            "channel_id": channel2,
            "message": str(message_num)
        }).json()
        message_count += 1

    return {}



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################
def test_http_message_send_v2_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']


    # Ensure AccessError
    assert requests.post(url + 'message/send/v2', json={
        'token': user2["token"],
        'channel_id': channel1,
        'message': "Hello",
    }).status_code == 403



# Testing to see if message is of valid length
def test_http_message_send_v2_InputError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    assert requests.post(url + 'message/send/v2', json={
        'token': user1["token"],
        'channel_id': channel1,
        'message': long_message,
    }).status_code == 400


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SEND #############################

# Testing for 1 message being sent by user1
def test_http_message_send_v2_send_one():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    message_one = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    channel_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages["messages"][0]["message_id"] == message_one["message_id"]



# Testing for 2 identical messages being sent by user1
def test_http_message_send_v2_user_sends_identical_messages():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    first_message_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    second_message_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    channel_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert first_message_id["message_id"] == channel_messages["messages"][1]["message_id"]
    assert second_message_id["message_id"] == channel_messages["messages"][0]["message_id"]

    assert first_message_id != second_message_id


# Testing for multiple messages with 2 users and that the correct messages are
# being sent
def test_http_message_send_v2_multiple_users_multiple_messages():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel1,
        "u_id": user2["auth_user_id"]
    }).json()

    send_x_messages(user1, user2, channel1, 10)

    channel_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages["messages"][0]["message"] == "10"
    assert channel_messages["messages"][5]["message"] == "5"
    assert channel_messages["messages"][9]["message"] == "1"


# Testing for multiple messages with 2 users and that the correct message_ids
# are being returned by message_send
def test_http_message_send_v2_multiple_users_multiple_messages_message_id():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel1,
        "u_id": user2["auth_user_id"]
    }).json()


    message_count = 0
    while message_count < 50:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_id = requests.post(f"{url}message/send/v2", json= {
                "token": user1["token"],
                "channel_id": channel1,
                "message": str(message_num)
            }).json()
        else:
            message_id = requests.post(f"{url}message/send/v2", json= {
                "token": user2["token"],
                "channel_id": channel1,
                "message": str(message_num)
            }).json()
        channel_messages = requests.get(f"{url}channel/messages/v2", json= {
            "token": user1["token"],
            "channel_id": channel1,
            "start": 0
        }).json()

        reversed_channel_messages = channel_messages["messages"][::-1]
        assert message_id["message_id"] == reversed_channel_messages[message_count]["message_id"]
        message_count += 1


# Same user sends the identical message to two different channels
# Message ids should be different
def test_http_message_send_v2_identical_message_to_2_channels():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel2",
        "is_public": True
    }).json()


    send_x_messages_two_channels(user1, channel1, channel2["channel_id"], 10)

    channel1_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "start": 0
    }).json()

    m_id0_ch1 = channel1_messages["messages"][0]["message_id"]
    m_id0_ch2 = channel2_messages["messages"][0]["message_id"]
    m_id5_ch1 = channel1_messages["messages"][5]["message_id"]
    m_id5_ch2 = channel2_messages["messages"][5]["message_id"]
    m_id9_ch1 = channel1_messages["messages"][9]["message_id"]
    m_id9_ch2 = channel2_messages["messages"][9]["message_id"]

    assert m_id0_ch1 != m_id0_ch2
    assert m_id5_ch1 != m_id5_ch2
    assert m_id9_ch1 != m_id9_ch2


# Test if message_send also appends message to the data['messages'] list
def test_http_message_send_v2_appends_to_data_messages():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel2",
        "is_public": True
    }).json()
    
    send_x_messages_two_channels(user1, channel1, channel2["channel_id"], 10)
    
    channel1_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "start": 0
    }).json()

    assert len(channel1_messages['messages']) + len(channel2_messages['messages']) == 20

'''
# Test if data['messages'] list is in order
def test_http_message_send_v2_data_messages_in_order():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    channel2 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel2",
        "is_public": True
    }).json()

    send_x_messages_two_channels(user1, channel1, channel2["channel_id"], 10)
    
    channel1_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()


    channel2_messages = requests.get(f"{url}channel/messages/v2", json= {
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "start": 0
    }).json()

    m_id0_ch1 = channel1_messages['messages'][0]
    m_id0_ch2 = channel2_messages['messages'][0]
    m_id5_ch1 = channel1_messages['messages'][5]
    m_id5_ch2 = channel2_messages['messages'][5]
    m_id9_ch1 = channel1_messages['messages'][9]
    m_id9_ch2 = channel2_messages['messages'][9]

    data = retrieve_data()

    assert data['messages'][0]['message_id'] == m_id9_ch1['message_id']
    assert data['messages'][0]['message'] == m_id9_ch1['message']
'''