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

def test_function():
    requests.delete(f"{url}clear/v1")
    
    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{url}auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body(user0, [user1]))
    dm0 = dm_id0.json()

    payload = requests.get(f"{url}dm/details/v1", params=dm_details_body(user0, dm0))
    dm_details = payload.json()

    assert dm_details == {
        'name': 'first_name0last_name, first_name1last_name',
        'members': [
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
        ]
    }

def test_multiple():
    requests.delete(f"{url}clear/v1")

    users = []
    for i in range(5):
        a_u_id = requests.post(f"{url}auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body(users[0], [users[1], users[2], users[3], users[4]]))
    dm0 = dm_id0.json()

    payload = requests.get(f"{url}dm/details/v1", params=dm_details_body(users[0], dm0))
    dm_details = payload.json()

    assert dm_details == {
        'name': 'first_name0last_name, first_name1last_name, first_name2last_name, first_name3last_name, first_name4last_name',
        'members': [
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
        ]
    }

def test_invalid_token():
    requests.delete(f"{url}clear/v1")
    
    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body({"token": 18936087134}, [user0]))
    dm0 = dm_id0.json()

    assert dm0["code"] == 403
    assert dm0["name"] == "System Error"
    assert dm0["message"] == "<p></p>"

def test_invalid_user():
    requests.delete(f"{url}clear/v1")
    
    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body(user0, [{"auth_user_id": 3295791357}]))
    dm0 = dm_id0.json()

    assert dm0["code"] == 400
    assert dm0["name"] == "System Error"
    assert dm0["message"] == "<p></p>"
    