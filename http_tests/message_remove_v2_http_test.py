import json
import requests
import pytest
from src.data import retrieve_data
from src.auth import auth_decode_token
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
        "channel_id": channel1,
        "u_id": user2["auth_user_id"]
    }).json()

    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1["channel_id"]
    }

    return setup


