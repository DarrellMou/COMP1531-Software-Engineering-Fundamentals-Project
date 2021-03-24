import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v1
from src.data import reset_data, retrieve_data, data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.message import message_send_v2, message_remove_v2, message_edit_v2


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Sharing a message will add a new message to the data['messages'] list and to
# the channel's or dm's messages list


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates channel_1 with member u_id = 1
def set_up_data():
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1 and
    # channel2 and invite user2 to the channels
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])
    channel2 = channels_create_v1(user1['auth_user_id'], 'Channel2', True)
    channel_invite_v1(user1['auth_user_id'], channel2['channel_id'], user2['auth_user_id'])


    setup = {
        'user1': user1['token'],
        'user2': user2['token'],
        'channel1': channel1['channel_id'],
        'channel2': channel2['channel_id']
    }

    return setup


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing to see if the user who is sharing the message to a channel/dm is
# actually in that channel/dm
def test_message_share_v1_AccessError():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']

    u_id1 = auth_decode_token(user1)

    channel3 = channels_create_v1(u_id1, "ch3, True)['channel_id']

    with pytest.raises(InputError):
        assert message_share_v1(user2, m_id, "Optional Message", channel3, -1)


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SHARE ############################

# Testing user1 sharing one message to channel
def test_message_share_v1_share_one_to_channel():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']

    shared_m_id = message_share_v1(user2, m_id, "Shared Message 1", channel2, -1)['shared_message_id']

    assert data['messages'][1]['message_id'] == shared_m_id
    assert data['messages'][1]['message'] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert data['messages'][0]['message_id'] == m_id
    assert data['messages'][0]['message'] == "Hello"
    assert data['channels'][channel1]['messages'][0]['message_id'] == m_id
    assert data['channels'][channel2]['messages'][0]['message_id'] == shared_m_id
    assert len(data['channels'][channel2]['messages']) == 1
    assert len(data['channels'][channel1]['messages']) == 1
    assert len(data['messages']) == 2


# Sharing and resharing the message a few times to differing channels
def test_message_share_v1_share_one_multiple_times():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2, m_id, "Shared Message 1", channel2, -1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2, shared_m_id1, "Shared Message 2", channel1, -1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2, shared_m_id2, "Shared Message 3", channel2, -1)['shared_message_id']

    assert data['messages'][0]['message_id'] == m_id
    assert data['messages'][0]['message'] == "Hello"
    assert data['messages'][1]['message_id'] == shared_m_id1
    assert data['messages'][1]['message'] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert data['messages'][3]['message_id'] == shared_m_id3
    assert data['messages'][3]['message'] == 'Shared Message 3\n\n"""\nShared Message 2\n\n    """\
        \n    Shared Message\n\n        """\n        Hello\n        """\n    """\n"""'
    assert data['channels'][channel1]['messages'][0]['message_id'] == m_id
    assert data['channels'][channel2]['messages'][0]['message_id'] == shared_m_id
    assert data['channels'][channel2]['messages'][1]['message'] == data['messages'][3]['message']
    assert len(data['channels'][channel2]['messages']) == 2
    assert len(data['channels'][channel1]['messages']) == 2
    assert len(data['messages']) == 4


# Sharing to the same channel
def test_message_share_v1_share_one_multiple_times():
    setup = set_up_data()
    user1, user2, channel1, channel2 = setup['user1'], setup['user2'], setup['channel1'], setup['channel2']
    m_id = message_send_v2(user1, channel1, "Hello")['message_id']

    shared_m_id1 = message_share_v1(user2, m_id, "Shared Message 1", channel1, -1)['shared_message_id']
    shared_m_id2 = message_share_v1(user2, shared_m_id1, "Shared Message 2", channel1, -1)['shared_message_id']
    shared_m_id3 = message_share_v1(user2, shared_m_id2, "Shared Message 3", channel1, -1)['shared_message_id']

    assert data['messages'][0]['message_id'] == m_id
    assert data['messages'][0]['message'] == "Hello"
    assert data['messages'][1]['message_id'] == shared_m_id1
    assert data['messages'][1]['message'] == 'Shared Message 1\n\n"""\nHello\n"""'
    assert data['messages'][3]['message_id'] == shared_m_id3
    assert data['messages'][3]['message'] == 'Shared Message 3\n\n"""\nShared Message 2\n\n    """\
        \n    Shared Message\n\n        """\n        Hello\n        """\n    """\n"""'
    assert data['channels'][channel1]['messages'][0]['message_id'] == m_id
    assert data['channels'][channel1]['messages'][0]['message_id'] == shared_m_id
    assert data['channels'][channel1]['messages'][3]['message'] == data['messages'][3]['message']
    assert len(data['channels'][channel1]['messages']) == 4
    assert len(data['messages']) == 4



# Testing user1 sharing one message from channel to dm



# Sharing and resharing the message a few times to differing dms


