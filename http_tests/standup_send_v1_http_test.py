# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import json
import requests
import urllib

from datetime import datetime
import time

from src.config import url

###                         HELPER FUNCTIONS                           ###

def channels_create_body(user, name, is_public): 
    return {
        "token": user["token"],
        "name": name,
        "is_public": is_public
    }

def standup_start_body(user, channel, length):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"],
        "length": length
    }

def standup_send_body(user, channel, message):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"],
        "message": message
    }

def channel_messages_body(user, channel, start):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"],
        "start": start
    }

def channel_invite_body(user1, channel, user2):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"],
        "u_id": user2["auth_user_id"]
    }

###                       END HELPER FUNCTIONS                         ###

def test_function(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Testmessage"))

    time.sleep(2)

    message_list = requests.get(f"{url}channel/messages/v2", params=channel_messages_body(user[0], channel0, 0))

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == "user0_firstuser0_las: Test message"

def test_multiple_messages(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Testmessage1"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Testmessage2"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Testmessage3"))

    time.sleep(2)

    message_list = requests.get(f"{url}channel/messages/v2", params=channel_messages_body(user[0], channel0, 0))

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == '''user0_firstuser0_las: Test message1
user0_firstuser0_las: Test message2
user0_firstuser0_las: Test message3'''

def test_multiple_messages_from_multiple_users(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[1]))
    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[2]))
    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[3]))
    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[4]))

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Testmessage0"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[1], channel0, "Testmessage1"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[2], channel0, "Testmessage2"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[3], channel0, "Testmessage3"))
    requests.post(f"{url}standup/send/v1", json=standup_send_body(users[4], channel0, "Testmessage4"))

    time.sleep(2)

    message_list = requests.get(f"{url}channel/messages/v2", params=channel_messages_body(user[0], channel0, 0))

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == '''user0_firstuser0_las: Test message0
user1_firstuser1_las: Test message1
user2_firstuser2_las: Test message2
user3_firstuser3_las: Test message3
user4_firstuser4_las: Test message4'''

def test_invalid_channel_id(users):
    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], {"channel_id" : 12345}, "Testmessage0"))
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }

def test_too_long_message(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, long_message))
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }
    time.sleep(2)

def test_inactive_standup(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body(users[0], channel0, "Test message"))
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }

def test_unauthorized_user(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body(users[1], channel0, "Test message"))
    assert standup_response == {
        "code" : 403,
        "name" : "System Error",
        "message" : "<p></p>"
    }
    time.sleep(2)

def test_invalid_token(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))

    standup_response = requests.post(f"{url}standup/send/v1", json=standup_send_body({"token" : 12345}, channel0, "Test message"))
    assert standup_response == {
        "code" : 403,
        "name" : "System Error",
        "message" : "<p></p>"
    }
    time.sleep(2)
