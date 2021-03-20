import pytest

from src.error import InputError, AccessError
from src.channel import channel_messages_v2, channel_invite_v1
from src.data import reset_data, retrieve_data
from src.auth import auth_register_v1, auth_decode_token
from src.channels import channels_create_v1
from src.message import message_send_v2


###############################################################################
#                                 ASSUMPTIONS                                 #
###############################################################################




###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Simple data population helper function; registers users 1 and 2,
# creates channel_1 with member u_id = 1
def set_up_data():
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)

    setup = {
        'user1': user1['token'],
        'user2': user2['token'],
        'channel1': channel1['channel_id']
    }

    return setup


def send_x_messages(user1, user2, channel1, num_messages):
    data = retrieve_data()
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            message_send_v2(user1, channel1, str(message_num))
        else:
            message_send_v2(user2, channel1, str(message_num))
        message_count += 1
    
    return data



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ##############################

# Testing for when the user is not part of the channel (testing Access Error)
def test_message_send_v2_AccessError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # user2 who is not a part of channel_1 tries to send message 
    # - should raise an access error
    with pytest.raises(AccessError):
        assert message_send_v2(user2, channel1, "Hello")


# Testing to see if message is of valid length
def test_message_send_v2_InputError():
    setup = set_up_data()
    user1, user2, channel1 = setup['user1'], setup['user2'], setup['channel1']
    
    # Create a message that is 1001 characters long (which exceeds character limit)
    long_message = ""
    while len(long_message) < 1001:
        long_message += "a" 

    # user1 tries to send a message that is too long to channel 1
    with pytest.raises(InputError):
        assert message_send_v2(user1, channel1, long_message)


############################ END EXCEPTION TESTING ############################