import json
import requests
import urllib

from src.config import url
# HELPER FUNCTIONS

def user_body(num):
    return {
        "email": f"example{num}@hotmail.com",
        "password": f"password{num}",
        "name_first": f"first_name{num}",
        "name_last": f"last_name{num}"
    }

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        "token": user["token"],
        "u_ids": u_ids_list
    }

def dm_list_body(user):
    return {
        "token": user["token"],
    }

def test_function():
    requests.delete(f"{url}clear/v1")
    
    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{url}auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body(user0, [user1]))
    dm0 = dm_id0.json()

    r = requests.get(f"{url}dm/list/v1", json=dm_list_body(user0))
    dm_list = r.json()

    assert dm_list == {
        'dms': [
            {
                'dm_id': dm0['dm_id'],
                'name': dm0['dm_name']
            }
        ]
    }

def test_multiple():
    requests.delete(f"{url}clear/v1")

    users = []
    for i in range(5):
        a_u_id = requests.post(f"{url}auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dms = []
    for i in range(4):
        dm_id = requests.post(f"{url}dm/create/v1", json=dm_create_body(users[0], [users[i + 1]]))
        dms.append(dm_id.json())

    r = requests.get(f"{url}dm/list/v1", json=dm_list_body(users[0]))
    dm_list = r.json()

    assert dm_list == {
        'dms': [
            {
                'dm_id': dms[0]['dm_id'],
                'name': dms[0]['dm_name']
            },
            {
                'dm_id': dms[1]['dm_id'],
                'name': dms[1]['dm_name']
            },
            {
                'dm_id': dms[2]['dm_id'],
                'name': dms[2]['dm_name']
            },
            {
                'dm_id': dms[3]['dm_id'],
                'name': dms[3]['dm_name']
            }
        ]
    }

def test_invalid_token():
    requests.delete(f"{url}clear/v1")

    r = requests.get(f"{url}dm/list/v1", json=dm_list_body({"token": 513875017835}))
    dm_list = r.json()

    assert dm_list["code"] == 403
    assert dm_list["name"] == "System Error"
    assert dm_list["message"] == "<p></p>"