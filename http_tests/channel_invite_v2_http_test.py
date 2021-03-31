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

    a_u_id1 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()
    
    a_u_id2 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(2))
    user2 = a_u_id2.json()

    ch_id1 = requests.post(f"{BASE_URL}/channels/create/v2", json=channel_create_body(user1, 1, True))
    channel1 = ch_id1.json()

    r = requests.post(f"{BASE_URL}/channel/invite/v2", json=channel_invite_body(user1, channel1, user2))

    payload = requests.get(f"{BASE_URL}/channel/details/v2", json=channel_details_body(user1, channel1))
    channel_details = payload.json()

    assert channel_details == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': user1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            }
        ],
        'all_members': [
            {
                'u_id': user1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': user2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            }
        ],
    }
