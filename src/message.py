
from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token
from uuid import uuid4
from datetime import datetime
'''
from data import data, retrieve_data, reset_data
from error import AccessError, InputError
from auth import auth_token_ok, auth_decode_token, auth_register_v1
from uuid import uuid4
from datetime import datetime
from channel import channel_invite_v1
from channels import channels_create_v1
'''


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# Given a message_id return the channel in which it was sent
def get_channel_id(message_id):
    data = retrieve_data()
    for msg in data['messages']:
        if msg['message_id'] == message_id:
            return msg['channel_id']




###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################


def message_send_v2(token, channel_id, message):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check to see if the message is too long
    if len(message) > 1000:
        raise InputError("The message exceeds 1000 characters")
    
    # Check to see if the given user (from token) is actully in the given channel
    user_id = auth_decode_token(token)
    if user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError("The user corresponding to the given token is not in the channel")


    # Creating a unique id for our message_id. The chances of uuid4 returning
    # the same time is infinitesimally small.
    # ASSUMPTION: int(uuid4()) will never reproduce the same id
    unique_message_id = int(uuid4())
    # Creating a timestamp for our time_created key for our messages dictionary
    # which is based on unix time (epoch/POSIX time)
    time_created_timestamp = round(datetime.now().timestamp())

    # Create a dictionary which we will append to our messages list in our channel
    channel_message_dictionary = {
        'message_id': unique_message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created_timestamp,
    }

    # Create a dictionary which we will append to our data['messages'] list
    message_dictionary = {
        'message_id': unique_message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created_timestamp,
        'channel_id': channel_id,
        'is_removed': False,
    }

    # Append our dictionaries to their appropriate lists
    data['channels'][channel_id]['messages'].append(channel_message_dictionary)
    data['messages'].append(message_dictionary)

    return {
        'message_id': unique_message_id
    }

def message_remove_v2(token, message_id):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check if the message_id given is already deleted
    for message_dict in data['messages']:
        if message_dict['message_id'] == message_id:
            if message_dict['is_removed'] == True:
                raise InputError("Message (based on id) no longer exists")
    #result = [True for x in data['messages'] if x['message_id'] == message_id and x['is_removed']]
    #if result[0]: raise InputError("Message (based on id) no longer exists")
    
    # Check to see if the user trying to remove the message sent the message
    given_id = auth_decode_token(token)
    did_user_send, is_ch_owner, is_dreams_owner, is_owner = True, False, False, False
    for msg_dict in data['messages']:
        if msg_dict['message_id'] == message_id:
            if msg_dict['u_id'] != given_id:
                did_user_send = False
    # Now, check to see if the user is an owner of the channel
    ch_id = get_channel_id(message_id)
    for member in data['channels'][ch_id]['owner_members']:
        if given_id == member:
            is_ch_owner = True
    # Now, check to see if the user is an owner of dreams server
    if data['users'][given_id]['permission_id'] == 1:
        is_dreams_owner = True
    if is_ch_owner or is_dreams_owner:
        is_owner = True
    AccessErrorConditions = [is_owner, did_user_send]
    #return AccessErrorConditions
    if not any(AccessErrorConditions):
        raise AccessError("User is not dreams owner or channel owner and did not send the message")

    for msg in data['messages']:
        if msg['message_id'] == message_id:
            msg['is_removed'] = True

    return {
}

def message_edit_v2(token, message_id, message):
    return {
    }

'''
data = reset_data()

user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
channel_invite_v1(user1['auth_user_id'], channel1['channel_id'], user2['auth_user_id'])

m_id = message_send_v2(user1['token'], channel1['channel_id'], "Hey")['message_id']


print(data)

print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")

blah = message_remove_v2(user2['token'], m_id)
print(blah)
'''