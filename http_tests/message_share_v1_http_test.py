import json
import requests
import pytest
from src.config import url


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Sharing a message will add a new message to the data['messages'] list and to
# the channel's or dm's messages list

# The way messages are shared in the http://Dreams-unsw.herokuapp.com/ app is
# the correct way of sharing messages

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

    channel2 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel2",
        "is_public": True
    }).json()

    requests.post(f"{url}channel/invite/v2", json = {
        "token": user1["token"],
        "channel_id": channel2["channel_id"],
        "u_id": user2["auth_user_id"]
    }).json()

    dm1 = requests.post(f"{url}dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [user2["auth_user_id"]]
    }).json()

    dm2 = requests.post(f"{url}dm/create/v1", json = {
        "token": user2["token"],
        "u_ids": [user1["auth_user_id"]]
    }).json()

    setup = {
        "user1": user1,
        "user2": user2,
        "channel1": channel1["channel_id"],
        "channel2": channel2["channel_id"],
        "dm1": dm1["dm_id"],
        "dm2": dm2["dm_id"]
    }

    return setup

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if the user who is sharing the message to a channel/dm is
# actually in that channel/dm
def test_http_message_share_v1_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    
    m_id = msg["message_id"]

    channel3 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel3",
        "is_public": True
    }).json()


    assert requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Optional Message",
        "channel_id": channel3["channel_id"],
        "dm_id": -1
    }).status_code == 403


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SHARE ############################

# Testing user1 sharing one message to channel
def test_http_message_share_v1_share_one_to_channel():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()

    m_id = msg["message_id"]

    shared_msg = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Shared Message 1",
        "channel_id": channel2,
        "dm_id": -1
    }).json()
    shared_m_id = shared_msg["shared_message_id"]

    channel1_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel2,
        "start": 0
    }).json()

    assert channel1_messages["messages"][0]["message_id"] == m_id
    assert channel1_messages["messages"][0]["message"] == "Hello"
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id
    assert channel2_messages["messages"][0]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert len(channel1_messages["messages"]) == 1
    assert len(channel2_messages["messages"]) == 1



# Sharing and resharing the message a few times to differing channels
def test_http_message_share_v1_share_one_multiple_times():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Shared Message 1",
        "channel_id": channel2,
        "dm_id": -1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "Shared Message 2",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Shared Message 3",
        "channel_id": channel2,
        "dm_id": -1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]

    channel1_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel2,
        "start": 0
    }).json()

    assert channel1_messages["messages"][1]["message_id"] == m_id
    assert channel1_messages["messages"][1]["message"] == "Hello"
    assert channel2_messages["messages"][1]["message_id"] == shared_m_id1
    assert channel2_messages["messages"][1]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel2_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n    \n    """\n    Shared Message 1\n        \n        """\n        Hello\n        """\n    """\n"""'

    assert len(channel2_messages["messages"]) == 2
    assert len(channel1_messages["messages"]) == 2



# Sharing to the same channel
def test_http_message_share_v1_share_one_multiple_times_same_channel():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Shared Message 1",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "Shared Message 2",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Shared Message 3",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]
    
    channel_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    assert channel_messages["messages"][3]["message_id"] == m_id
    assert channel_messages["messages"][3]["message"] == "Hello"
    assert channel_messages["messages"][2]["message_id"] == shared_m_id1
    assert channel_messages["messages"][2]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert channel_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n    \n    """\n    Shared Message 1\n        \n        """\n        Hello\n        """\n    """\n"""'
    assert len(channel_messages["messages"]) == 4


