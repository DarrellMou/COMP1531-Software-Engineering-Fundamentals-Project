
from src.data import data, retrieve_data
from src.error import AccessError, InputError

from src.auth import auth_token_ok, auth_decode_token

import uuid
'''
from data import data, retrieve_data, reset_data
from error import AccessError, InputError

from auth import auth_token_ok, auth_decode_token, auth_register_v1
from message import message_senddm_v1
'''
# Creates dm given list of users
def dm_create_v1(token, u_ids):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if users in u_ids exists
    for u_id in u_ids:
        if u_id not in data['users']: raise InputError

    # Create temporary list for dm members
    users_list = []
    users_list.append(auth_user_id)

    # Create variable to make dm name by combining handle_str(s) of given users
    dm_name = data['users'][auth_user_id]['handle_str'] + ', '
    for u_id in u_ids:
        if u_id == u_ids[-1]:
            dm_name += data['users'][u_ids[-1]]['handle_str']
        else:
            dm_name += data['users'][u_id]['handle_str'] + ', '
        users_list.append(u_id)

    dm_id = int(uuid.uuid1())
    # Add new dm to dms data
    data['dms'][dm_id] = {
        'name': dm_name,
        'members': users_list,
        'messages': []
    }   

    return {'dm_id': dm_id, 'dm_name': dm_name}

# Returns details of given dm
def dm_details_v1(token, dm_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    members = data['dms'][dm_id]['members']

    # Create temporary list for dm members
    tmp_list = []
    for member in members:
        tmp_dict = {
            'u_id' : member,
            'name_first' : data['users'][member]['name_first'],
            'name_last' : data['users'][member]['name_last']
        }
        tmp_list.append(tmp_dict)

    # Create list to return
    details_dict = {
        'name' : data['dms'][dm_id]['name'],
        'members': tmp_list
    }

    return details_dict

# Returns list of dms that user is a member of
def dm_list_v1(token):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Make list for dms
    dm_list = []

    # Make dict to append to dm_list
    for dm in data['dms']:
        if auth_user_id in data['dms'][dm]['members']:
            dm_dict = {
                'dm_id': dm,
                'name': data['dms'][dm]['name']
            }
            dm_list.append(dm_dict)

    return {'dms': dm_list}

# Returns nothing, removes dm from data
def dm_remove_v1(token, dm_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user is the creator of dm
    if auth_user_id != data['dms'][dm_id]['members'][0]: raise AccessError

    # Deletes dm from data
    del data['dms'][dm_id]

    return {}

# Inviting a user to an existing dm
def dm_invite_v1(token, dm_id, u_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user exists
    if u_id not in data['users']: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    data['dms'][dm_id]['members'].append(u_id)

    return {}

# Given a DM ID, the user is removed as a member of this DM
def dm_leave_v1(token, dm_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    data['dms'][dm_id]['members'].remove(auth_user_id)

    return {}


def dm_messages_v1(token, dm_id, start):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check to see if the given dm_id is a valid dm
    if dm_id not in data['dms']:
        raise InputError("dm_id is not valid")

    # Check to see if the given user (token) is actully in the given dm
    user_id = auth_decode_token(token)
    if user_id not in data['dms'][dm_id]['members']:
        raise AccessError("The user corresponding to the given token is not in the dm")

    
    # Check to see if the given start value is larger than the number of
    # messages in the given dm
    num_messages = len(data['dms'][dm_id]['messages'])
    if start > num_messages:
        raise InputError("Inputted starting index is larger than the current number of messages in the dm")

    # Initialise our message dictionary which we will be returning
    messages_dict = {
        'messages': [],
        'start': start,
        'end': 0
    }

    # Get our current dm
    dm = data['dms'][dm_id]
    # ASSUMPTION: messages are APPENDED to our message list within the dm
    # key of our data dictionary
    # Reverse the order of the dm messages so the most recent message
    # appears in index 0 and the least recent in the last index
    messages_list = dm['messages'][::-1]


    # Loop through our list and return up to 50 of the most recent messages
    # starting our index with the given start
    count = 0
    for message in messages_list:
        # Check to see if the message has been removed and if it has then
        # skip it
        if is_message_removed(message['message_id']):
            continue
        
        # Starting off at the start index, add up to 50 messages to the list
        # in the messages dictionary
        if count >= start and count < (start + 50):
            messages_dict['messages'].append(message)
        count += 1

    # If 50 messages were added, then the most recent message is going to be
    # returned and as per the spec, 'end' should return -1. Otherwise, end
    # should return (start + 50)
    if len(messages_dict['messages']) != 50:
        messages_dict['end'] = -1
    # If the number of messages in the dm minus the given start divided
    # by 50 returns 1, this mean the most recent message has been returned
    elif (num_messages - start) / 50 == 1:
        messages_dict['end'] = -1
    else:
        messages_dict['end'] = start + 50

    return messages_dict




###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################

# A function to check whether a message with given message_id is removed
def is_message_removed(msg_id):
    data = retrieve_data()
    count = 0
    while count < len(data['messages']):
        if data['messages'][count]['message_id'] == msg_id:
            if data['messages'][count]['is_removed']:
                return True
        count += 1
    return False
