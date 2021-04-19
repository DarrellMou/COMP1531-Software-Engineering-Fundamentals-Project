# PROJECT-BACKEND: Team Echo
# Written by Kellen

import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_send_v2, message_senddm_v1, message_react_v1
from src.data import retrieve_data
from src.other import clear_v1


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Messages that are sent using send_message are appended to the message list
# within the channel


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates channel_1 with member u_id = 1
def set_up_data():
    clear_v1()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)

    setup = {
        'user1': user1,
        'user2': user2,
        'channel1': channel1['channel_id']
    }

    return setup

#Define like react
like = 1

###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# The user attempts to react to a message id that doesn't exist in any of his channels
def test_react_v1_invalid_message_id_nonexistent_InputError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    # Fill the channel and dm with one message
    message_send_v2(user1["token"], channel1, "Hello world!_ch")
    message_senddm_v1(user1['token'], dmid1['dm_id'], "Hello world!_dm")

    # dict jank
    bad_id = {
        'message_id': -9999
    }

    # user1 tries to react to a message that doesn't exist in either of his channels
    with pytest.raises(InputError):
        message_react_v1(user1["token"], bad_id, like)


# The react id the user sends is not valid (currently only id 1 is valid)
def test_react_v1_invalid_react_id_InputError():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    # User 1 sends message in a channel, of which they are the only user
    message_id = message_send_v2(user1["token"], channel1, "Hello world!")

    # user1 tries to react to his own message (legal) with a react that doesn't exist (illegal)
    with pytest.raises(InputError):
        message_react_v1(user1["token"], message_id['message_id'], -9999)


# User has already reacted to the same message id with the same react id
def test_react_v1_repeat_react_InputError():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    # User 1 sends message in a channel, of which they are the only user and likes
    # his own message
    message_id = message_send_v2(user1["token"], channel1, "Hello world!")
    message_react_v1(user1["token"], message_id['message_id'], like)

    # user1 tries to react again with the same id
    with pytest.raises(InputError):
        message_react_v1(user1["token"], message_id['message_id'], like)


# The user attempts to react to an existing message, but is not in the corresponding channel
def test_react_v1_invalid_message_id_inaccessible_channel_InputError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']

    # User 1 sends message in a channel, of which they are the only user
    message_id = message_send_v2(user1["token"], channel1, "Hello world!")

    # user2 tries to react the message despite not being a member of channel1
    with pytest.raises(AccessError):
        message_react_v1(user2["token"], message_id['message_id'], like)


# The user attempts to react to an existing message, but is not in the corresponding dm
def test_react_v1_invalid_message_id_inaccessible_dm_InputError():
    setup = set_up_data()
    user1, user2 = setup['user1'], setup['user2']
    user3 = auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    # User1 sends message in dm, of which user3 is not a part of
    message_id = message_senddm_v1(user1['token'], dmid1['dm_id'], 'Hello world!')

    # user3 tries to react the message despite not being a member of channel1
    with pytest.raises(AccessError):
        message_react_v1(user3["token"], message_id['message_id'], like)


# Default access error when token is invalid
def test_message_react_v1_default_Access_Error():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']
    message_id = message_send_v2(user1["token"], channel1, "Hello world!")

    with pytest.raises(AccessError):
        message_react_v1("imposter", message_id['message_id'], like)

############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE REACT #############################

# Testing for user reacting to another user's in channel
def test_message_react_v1_channel():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    channel_invite_v2(user1['token'], channel1, user2['auth_user_id'])

    message_id = message_send_v2(user2["token"], channel1, "Hello")
    message_react_v1(user1["token"], message_id['message_id'], like)
    data = retrieve_data()
    assert data['messages'][0]["reacts"][0]["u_ids"] == [user1["auth_user_id"]]
    assert data['messages'][0]["reacts"][0]["react_id"] == 1


# Testing for user reacting to another user's in dm
def test_message_react_v1_dm():
    setup = set_up_data()
    user1, user2 = setup['user1'], setup['user2']
    dmid1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    message_id = message_senddm_v1(user2["token"], dmid1["dm_id"], "Hello")
    message_react_v1(user1["token"], message_id['message_id'], like)
    data = retrieve_data()

    assert data['messages'][0]["reacts"][0]["u_ids"] == [user1["auth_user_id"]]
    assert data['messages'][0]["reacts"][0]["react_id"] == 1


# Testing for user reacting to themselves
def test_message_react_v1_self():
    setup = set_up_data()
    user1, channel1 = setup['user1'], setup['channel1']

    message_id = message_send_v2(user1["token"], channel1, "Hello")
    message_react_v1(user1["token"], message_id['message_id'], like)

    data = retrieve_data()

    assert data['messages'][0]["reacts"][0]["u_ids"] == [user1["auth_user_id"]]
    assert data['messages'][0]["reacts"][0]["react_id"] == 1


# Testing for reacts on different messages
def test_message_react_v1_different_messages():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    channel_invite_v2(user1['token'], channel1, user2['auth_user_id'])

    message_id1 = message_send_v2(user1["token"], channel1, "Creeper")
    message_react_v1(user2["token"], message_id1['message_id'], like)

    message_id2 = message_send_v2(user2["token"], channel1, "Oh")
    message_react_v1(user1["token"], message_id2['message_id'], like)

    message_send_v2(user1["token"], channel1, "Man")

    data = retrieve_data()

    assert data['messages'][0]["reacts"][0]["u_ids"] == [user2["auth_user_id"]]
    assert data['messages'][0]["reacts"][0]["react_id"] == 1

    assert data['messages'][1]["reacts"][0]["u_ids"] == [user1["auth_user_id"]]
    assert data['messages'][1]["reacts"][0]["react_id"] == 1

    assert data['messages'][2]["reacts"] == []

# Testing for multiple reacts on the same message
def test_message_react_v1_multiple_reacts():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    user3 = auth_register_v1('user3@gmail.com', 'password123', 'first3', 'last3')
    channel_invite_v2(user1['token'], channel1, user2['auth_user_id'])
    channel_invite_v2(user1['token'], channel1, user3['auth_user_id'])

    message_id = message_send_v2(user1["token"], channel1, "3 likes on this message and I die")
    message_react_v1(user1["token"], message_id['message_id'], like)
    message_react_v1(user2["token"], message_id['message_id'], like)
    message_react_v1(user3["token"], message_id['message_id'], like)

    data = retrieve_data()

    assert data['messages'][0]["reacts"][0]["u_ids"] == [user1["auth_user_id"], user2["auth_user_id"], user3["auth_user_id"]]
    assert data['messages'][0]["reacts"][0]["react_id"] == 1