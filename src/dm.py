# PROJECT-BACKEND: Team Echo
# Written by Darrell Mounarath (dm_create, dm_details, dm_list, dm_remove, dm_invite, dm_leave), Brendan Ye (dm_messages)

from src.data import retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token

import uuid

def dm_create_v1(token, u_ids):
    '''
    Creates a DM with a name containing users handle strings

    Arguments:
        token (string) - token belonging to caller
        u_ids (list)   - auth_user_ids belonging to users joining DM

    Exceptions:
        AccessError - u_id in u_ids does not refer to a valid user
        AccessError - invalid token

    Returns:
        Returns dm_id and dm_name
    '''

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if users in u_ids exists
    for u_id in u_ids:
        if u_id not in data['users'] or data['users'][u_id]['is_removed'] == True: raise InputError

    # Create users list for dm members
    u_ids.insert(0, auth_user_id)

    # Create variable to make dm name by combining handle_str(s) of given users
    handle_strs = [data['users'][u_id]['handle_str'] for u_id in u_ids]
    dm_name = ''
    for handle_str in sorted(handle_strs):
        dm_name += handle_str if handle_str == handle_strs[-1] else (handle_str + ', ')

    dm_id = int(uuid.uuid1())
    # Add new dm to dms data
    data['dms'][dm_id] = {
        'name': dm_name,
        'members': u_ids,
        'messages': []
    }

    # Create notification for users added to dm's
    notification = {
        'channel_id' : -1,
        'dm_id' : dm_id,
        'notification_message' : (str(data['users'][auth_user_id]['handle_str']) + " added you to " + dm_name)
    }
    for u_id in u_ids:
        # Make sure notification list is len 20
        if len(data['users'][u_id]['notifications']) > 19:
            data['users'][u_id]['notifications'].pop(0)
        
        # Append new notification to end of list
        data['users'][u_id]['notifications'].append(notification)


    return {'dm_id': dm_id, 'dm_name': dm_name}
    
# Returns details of given dm
def dm_details_v1(token, dm_id):
    '''
    Provides basic details about the given DM
    
    Arguments:
        token (string) - token belonging to caller
        dm_id (int)    - id belonging to DM
    
    Exceptions:
        InputError  - dm_id is not a valid DM
        AccessError - Authorised user is not a member of this DM with dm_id
        AccessError - invalid token
    
    Return value:
        Returns DM details 
    '''

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

def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of
    
    Arguments:
        token (string) - token belonging to caller
    
    Exceptions:
        AccessError - invalid token
    
    Return value:
        Returns list of DMs
    '''

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

def dm_remove_v1(token, dm_id):
    '''
    Removes given DM from data
    
    Arguments:
        token (string) - token belonging to caller
    
    Exceptions:
        AccessError - invalid token
    
    Return value:
        Returns nothing
    '''

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

def dm_invite_v1(token, dm_id, u_id):
    '''
    Invites a user to a DM, invited user immediately joins DM
    
    Arguments:
        token (string) - token belonging to inviter
        dm_id (int)    - id belonging to DM
        u_id (int)     - the auth_user_id of the invitee
    
    Exceptions:
        InputError  - dm_id does not refer to an existing DM
        InputError  - u_id does not refer to a valid user
        AccessError - the authorised user is not already a member of the DM
        AccessError - invalid token
    
    Return value:
        Returns nothing
    '''

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if user exists
    if u_id not in data['users'] or data['users'][u_id]['is_removed'] == True: raise InputError

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    data['dms'][dm_id]['members'].append(u_id)

    # Create notification for added user
    notification = {
        'channel_id' : -1,
        'dm_id' : dm_id,
        'notification_message' : (str(data['users'][auth_user_id]['handle_str']) + " added you to " + str(data['dms'][dm_id]['name']))
    }
    # Make sure notification list is len 20
    if len(data['users'][u_id]['notifications']) > 19:
        data['users'][u_id]['notifications'].pop(0)
    # Append new notification to end of list
    data['users'][u_id]['notifications'].append(notification)

    return {}

def dm_leave_v1(token, dm_id):
    '''
    Given a dm_id, the user is removed as a member of this DM
    
    Arguments:
        token (string) - token belonging to caller
        dm_id (int)    - id belonging to DM
    
    Exceptions:
        InputError  - dm_id is not a valid DM
        AccessError - Authorised user is not a member of DM with dm_id
        AccessError - invalid token
    
    Return value:
        Returns nothing
    '''

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
    '''
    BRIEF DESCRIPTION
    Given a DM with ID dm_id that the authorised user is part of, return up to 
    50 messages between index "start" and "start + 50". Message with index 0 is the most 
    recent message in the DM. This function returns a new index "end" which is the 
    value of "start + 50", or, if this function has returned the least recent messages in 
    the DM, returns -1 in "end" to indicate there are no more messages to load after 
    this return.

    Arguments:
        token (string)  - authenticated user view messages of a DM they are in
        dm_id (integer) - DM that the user wants to view messages in   
        start (integer) - the position to start the load of messages

    Exceptions:
        InputError  - dm_id is not a valid DM
        InputError  - start is greater than the total number of messages in the DM
        AccessError - Authorised user is not a member of DM with dm_id

    Returns:
        Returns messages in the DM
        Returns the start index of messages returned from DM
        Returns the end index of messages returned from DM
    '''

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
