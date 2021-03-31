import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v1
from src.dm import dm_create_v1, dm_invite_v1
from src.data import reset_data, retrieve_data, data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.message import message_send_v2 message_senddm_v1
from src.notifications import notifications_get_v1

def set_up_users():
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1 and
    # channel2 and invite user2 to the channels
    user1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    user2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    user3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')

    setup = {
        'user1': user1['token'],
        'user2': user2['token'],
        'user3': user3['token'],
    }

    return setup

def test_channelinvite():
    setup = set_up_users()
    user1, user2, user3 = setup['user1'], setup['user2'], setup['user3']

    chid1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])
    channel_invite_v1(user2['auth_user_id'], channel1['channel_id'], user3['auth_user_id'])

    assert notifications_get_v1(user2['token']) == {
        {
            'channel_id' : chid1,
            'dm_id' : -1,
            'notification_message' : 'first_name1last_name1 added you to channel1',
        },
    }
    assert notifications_get_v1(user3) == {
        {
            'channel_id' : chid1,
            'dm_id' : -1,
            'notification_message' : 'first_name1last_name1 added you to channel1',
        },
    }