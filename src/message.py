
from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token
from uuid import uuid4
from datetime import datetime
import re
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

# Given a message_id return the message within that message_id
def get_message(message_id):
    data = retrieve_data()
    for msg in data['messages']:
        if msg['message_id'] == message_id:
            return msg['message']

# Given a message_id, return whether the message is a shared message or not
def get_share_status(message_id):
    data = retrieve_data()
    for msg in data['messages']:
        if msg['message_id'] == message_id:
            return msg['was_shared']


# Given a message, return a tab in front of the relevant lines
def tab_given_message(msg):
    msg_len = len(msg)
    index = 0
    for n in range(0, len(msg)):
        if msg[n] == msg[n + 1] == msg[n + 2] == '"':
            index = n - 2
            break
    beginning_of_string = msg[0:index]
    to_be_changed_str = msg[index:]
    changed_string = to_be_changed_str.replace("\n", "\n    ")

    tabbed_msg = beginning_of_string + changed_string
    return tabbed_msg


    '''
    for n in range(0, msg_len):
        if msg[n] == msg[n + 1] == msg[n + 2] == '"':
            if count == 0:
                count = 0.5
        if count == 0.5 and msg[n] == '\n':
            count = 1
        if count == 1 and msg[n] == '\n':
            msg = msg[0:n] + "\n    " +  msg[(n + 1):len(msg)]
    return msg
    '''

'''
# Given a message_id, return its index in data['messages']
def get_message_index(message_id):
    data = retrieve_data()
    i = 0
    while i < len(data['messages']):
        if data['messages']['message_id'] = 
'''


###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################


def message_send_v2(token, channel_id, message):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError(description="The given token is not valid")

    # Check to see if the message is too long
    if len(message) > 1000:
        raise InputError(description="The message exceeds 1000 characters")
    
    # Check to see if the given user (from token) is actully in the given channel
    user_id = auth_decode_token(token)
    if user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError(description=\
            "The user corresponding to the given token is not in the channel")


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
        'dm_id': -1,
        'is_removed': False,
        'was_shared': False,
    }

    # Append our dictionaries to their appropriate lists
    data['channels'][channel_id]['messages'].append(channel_message_dictionary)
    data['messages'].append(message_dictionary)
    #f = open("demofile3.txt", "w")
    #f.write(data)

    # Create notification if someone is tagged
    tag = re.search("^@.* ", message)
    if tag != None:
        tag = tag[1:-1]
        tagged = 0

        # Search for the tagged user within all_members and get their auth_id
        for member in data['channels'][channel_id]['all_members']:
            if (tag == data['users'][member]['handle_str']):
                tagged = member
        
        notification = {
        'channel_id' : channel_id,
        'dm_id' : -1,
        ('notification_message' : (str(data['users'][user_id]['handle_str'])
        + " tagged you in " + str(data['channels'][channel_id]['name']))
        + ":" + str(message[0:20]))
        }
        # Make sure notification list is len 20
        if len(data['users'][tagged]['notifications']) == 20:
            data['users'][tagged]['notifications'].pop(0)
        # Append new notification to end of list
        data['users'][tagged]['notifications'].append(notification)

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
                raise InputError(description="Message (based on id) no longer exists")
    
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
        raise AccessError(description=\
            "User is not dreams owner or channel owner and did not send the message")

    for msg in data['messages']:
        if msg['message_id'] == message_id:
            msg['is_removed'] = True

    return {
    }

def message_edit_v2(token, message_id, message):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check if the message_id given is already deleted
    for message_dict in data['messages']:
        if message_dict['message_id'] == message_id:
            if message_dict['is_removed'] == True:
                raise InputError(description="Message (based on id) no longer exists")

    # Check if the message is within the character limits
    if len(message) > 1000:
        raise InputError(description="The message exceeds 1000 characters")


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
        raise AccessError(description=\
            "User is not dreams owner or channel owner and did not send the message")
    

    # Remove the message if the new message is an empty string
    if message == "":
        message_remove_v2(token, message_id)
    
    # Otherwise, update the message in both data['messages'] and the channel
    for msg in data['messages']:
        if msg['message_id'] == message_id:
            ch_id = msg['channel_id']
            msg['message'] = message
    for ch_msg in data['channels'][ch_id]['messages']:
        if ch_msg['message_id'] == message_id:
            ch_msg['message'] = message

    return {
    }



def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    data = retrieve_data()
    u_id = auth_decode_token(token)
    og_message = get_message(og_message_id)

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError(description="The given token is not valid")

    # Check if the user is actually in the channel/dm they are trying to share to
    if channel_id != -1 and u_id not in data['channels'][channel_id]['all_members']:
        raise AccessError(description=\
            "User is not in the channel that they are trying to share to")
    if dm_id != -1 and u_id not in data['channels'][dm_id]['all_members']:
        raise AccessError(description=\
            "User is not in the channel that they are trying to share to")

    if not get_share_status(og_message_id):
        shared_message = message + '\n\n"""\n' + og_message + '\n"""'
    else:
        shared_message = message + '\n\n"""\n' + tab_given_message(og_message) + '\n"""'

    if channel_id != -1:
        shared_message_id = message_send_v2(token, channel_id, shared_message)['message_id']
        data['messages'][len(data['messages']) - 1]['was_shared'] = True
    #else:
        #shared_message_id = message_senddm_v1(token, dm_id, shared_message)['message_id']

    return {'shared_message_id': shared_message_id}


def message_senddm_v1(token, dm_id, message):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError(description="The given token is not valid")

    # Check to see if the message is too long
    if len(message) > 1000:
        raise InputError(description="The message exceeds 1000 characters")
    
    # Check to see if the given user (from token) is actully in the given dm
    user_id = auth_decode_token(token)
    if user_id not in data['dms'][dm_id]['members']:
        raise AccessError(description=\
            "The user corresponding to the given token is not in the dm")

    # Creating a unique id for our message_id
    unique_message_id = int(uuid4())
    # Creating a timestamp for our time_created key for our messages dictionary
    # which is based on unix time (epoch/POSIX time)
    time_created_timestamp = round(datetime.now().timestamp())

    # Create a dictionary which we will append to our messages list in our dm
    dm_message_dictionary = {
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
        'channel_id': -1,
        'dm_id': dm_id,
        'is_removed': False,
        'was_shared': False,
    }

    # Append our dictionaries to their appropriate lists
    data['dms'][dm_id]['messages'].append(dm_message_dictionary)
    data['messages'].append(message_dictionary)
    #f = open("demofile3.txt", "w")
    #f.write(data)

    return {
        'message_id': unique_message_id
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
