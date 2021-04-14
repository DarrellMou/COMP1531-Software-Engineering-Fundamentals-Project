# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath

import pytest

from src.error import InputError, AccessError
from src.standup import standup_start_v1, standup_active_v1
from src.channels import channels_create_v2
from datetime import datetime
import time

def test_function_active(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 1)

    standup = standup_active_v1(users[0]['token'], ch_id0['channel_id'])

    assert standup["is_active"] == True
    assert float("{:.2f}".format(standup["time_finish"])) == float("{:.2f}".format(datetime.now().timestamp() + 1))
    time.sleep(2)

def test_function_inactive(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)

    standup = standup_active_v1(users[0]['token'], ch_id0['channel_id'])

    assert standup["is_active"] == False
    assert standup["time_finish"] == None

def test_multiple_runs(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 1)
    standup = standup_active_v1(users[0]['token'], ch_id0['channel_id'])

    assert standup["is_active"] == True
    assert float("{:.2f}".format(standup["time_finish"])) == float("{:.2f}".format(datetime.now().timestamp() + 1))
    time.sleep(2)


    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 3)
    standup = standup_active_v1(users[1]['token'], ch_id0['channel_id'])

    assert standup["is_active"] == True
    assert float("{:.2f}".format(standup["time_finish"])) == float("{:.2f}".format(datetime.now().timestamp() + 3))
    time.sleep(4)

    standup_start_v1(users[0]['token'], ch_id0['channel_id'], 5)
    standup = standup_active_v1(users[2]['token'], ch_id0['channel_id'])

    assert standup["is_active"] == True
    assert float("{:.2f}".format(standup["time_finish"])) == float("{:.2f}".format(datetime.now().timestamp() + 5))
    time.sleep(6)

def test_invalid_channel_id(users):
    with pytest.raises(InputError):
        standup_active_v1(users[0]['token'], 12345)

def test_invalid_token(users):
    ch_id0 = channels_create_v2(users[0]['token'], "Channel0", True)
    with pytest.raises(AccessError):
        standup_active_v1(12345, ch_id0['channel_id'])
