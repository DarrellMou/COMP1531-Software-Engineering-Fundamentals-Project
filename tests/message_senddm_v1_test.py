
import pytest

from src.error import InputError, AccessError
from src.data import retrieve_data
from src.other import clear_v1
from src.auth import auth_register_v1, auth_decode_token
from src.dm import dm_create_v1, dm_invite_v1
from src.message import message_senddm_v1


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################

# Messages that are sent using message_senddm are appended to the message list
# within the dm


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates dm 1 with member u_id = 1
def set_up_data():
    clear_v1()
    
    # Populate data - create/register users 1 and 2 and have user 1 make dm1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    user3 = auth_register_v1('bing.bao@email.com', 'password123', 'Bing', 'Bao')
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])

    return {
        'user1': user1['token'],
        'user2': user2['token'],
        'user3': user3['token'],
        'dm1': dm1['dm_id']
    }
    return setup

def send_x_messages(user1, user2, dm1, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_senddm_v1(user1, dm1, str(message_num))
        else:
            message_senddm_v1(user2, dm1, str(message_num))
        message_count += 1
    
    return data

def send_x_messages_two_dms(user, dm1, dm2, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        message_senddm_v1(user, dm1, str(message_num))
        message_senddm_v1(user, dm2, str(message_num))
        message_count += 1
    return data


###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the dm (testing Access Error)
def test_message_senddm_v1_AccessError():
    setup = set_up_data()
    user1, user3, dm1 = setup['user1'], setup['user3'], setup['dm1']
    
    # user2 who is not a part of dm1 tries to send message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_senddm_v1(user3, dm1, "Hello")


# Testing to see if message is of valid length
def test_message_senddm_v1_InputError():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to dm 1
    with pytest.raises(InputError):
        assert message_senddm_v1(user1, dm1, long_message)


############################ END EXCEPTION TESTING ############################


############################ TESTING MESSAGE SEND #############################

# Testing for 1 message being sent by user1
def test_message_senddm_v1_send_one():
    setup = set_up_data()
    data = retrieve_data()

    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    assert message_senddm_v1(user1, dm1, "Hello")['message_id'] ==\
        data['dms'][dm1]['messages'][0]['message_id']


# Testing for 2 identical messages being sent by user1
def test_message_senddm_v1_user_sends_identical_messages():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']

    data = retrieve_data()

    first_message_id = message_senddm_v1(user1, dm1, "Hello")['message_id']
    second_message_id = message_senddm_v1(user1, dm1, "Hello")['message_id']

    assert first_message_id == data['dms'][dm1]['messages'][0]['message_id']
    assert second_message_id == data['dms'][dm1]['messages'][1]['message_id']

    assert first_message_id != second_message_id


# Testing for multiple messages with 2 users and that the correct messages are
# being sent
def test_message_senddm_v1_multiple_users_multiple_messages():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    u_id2 = auth_decode_token(user2)

    dm_invite_v1(user1, dm1, u_id2)

    send_x_messages(user1, user2, dm1, 10)

    data = retrieve_data()

    assert data['dms'][dm1]['messages'][0]['message'] == "1"
    assert data['dms'][dm1]['messages'][5]['message'] == "6"
    assert data['dms'][dm1]['messages'][9]['message'] == "10"


# Testing for multiple messages with 2 users and that the correct message_ids
# are being returned by message_send
def test_message_senddm_v1_multiple_users_multiple_messages_message_id():
    setup = set_up_data()
    user1, user2, dm1 = setup['user1'], setup['user2'], setup['dm1']
    u_id2 = auth_decode_token(user2)

    dm_invite_v1(user1, dm1, u_id2)

    data = retrieve_data()
    message_count = 0
    while message_count < 100:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_id = message_senddm_v1(user1, dm1, str(message_num))['message_id']
        else:
            message_id = message_senddm_v1(user2, dm1, str(message_num))['message_id']
        assert message_id == data['dms'][dm1]['messages'][message_count]['message_id']
        message_count += 1


# Same user sends the identical message to two different dms
# Message ids should be different
def test_message_senddm_v1_identical_message_to_2_dms():
    setup = set_up_data()
    user1, dm1, user3 = setup['user1'], setup['dm1'], setup['user3']
    u_id3 = auth_decode_token(user3)

    dm2 = dm_create_v1(user1, [u_id3])['dm_id']


    send_x_messages_two_dms(user1, dm1, dm2, 10)

    data = retrieve_data()

    m_id0_ch1 = data['dms'][dm1]['messages'][0]['message_id']
    m_id0_ch2 = data['dms'][dm2]['messages'][0]['message_id']
    m_id5_ch1 = data['dms'][dm1]['messages'][5]['message_id']
    m_id5_ch2 = data['dms'][dm2]['messages'][5]['message_id']
    m_id9_ch1 = data['dms'][dm1]['messages'][9]['message_id']
    m_id9_ch2 = data['dms'][dm2]['messages'][9]['message_id']

    assert m_id0_ch1 != m_id0_ch2
    assert m_id5_ch1 != m_id5_ch2
    assert m_id9_ch1 != m_id9_ch2

# Test if message_send also appends message to the data['messages'] list
def test_message_senddm_v1_appends_to_data_messages():
    setup = set_up_data()
    user1, dm1, user3 = setup['user1'], setup['dm1'], setup['user3']
    u_id3 = auth_decode_token(user3)

    dm2 = dm_create_v1(user1, [u_id3])['dm_id']
    
    send_x_messages_two_dms(user1, dm1, dm2, 10)
    
    data = retrieve_data()
    assert len(data['messages']) == 20


# Test if data['messages'] list is in order
def test_message_senddm_v1_data_messages_in_order():
    setup = set_up_data()
    user1, dm1, user3 = setup['user1'], setup['dm1'], setup['user3']
    u_id3 = auth_decode_token(user3)

    dm2 = dm_create_v1(user1, [u_id3])['dm_id']

    send_x_messages_two_dms(user1, dm1, dm2, 10)
    
    data = retrieve_data()

    m_id0_ch1 = data['dms'][dm1]['messages'][0]
    m_id0_ch2 = data['dms'][dm2]['messages'][0]
    m_id5_ch1 = data['dms'][dm1]['messages'][5]
    m_id5_ch2 = data['dms'][dm2]['messages'][5]
    m_id9_ch1 = data['dms'][dm1]['messages'][9]['message_id']
    m_id9_ch2 = data['dms'][dm2]['messages'][9]['message_id']

    assert data['messages'][0]['message_id'] == m_id0_ch1['message_id']
    assert data['messages'][0]['message'] == m_id0_ch1['message']
<<<<<<< HEAD
'''
=======
>>>>>>> nikki/message_senddm_v1
