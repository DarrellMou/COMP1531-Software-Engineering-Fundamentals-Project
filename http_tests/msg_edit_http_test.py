import json
import requests
import pytest
from src.config import url

def test():
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { # Dreams owner
        "email": "bob.builder@email.com",
        "password": "badpassword1",
        "name_first": "Bob",
        "name_last": "Builder"
    }).json()

    channel1 = requests.post(f"{url}channels/create/v2", json = {
        "token": user1["token"],
        "name": "Channel1",
        "is_public": True
    }).json()

    msg_id = requests.post(f"{url}message/send/v2", json= {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "message": "Hello"
    }).json()

    messages_info = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    m_dict = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'Hello',
        'time_created': messages_info['messages'][0]['time_created'],
        'reacts': [{
            'react_id': 1,
            'u_ids': [],
            'is_this_user_reacted': False
        }],
        'is_pinned': False
    }

    pre_answer = {
        'messages': [m_dict],
        'start': 0,
        'end': -1
    }

    first_ans = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert first_ans == pre_answer
    
    requests.put(f"{url}message/edit/v2", json={
        "token": user1["token"],
        "message_id": msg_id["message_id"],
        "message": "Bao"
    }).json()

    m_dict0 = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'Bao',
        'time_created': messages_info['messages'][0]['time_created'],
        'reacts': [{
            'react_id': 1,
            'u_ids': [],
            'is_this_user_reacted': False
        }],
        'is_pinned': False
    }
    
    answer = {
        'messages': [m_dict0],
        'start': 0,
        'end': -1
    }

    ans = requests.get(f"{url}channel/messages/v2", params= {
        "token": user1["token"],
        "channel_id": channel1["channel_id"],
        "start": 0
    }).json()

    assert ans == answer
