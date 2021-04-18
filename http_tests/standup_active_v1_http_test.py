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

def standup_active_body(user, channel):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"]
    }

###                       END HELPER FUNCTIONS                         ###

def test_function(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1)).json()

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == int(datetime.now().timestamp() + 1)
    assert standup_response['is_active'] == True
    time.sleep(2)

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == None
    assert standup_response['is_active'] == False

def test_multiple_runs(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 1)).json()
    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == int(datetime.now().timestamp() + 1)
    assert standup_response['is_active'] == True
    time.sleep(2)

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == None
    assert standup_response['is_active'] == False

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 3)).json()
    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == int(datetime.now().timestamp() + 3)
    assert standup_response['is_active'] == True
    time.sleep(4)

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == None
    assert standup_response['is_active'] == False

    requests.post(f"{url}standup/start/v1", json=standup_start_body(users[0], channel0, 5)).json()
    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == int(datetime.now().timestamp() + 5)
    assert standup_response['is_active'] == True
    time.sleep(6)

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], channel0)).json()

    assert standup_response['time_finish'] == None
    assert standup_response['is_active'] == False

def test_invalid_channel_id(users):
    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body(users[0], {"channel_id": 12345})).json()
    assert standup_response == {
        "code" : 400,
        "name" : "System Error",
        "message" : "<p></p>"
    }

def test_invalid_token(users):
    channel_id0 = requests.post(f"{url}channels/create/v2", json=channels_create_body(users[0], "Channel0", True))
    channel0 = channel_id0.json()

    standup_response = requests.get(f"{url}standup/active/v1", params=standup_active_body({"token" : 12345}, channel0)).json()
    assert standup_response == {
        "code" : 403,
        "name" : "System Error",
        "message" : "<p></p>"
    }