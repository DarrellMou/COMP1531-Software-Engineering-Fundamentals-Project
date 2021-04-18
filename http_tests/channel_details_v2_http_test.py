# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import json
import requests
import urllib

from src.config import url

###                         HELPER FUNCTIONS                           ###

def user_body(num):
    return {
        "email": f"example{num}@hotmail.com",
        "password": f"password{num}",
        "name_first": f"first_name{num}",
        "name_last": f"last_name{num}"
    }

def channel_create_body(user, num, is_public): 
    return {
        "token": user["token"],
        "name": f"channel{num}",
        "is_public": is_public
    }

def channel_invite_body(user1, channel, user2):
    return {
        "token": user1["token"],
        "channel_id": channel["channel_id"],
        "u_id": user2["auth_user_id"]
    }

def channel_details_body(user, channel):
    return {
        "token": user["token"],
        "channel_id": channel["channel_id"]
    }

###                       END HELPER FUNCTIONS                         ###

def test_function():
    requests.delete(f"{url}clear/v1")

    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()
    
    a_u_id1 = requests.post(f"{url}auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    ch_id0 = requests.post(f"{url}channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    requests.post(f"{url}channel/invite/v2", json=channel_invite_body(user0, channel0, user1))

    payload = requests.get(f"{url}channel/details/v2", params=channel_details_body(user0, channel0))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel0',
        'is_public': True,
        'owner_members': [
            {
                'u_id': user0['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            }
        ],
        'all_members': [
            {
                'u_id': user0['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            },
            {
                'u_id': user1['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            }
        ],
    }

def test_multiple():
    requests.delete(f"{url}clear/v1")

    users = []
    for i in range(10):
        a_u_id = requests.post(f"{url}auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    ch_id0 = requests.post(f"{url}channels/create/v2", json=channel_create_body(users[0], 0, True))
    channel0 = ch_id0.json()

    for i in range(1,10):
        requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[i]))

    payload = requests.get(f"{url}channel/details/v2", params=channel_details_body(users[0], channel0))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel0',
        'is_public': True,
        'owner_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            }
        ],
        'all_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            },
            {
                'u_id': users[1]['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': users[2]['auth_user_id'],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': users[3]['auth_user_id'],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': users[4]['auth_user_id'],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
            {
                'u_id': users[5]['auth_user_id'],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
            {
                'u_id': users[6]['auth_user_id'],
                'email': 'example6@hotmail.com',
                'name_first': 'first_name6',
                'name_last': 'last_name6',
                'handle_str': 'first_name6last_name'
            },
            {
                'u_id': users[7]['auth_user_id'],
                'email': 'example7@hotmail.com',
                'name_first': 'first_name7',
                'name_last': 'last_name7',
                'handle_str': 'first_name7last_name'
            },
            {
                'u_id': users[8]['auth_user_id'],
                'email': 'example8@hotmail.com',
                'name_first': 'first_name8',
                'name_last': 'last_name8',
                'handle_str': 'first_name8last_name'
            },
            {
                'u_id': users[9]['auth_user_id'],
                'email': 'example9@hotmail.com',
                'name_first': 'first_name9',
                'name_last': 'last_name9',
                'handle_str': 'first_name9last_name'
            }
        ],
    }

def test_multiple_channels():
    requests.delete(f"{url}clear/v1")

    users = []
    for i in range(10):
        a_u_id = requests.post(f"{url}auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    ch_id0 = requests.post(f"{url}channels/create/v2", json=channel_create_body(users[0], 0, True))
    channel0 = ch_id0.json()

    ch_id1 = requests.post(f"{url}channels/create/v2", json=channel_create_body(users[5], 1, True))
    channel1 = ch_id1.json()

    for i in range(1,5):
        requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[0], channel0, users[i]))

    for i in range(6,10):
        requests.post(f"{url}channel/invite/v2", json=channel_invite_body(users[5], channel1, users[i]))

    payload0 = requests.get(f"{url}channel/details/v2", params=channel_details_body(users[2], channel0))
    channel_details0 = payload0.json()

    assert channel_details0 == {
        'name': 'channel0',
        'is_public': True,
        'owner_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            }
        ],
        'all_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'email': 'example0@hotmail.com',
                'name_first': 'first_name0',
                'name_last': 'last_name0',
                'handle_str': 'first_name0last_name'
            },
            {
                'u_id': users[1]['auth_user_id'],
                'email': 'example1@hotmail.com',
                'name_first': 'first_name1',
                'name_last': 'last_name1',
                'handle_str': 'first_name1last_name'
            },
            {
                'u_id': users[2]['auth_user_id'],
                'email': 'example2@hotmail.com',
                'name_first': 'first_name2',
                'name_last': 'last_name2',
                'handle_str': 'first_name2last_name'
            },
            {
                'u_id': users[3]['auth_user_id'],
                'email': 'example3@hotmail.com',
                'name_first': 'first_name3',
                'name_last': 'last_name3',
                'handle_str': 'first_name3last_name'
            },
            {
                'u_id': users[4]['auth_user_id'],
                'email': 'example4@hotmail.com',
                'name_first': 'first_name4',
                'name_last': 'last_name4',
                'handle_str': 'first_name4last_name'
            },
        ],
    }

    payload1 = requests.get(f"{url}channel/details/v2", params=channel_details_body(users[8], channel1))
    channel_details1 = payload1.json()

    assert channel_details1 == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': users[5]['auth_user_id'],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            }
        ],
        'all_members': [
            {
                'u_id': users[5]['auth_user_id'],
                'email': 'example5@hotmail.com',
                'name_first': 'first_name5',
                'name_last': 'last_name5',
                'handle_str': 'first_name5last_name'
            },
            {
                'u_id': users[6]['auth_user_id'],
                'email': 'example6@hotmail.com',
                'name_first': 'first_name6',
                'name_last': 'last_name6',
                'handle_str': 'first_name6last_name'
            },
            {
                'u_id': users[7]['auth_user_id'],
                'email': 'example7@hotmail.com',
                'name_first': 'first_name7',
                'name_last': 'last_name7',
                'handle_str': 'first_name7last_name'
            },
            {
                'u_id': users[8]['auth_user_id'],
                'email': 'example8@hotmail.com',
                'name_first': 'first_name8',
                'name_last': 'last_name8',
                'handle_str': 'first_name8last_name'
            },
            {
                'u_id': users[9]['auth_user_id'],
                'email': 'example9@hotmail.com',
                'name_first': 'first_name9',
                'name_last': 'last_name9',
                'handle_str': 'first_name9last_name'
            }
        ],
    }

def test_invalid_channel_id():
    requests.delete(f"{url}clear/v1")

    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    payload = requests.get(f"{url}channel/details/v2", params=channel_details_body(user0, {"channel_id": 126347542124}))
    channel_details = payload.json()

    assert channel_details["code"] == 400
    assert channel_details["name"] == "System Error"
    assert channel_details["message"] == "<p></p>"

def test_unauthorized_user():
    requests.delete(f"{url}clear/v1")

    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()
    
    a_u_id1 = requests.post(f"{url}auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    ch_id0 = requests.post(f"{url}channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    payload = requests.get(f"{url}channel/details/v2", params=channel_details_body(user1, channel0))
    channel_details = payload.json()

    assert channel_details["code"] == 403
    assert channel_details["name"] == "System Error"
    assert channel_details["message"] == "<p>The user corresponding to the given token is not in the channel</p>"

def test_invalid_token():
    requests.delete(f"{url}clear/v1")

    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    ch_id0 = requests.post(f"{url}channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    payload = requests.get(f"{url}channel/details/v2", params=channel_details_body({"token": 18936087134}, channel0))
    channel_details = payload.json()

    assert channel_details["code"] == 403
    assert channel_details["name"] == "System Error"
    assert channel_details["message"] == "<p></p>"