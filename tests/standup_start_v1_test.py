# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import pytest

from src.error import InputError, AccessError
from src.standup import standup_start_v1
from src.channels import channels_create_v2
from datetime import datetime
import time

def test_function(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    time_finish = standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    assert time_finish == int(datetime.now().timestamp() + 5)
    time.sleep(6)

def test_multiple_runs(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    time_finish1 = standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)

    assert time_finish1 == int(datetime.now().timestamp() + 5)
    
    time.sleep(6)

    time_finish2 = standup_start_v1(users[0]['token'], ch_id0['channel_id'], 10)

    assert time_finish2 == int(datetime.now().timestamp() + 10)

    time.sleep(11)

    time_finish3 = standup_start_v1(users[0]['token'], ch_id0['channel_id'], 20)

    assert time_finish3 == int(datetime.now().timestamp() + 20)

    time.sleep(21)

def test_invalid_channel_id(users):
    with pytest.raises(InputError):
        standup_start_v1(users[0]['token'], 12345, 1)

def test_active_standup(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 1)

    with pytest.raises(InputError):
        standup_start_v1(users[0]['token'], ch_id0['channel_id'], 1)
    time.sleep(1)

def test_unauthorized_user(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)

    with pytest.raises(AccessError):
        standup_start_v1(users[1]['token'], ch_id0['channel_id'], 1)

def test_invalid_token(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)

    with pytest.raises(AccessError):
        standup_start_v1(12345, ch_id0['channel_id'], 1)