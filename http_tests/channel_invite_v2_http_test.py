import json
import requests
import urllib

BASE_URL = 'http://127.0.0.1:8080'

def test_function():
    requests.delete(f"{BASE_URL}/clear/v1")

    r = requests.post(f"{BASE_URL}/auth/register/v1", json={
        "email": "example1@hotmail.com",
        "password": "password1",
        "name_first": "first_name1",
        "name_last": "last_name1"
    })
    payload1 = r.json()
    
    r = requests.post(f"{BASE_URL}/auth/register/v1", json={
        "email": "example2@hotmail.com",
        "password": "password2",
        "name_first": "first_name2",
        "name_last": "last_name2"
    })
    payload2 = r.json()

    r = requests.post(f"{BASE_URL}/dm/create/v1", json={
        "token": payload1['token'],
        "auth_user_id": payload2['auth_user_id']
    })

    assert r.json()['dm_name'] == 'first_name1last_name, first_name2last_name'

test_system()