# PROJECT-BACKEND: Team Echo
# Written by Brendan Ye

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_senddm_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1

def test_message_edit_v2_edit_one():
    clear_v1()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)['channel_id']

    msg_id = message_send_v2(user1["token"], channel1, "Hello")

    messages_info = channel_messages_v2(user1["token"], channel1, 0)['messages'][0]

    m_dict = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'Hello',
        'time_created': messages_info['time_created'],
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

    assert channel_messages_v2(user1["token"], channel1, 0) == pre_answer

    message_edit_v2(user1["token"], msg_id['message_id'], "HI")

    m_dict0 = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'HI',
        'time_created': messages_info['time_created'],
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

    assert channel_messages_v2(user1["token"], channel1, 0) == answer


def test_message_edit_v2_edit_one_dm():
    clear_v1()
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('bob.bulder@email.com', 'badpassword1', 'Bo', 'Bulder')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])['dm_id']

    msg_id = message_senddm_v1(user1["token"], dm1, "Hello")

    messages_info = dm_messages_v1(user1["token"], dm1, 0)['messages'][0]

    m_dict = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'Hello',
        'time_created': messages_info['time_created'],
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

    assert dm_messages_v1(user1["token"], dm1, 0) == pre_answer

    message_edit_v2(user1["token"], msg_id['message_id'], "HI")

    m_dict0 = {
        'message_id': msg_id['message_id'],
        'u_id': user1['auth_user_id'],
        'message': 'HI',
        'time_created': messages_info['time_created'],
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

    assert dm_messages_v1(user1["token"], dm1, 0) == answer
