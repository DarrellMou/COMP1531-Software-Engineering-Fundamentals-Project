import json
import requests
import urllib
import src.server
from src.message import message_send
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.channel import channel_invite_v1


BASE_URL = 'http://127.0.0.1:8080/'


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

def set_up_data():
    requests.delete(f"{BASE_URL}clear/v1/")
    r = requests.post(f"{BASE_URL}auth/register/v2", json = {
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    })
    user1 = r.json()

    r = requests.post(f"{BASE_URL}auth/register/v2", json = {
        "email": "shaun.sheep@email.com",
        "password": "password123",
        "name_first": "Shaun",
        "name_last": "Sheep"
    })
    user2 = r.json()

    r = requests.post(f"{BASE_URL}channels/create/v2", json = {
        "auth_user_id": user1['auth_user_id'],
        "name": "Channel1",
        "is_public": True
    })
    channel1 = r.json()

    setup = {
        "user1": user1["token"],
        "user2": user2["token"],
        "channel1": channel1["channel_id"]
    }

    return setup


def send_x_messages(user1, user2, channel1, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_send_v2(user1, channel1, str(message_num))
        else:
            message_send_v2(user2, channel1, str(message_num))
        message_count += 1
    
    return data

def send_x_messages_two_channels(user, channel1, channel2, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_send_v2(user, channel1, str(message_num))
        message_send_v2(user, channel2, str(message_num))
        message_count += 1
    return data



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################
def test_http_message_send_v2_AccessError():
