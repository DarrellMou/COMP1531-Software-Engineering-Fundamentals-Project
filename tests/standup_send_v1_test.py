# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import pytest

from src.error import InputError, AccessError
from src.standup import standup_start_v1, standup_send_v1
from src.channels import channels_create_v2
from src.channel import channel_messages_v2, channel_invite_v2
from src.data import retrieve_data
from datetime import datetime
import time

def test_function(users):
    data = retrieve_data()

    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message")

    time.sleep(6)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == f"{data['users'][users[0]["auth_user_id"]]["handle_str"]}: Test message"

def test_multiple_messages(users):
    data = retrieve_data()

    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message1")
    standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message2")
    standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message3")

    time.sleep(6)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == f'''
{data['users'][users[0]["auth_user_id"]]["handle_str"]}: Test message1
{data['users'][users[0]["auth_user_id"]]["handle_str"]}: Test message2
{data['users'][users[0]["auth_user_id"]]["handle_str"]}: Test message3'''

def test_multiple_messages_from_multiple_users(users):
    data = retrieve_data()

    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    channel_invite_v2(users[0]['token'], ch_id0['channel_id'], users[1]['auth_user_id'])
    channel_invite_v2(users[0]['token'], ch_id0['channel_id'], users[2]['auth_user_id'])
    channel_invite_v2(users[0]['token'], ch_id0['channel_id'], users[3]['auth_user_id'])
    channel_invite_v2(users[0]['token'], ch_id0['channel_id'], users[4]['auth_user_id'])

    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message0")
    standup_send_v1(users[1]['token'], ch_id0['channel_id'], "Test message1")
    standup_send_v1(users[2]['token'], ch_id0['channel_id'], "Test message2")
    standup_send_v1(users[3]['token'], ch_id0['channel_id'], "Test message3")
    standup_send_v1(users[4]['token'], ch_id0['channel_id'], "Test message4")

    time.sleep(6)

    messages_list = channel_messages_v2(user1["token"], channel1, 0)

    assert messages_list['messages'][0]["u_id"] == users[0]["auth_user_id"]
    assert messages_list['messages'][0]["message"] == f'''
{data['users'][users[0]["auth_user_id"]]["handle_str"]}: Test message0
{data['users'][users[1]["auth_user_id"]]["handle_str"]}: Test message1
{data['users'][users[2]["auth_user_id"]]["handle_str"]}: Test message2
{data['users'][users[3]["auth_user_id"]]["handle_str"]}: Test message3
{data['users'][users[4]["auth_user_id"]]["handle_str"]}: Test message4'''

def test_invalid_channel_id(users):
    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], 12345, "Test message0")

def test_too_long_message(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], ch_id0['channel_id'], long_message)
    time.sleep(6)

def test_inactive_standup(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)

    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], ch_id0['channel_id'], "Test message")

def test_unauthorized_user(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    with pytest.raises(AccessError):
        standup_send_v1(users[1]['token'], ch_id0['channel_id'], "Test message")
    time.sleep(6)

def test_invalid_token(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    with pytest.raises(AccessError):
        standup_send_v1(12345, ch_id0['channel_id'], "Test message")
    time.sleep(6)