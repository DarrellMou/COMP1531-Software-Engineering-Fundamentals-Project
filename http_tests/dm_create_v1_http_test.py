import json
import requests
import urllib

from src.data import retrieve_data

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
        "channel_id": dm["dm_id"]
    }


BASE_URL = 'http://127.0.0.1:6000'

def test_function():
    data = retrieve_data()

    requests.delete(f"{BASE_URL}/clear/v1")
    
    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    dm_id0 = requests.post(f"{BASE_URL}/dm/create/v1", json=dm_create_body(user0, [user1]))
    dm0 = dm_id0.json()

    payload = requests.get(f"{BASE_URL}/dm/details/v1", json=dm_details_body(user0, dm0))
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
            }
        ]
    }

'''
def test_multiple():
    data = retrieve_data()

    requests.delete(f"{BASE_URL}/clear/v1")

    users = []
    for i in range(5):
        a_u_id = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(i))
        users.append(a_u_id.json())

    dm_id0 = requests.post(f"{BASE_URL}/dm/create/v1", json=dm_create_body(users[0], users[1], users[2], users[3], users[4]))
    dm0 = dm_id0.json()

    assert dm0 == {
        'dm_id': data['users'][a_u_id1['auth_user_id']]['dms'][0],
        'dm_name': 'first_name1last_name, first_name2last_name, first_name3last_name, first_name4last_name, first_name5last_name'
    }

def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    
    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    dm_id0 = requests.post(f"{BASE_URL}/dm/create/v1", json=dm_create_body({"token": 107531534827}, [user0]))
    dm0 = dm_id0.json()

    assert payload.json()["code"] == 403
    assert payload.json()["name"] == "System Error"
    assert payload.json()["message"] == "<p></p>"
    
def test_invalid_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    
    a_u_id0 = requests.post(f"{BASE_URL}/auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    dm_id0 = requests.post(f"{BASE_URL}/dm/create/v1", json=dm_create_body(user0, [{"auth_user_id": 3295791357}]))
    dm0 = dm_id0.json()

    assert payload.json()["code"] == 400
    assert payload.json()["name"] == "System Error"
    assert payload.json()["message"] == "<p></p>"
'''