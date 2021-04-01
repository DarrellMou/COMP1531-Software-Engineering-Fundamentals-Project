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

def dm_details_body(user, dm):
    return {
        "token": user["token"],
        "dm_id": dm["dm_id"]
    }

def dm_invite_body(user1, dm, user2):
    return {
        "token": user1["token"],
        "dm_id": dm["dm_id"],
        "u_id": user2["auth_user_id"]
    }

def test_function():
    requests.delete(f"{url}/clear/v1")

    users = []
    for i in range(3):
        a_u_id = requests.post(f"{url}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{url}/dm/create/v1", json=dm_create_body(users[0], [users[1], users[2], users[3], users[4]]))
    dm0 = dm_id0.json()

    requests.post(f"{url}/dm/invite/v1", json=dm_invite_body(users[0], dm0, users[2]))

    payload = requests.get(f"{url}/dm/details/v1", json=dm_details_body(users[0], dm0))
    dm_details = payload.json()

    assert dm_details == {
        'name': 'first_name1last_name, first_name2last_name',
        'members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            }
        ]
    }

def test_multiple():
    requests.delete(f"{url}/clear/v1")
    
    users = []
    for i in range(5):
        a_u_id = requests.post(f"{url}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{url}/dm/create/v1", json=dm_create_body(users[0], [users[1]]))
    dm0 = dm_id0.json()

    for i in range(3):
        requests.post(f"{url}/dm/invite/v1", json=dm_invite_body(users[0], dm0, users[i + 2]))

    payload = requests.get(f"{url}/dm/details/v1", json=dm_details_body(users[0], dm0))
    dm_details = payload.json()

    assert dm_details == {
        'name': 'first_name1last_name, first_name2last_name',
        'members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': a_u_id4['auth_user_id'],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
            {
                'u_id': a_u_id5['auth_user_id'],
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            }
        ]
    }

def test_invalid_token():
    requests.delete(f"{url}/clear/v1")

    users = []
    for i in range(3):
        a_u_id = requests.post(f"{url}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{url}/dm/create/v1", json=dm_create_body(users[0], [users[1]]))
    dm0 = dm_id0.json()

    r = requests.post(f"{url}/dm/invite/v1", json=dm_invite_body({"token": 3165801385}, dm0, users[2]))

    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_invalid_dm_id():
    requests.delete(f"{url}/clear/v1")

    a_u_id0 = requests.post(f"{url}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{url}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    r = requests.post(f"{url}/dm/invite/v1", json=dm_invite_body(user0, {"dm_id": 427602476}, user1))

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_invalid_user():
    requests.delete(f"{url}/clear/v1")

    a_u_id0 = requests.post(f"{url}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{url}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    dm_id0 = requests.post(f"{url}/dm/create/v1", json=dm_create_body(users[0], [users[1]]))
    dm0 = dm_id0.json()

    r = requests.post(f"{url}/dm/invite/v1", json=dm_invite_body(users[0], dm0, {"auth_user_id": 671836071683}))

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

def test_unauthorised_user():
    requests.delete(f"{url}/clear/v1")

    users = []
    for i in range(4):
        a_u_id = requests.post(f"{url}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{url}/dm/create/v1", json=dm_create_body(users[0], [users[1]]))
    dm0 = dm_id0.json()

    r = requests.post(f"{url}/dm/invite/v1", json=dm_invite_body(users[2], dm0, users[3]))

    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"
