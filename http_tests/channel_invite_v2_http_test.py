import json
import requests
import urllib

# HELPER FUNCTIONS

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

BASE_URL = 'http://127.0.0.1:6000'

def test_function():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()
    
    a_u_id1 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(user0, channel0, user1))

    payload = requests.get(f"{BASE_URL}/channel/details/v2", json=channel_details_body(user0, channel0))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': user0['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': user0['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            },
            {
                'u_id': user1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
    }

def test_multiple():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    users = []
    for i in range(5):
        a_u_id = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(users[0], 0, True))
    channel0 = ch_id0.json()

    for i in range(1,5):
        requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(users[0], channel0, users[i]))

    payload = requests.get(f"{BASE_URL}/channel/details/v2", json=channel_details_body(users[0], channel0))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            },
            {
                'u_id': users[1]['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': users[2]['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': users[3]['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': users[4]['auth_user_id'],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
        ],
    }

def test_multiple_users_invite():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    users = []
    for i in range(5):
        a_u_id = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(users[0], 0, True))
    channel0 = ch_id0.json()

    for i in range(4):
        requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(users[i], channel0, users[i + 1]))

    payload = requests.get(f"{BASE_URL}/channel/details/v2", json=channel_details_body(users[0], channel0))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel0',
        'owner_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            }
        ],
        'all_members': [
            {
                'u_id': users[0]['auth_user_id'],
                'name_first': 'first_name0',
                'name_last': 'last_name0',
            },
            {
                'u_id': users[1]['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': users[2]['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': users[3]['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': users[4]['auth_user_id'],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
        ],
    }

def test_invalid_channel_id():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    r = requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(user0, channel0, {"auth_user_id": 1216374684571}))

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_invalid_invited_user():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    r = requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(user0, {"channel_id": 319245780425}, user1))
    print(r)

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_unauthorized_user():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    users = []
    for i in range(3):
        a_u_id = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(users[0], 0, True))
    channel0 = ch_id0.json()

    r = requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(users[1], channel0, users[2]))
    
    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_invalid_token():
    r = requests.delete(f"{BASE_URL}/clear/v1")

    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    ch_id0 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(user0, 0, True))
    channel0 = ch_id0.json()

    r = requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body({"token": 18936087134}, channel0, {"auth_user_id": 1216374684571}))

    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"