# There is no additional message that is attached to the og message
# This follows the way it is shared at http://Dreams-unsw.herokuapp.com/ when
# no optional message is added to the shared message
def test_http_message_share_v1_share_with_no_added_msg():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "",
        "channel_id": channel2,
        "dm_id": -1
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Hi",
        "channel_id": channel1,
        "dm_id": -1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]

    channel1_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    channel2_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel2,
        "start": 0
    }).json()

    assert channel1_messages["messages"][2]["message_id"] == m_id
    assert channel1_messages["messages"][2]["message"] == "Hello"
    assert channel1_messages["messages"][1]["message_id"] == shared_m_id1
    assert channel1_messages["messages"][1]["message"] == '\n\n"""\nHello\n"""'
    assert channel1_messages["messages"][0]["message_id"] == shared_m_id3
    assert channel1_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n    \n    """\n    \n        \n        """\n        Hello\n        """\n    """\n"""'
    assert len(channel1_messages["messages"]) == 3
    assert channel2_messages["messages"][0]["message_id"] == shared_m_id2
    assert channel2_messages["messages"][0]["message"] == '\n\n"""\n\n    \n    """\n    Hello\n    """\n"""'
    assert len(channel2_messages["messages"]) == 1


# Testing user1 sharing one message from channel to dm
def test_http_message_share_v1_share_from_channel_to_dm():
    setup = set_up_data()
    user1, user2, channel1, dm1 = setup['user1'], setup['user2'], setup['channel1'], setup['dm1']
    msg = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Shared Message 1",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    channel_messages = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1,
        "start": 0
    }).json()

    dm_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    assert channel_messages["messages"][0]["message_id"] == m_id
    assert channel_messages["messages"][0]["message"] == "Hello"
    assert channel_messages["messages"][0]["time_created"] <= dm_messages["messages"][0]["time_created"]
    assert len(channel_messages["messages"]) == 1
    assert dm_messages["messages"][0]["message_id"] == shared_m_id1
    assert dm_messages["messages"][0]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert len(dm_messages["messages"]) == 1


# Sharing and resharing the message a few times to differing dms. Message is
# originally sent to a dm
def test_http_message_share_v1_share_dm_multiple_times():
    setup = set_up_data()
    user1, user2, dm1, dm2 = setup['user1'], setup['user2'], setup['dm1'], setup['dm2']
    msg = requests.post(f"{url}message/senddm/v1", json= {
        "token": user1["token"],
        "dm_id": dm1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "Shared Message 1",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "Shared Message 2",
        "channel_id": -1,
        "dm_id": dm2
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Shared Message 3",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]

    dm1_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    
    dm2_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm2,
        "start": 0
    }).json()

    assert dm1_messages["messages"][2]["message_id"] == m_id
    assert dm1_messages["messages"][2]["message"] == "Hello"
    assert dm1_messages["messages"][1]["message_id"] == shared_m_id1
    assert dm1_messages["messages"][1]["message"] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert dm1_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm1_messages["messages"][0]["message"] == 'Shared Message 3\n\n"""\nShared Message 2\n    \n    """\n    Shared Message 1\n        \n        """\n        Hello\n        """\n    """\n"""'
    assert len(dm1_messages["messages"]) == 3

    assert dm2_messages["messages"][0]["message_id"] == shared_m_id2
    assert dm2_messages["messages"][0]["message"] == 'Shared Message 2\n\n"""\nShared Message 1\n    \n    """\n    Hello\n    """\n"""'
    assert len(dm2_messages["messages"]) == 1

# There is no additional message that is attached to the og message which was
# sent from dm
def test_http_message_share_v1_share_dm_with_no_added_msg():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    msg = requests.post(f"{url}message/senddm/v1", json= {
        "token": user1["token"],
        "dm_id": dm1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "",
        "channel_id": -1,
        "dm_id": dm1,
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Hi",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]

    dm_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()
    assert dm_messages["messages"][3]["message_id"] == m_id
    assert dm_messages["messages"][3]["message"] == "Hello"
    assert dm_messages["messages"][2]["message_id"] == shared_m_id1
    assert dm_messages["messages"][2]["message"] == '\n\n"""\nHello\n"""'
    assert dm_messages["messages"][1]["message_id"] == shared_m_id2
    assert dm_messages["messages"][1]["message"] == '\n\n"""\n\n    \n    """\n    Hello\n    """\n"""'
    assert dm_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n    \n    """\n    \n        \n        """\n        Hello\n        """\n    """\n"""'
    assert len(dm_messages["messages"]) == 4


# There is no additional message that is attached to the og message which was
# sent from dm - this time shared between multiple dms
def test_http_message_share_v1_share_dm_with_no_added_msg_2_dms():
    setup = set_up_data()
    user1, user2, dm1, dm2 = setup['user1'], setup['user2'], setup['dm1'], setup['dm2']
    msg = requests.post(f"{url}message/senddm/v1", json= {
        "token": user1["token"],
        "dm_id": dm1,
        "message": "Hello"
    }).json()
    m_id = msg["message_id"]

    shared_msg1 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": m_id,
        "message": "",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id1 = shared_msg1["shared_message_id"]

    shared_msg2 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id1,
        "message": "",
        "channel_id": -1,
        "dm_id": dm2,
    }).json()
    shared_m_id2 = shared_msg2["shared_message_id"]

    shared_msg3 = requests.post(f"{url}message/share/v1", json={
        "token": user2["token"],
        "og_message_id": shared_m_id2,
        "message": "Hi",
        "channel_id": -1,
        "dm_id": dm1
    }).json()
    shared_m_id3 = shared_msg3["shared_message_id"]

    dm1_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm1,
        "start": 0
    }).json()

    dm2_messages = requests.get(f"{url}dm/messages/v1", params= {
        "token": user1["token"],
        "dm_id": dm2,
        "start": 0
    }).json()

    assert dm1_messages["messages"][2]["message_id"] == m_id
    assert dm1_messages["messages"][2]["message"] == "Hello"
    assert dm1_messages["messages"][1]["message_id"] == shared_m_id1
    assert dm1_messages["messages"][1]["message"] == '\n\n"""\nHello\n"""'
    assert dm1_messages["messages"][0]["message_id"] == shared_m_id3
    assert dm1_messages["messages"][0]["message"] == 'Hi\n\n"""\n\n    \n    """\n    \n        \n        """\n        Hello\n        """\n    """\n"""'
    assert len(dm1_messages["messages"]) == 3
    assert dm2_messages["messages"][0]["message_id"] == shared_m_id2
    assert dm2_messages["messages"][0]["message"] == '\n\n"""\n\n    \n    """\n    Hello\n    """\n"""'
    assert len(dm2_messages["messages"]) == 1
