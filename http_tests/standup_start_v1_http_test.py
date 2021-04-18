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

###                       END HELPER FUNCTIONS                         ###

def test_function(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1)).json()

    assert standup_response['time_finish'] == int(datetime.now().timestamp() + 1)
    time.sleep(2)

def test_multiple_runs(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response1 = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1)).json()
    assert standup_response1['time_finish'] == int(datetime.now().timestamp() + 1)
    time.sleep(2)

    standup_response2 = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 3)).json()
    assert standup_response2['time_finish'] == int(datetime.now().timestamp() + 3)
    time.sleep(4)

    standup_response3 = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 5)).json()
    assert standup_response3['time_finish'] == int(datetime.now().timestamp() + 5)
    time.sleep(6)

def test_invalid_channel_id(users):
    standup_response = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], {"channel_id": 12345}, 1)).json()
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }

def test_active_standup(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1))
    
    standup_response = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1)).json()
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }
    time.sleep(2)

def test_unauthorized_user(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response = requests.post(f"{url}standup/start/v1", json=standup_start_body(users[1], channel0, 1)).json()
    assert standup_response == {
        "code" : 403,
        "name" : "System Error",
        "message" : "<p></p>"
    }

def test_invalid_token(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response = requests.post(f"{url}standup/start/v1", json=standup_start_body({"token" : 12345}, channel0, 1)).json()
    assert standup_response == {
        "code" : 403,
        "name" : "System Error",
        "message" : "<p></p>"
    }
