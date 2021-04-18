# PROJECT-BACKEND: Team Echo
# Written by Kellen (everything else), Brendan Ye (channel_messages), Darrell (channel_invite, channel_details, channel_leave)

from src.data import retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token

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

###############################################################################

def channel_invite_v2(token, channel_id, u_id):
    '''
    BRIEF DESCRIPTION
    Invites a user to a channel, invited user immediately joins channel
    
    Arguments:
        token (string)   - token belonging to inviter
        channel_id (int) - id belonging to channel
        u_id (int)       - the auth_user_id of the invitee
    
    Exceptions:
        InputError  - channel_id does not refer to a valid channel
        InputError  - u_id does not refer to a valid user
        AccessError - the authorised user is not already a member of the channel
        AccessError - invalid token
    
    Return value:
        Returns nothing
    '''

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError

    # Checks if u_id is valid
    if u_id not in data['users']: raise InputError

    # Checks if the auth_user is in channel
    if auth_user_id not in data['channels'][channel_id]['all_members']: raise AccessError

    # Checks if u_id exists
    if u_id not in data['users'] or data['users'][u_id]['is_removed'] == True: raise InputError

    # Appends new user to given channel
    # Assume no duplicate entries allowed
    # Assume no inviting themselves
    # Assume inviting people outside channel only
    # if not any(user == u_id for user in data['channels'][channel_id]['all_members']):
    if data['users'][u_id]['permission_id'] == 1:
        data['channels'][channel_id]['owner_members'].append(u_id)
    data['channels'][channel_id]['all_members'].append(u_id)
    # Create notification for added user
    data['users'][u_id]['notifications'].append({
        'channel_id' : channel_id,
        'dm_id' : -1,
        'notification_message' : (str(data['users'][auth_user_id]['handle_str']) + " added you to " + str(data['channels'][channel_id]['name']))
    })
    # Make sure notification list is len 20
    if len(data['users'][u_id]['notifications']) > 19:
        data['users'][u_id]['notifications'].pop(0)

    return {}

def channel_details_v2(token, channel_id):
    '''
    BRIEF DESCRIPTION
    Provides basic details about the given channel
    
    Arguments:
        token (string)   - token belonging to caller
        channel_id (int) - id belonging to channel
    
    Exceptions:
        InputError  - channel_id does not refer to a valid channel
        AccessError - Authorised user is not a member of channel with channel_id
        AccessError - invalid token
    
    Return value:
        Returns channel details 
    '''
    data = retrieve_data()
    
    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError 
    auth_user_id = auth_decode_token(token)

    # Checks if the auth_user is in channel
    if auth_user_id not in data['channels'][channel_id]['all_members']: raise AccessError("The user corresponding to the given token is not in the channel")

    # Creates list with necessary data
    name = data['channels'][channel_id]['name']
    is_public = data['channels'][channel_id]['is_public']
    owners = data['channels'][channel_id]['owner_members']
    members = data['channels'][channel_id]['all_members']

    # Create list to return
    details_dict = {
        'name' : name,
        'is_public' : is_public,
        'owner_members' : [],
        'all_members' : []
    }

    # Create temporary list for owner members
    tmp_list = []
    for owner in owners:
        tmp_dict = {
            'u_id' : owner,
            'email' : data['users'][owner]['email'],
            'name_first' : data['users'][owner]['name_first'],
            'name_last' : data['users'][owner]['name_last'],
            'handle_str' : data['users'][owner]['handle_str']
        }
        tmp_list.append(tmp_dict)

    # Assigns 'owner_members' key to tmp_list
    details_dict['owner_members'] = tmp_list

    # Create temporary list for all members
    tmp_list = []
    
    # Iterates through members in 'all_members', and appends to tmp_list
    for member in members:
        tmp_dict = {
            'u_id' : member,
            'email' : data['users'][member]['email'],
            'name_first' : data['users'][member]['name_first'],
            'name_last' : data['users'][member]['name_last'],
            'handle_str' : data['users'][member]['handle_str']
        }
        tmp_list.append(tmp_dict)
    
    # Assigns 'all_members' key to tmp_list
    details_dict['all_members'] = tmp_list

    return details_dict


# Given a valid channel_id, return up to 50 messages in the channel
# ASSUMPTION: Start IS NOT negative (originally I made it an input error but
# apparently you're not allowed to raise any input or access errors other than
# the ones listed in the spec, so its tests were removed altogether and was
# replaced by an assumption)
def channel_messages_v2(token, channel_id, start):
    '''
    BRIEF DESCRIPTION
    Given a Channel with ID channel_id that the authorised user is part of, return up to 
    50 messages between index "start" and "start + 50". Message with index 0 is the most 
    recent message in the channel. This function returns a new index "end" which is the 
    value of "start + 50", or, if this function has returned the least recent messages in 
    the channel, returns -1 in "end" to indicate there are no more messages to load after 
    this return.

    Arguments:
        token (string)       - authenticated user view messages of a channel they are in
        channel_id (integer) - channel that the user wants to view messages in   
        start (integer)      - the position to start the load of messages

    Exceptions:
        InputError  - Occurs when the channel id is not valid
        InputError  - Occurs when the start is greater than the total number of messages in the channel
        AccessError - Occurs when the authorised user is not a member of channel with channel_id

    Returns:
        Returns messages in the channel
        Returns the start index of messages returned from channel
        Returns the end index of messages returned from channel
    '''
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check to see if the given channel_id is a valid channel
    if channel_id not in data['channels']:
        raise InputError("Channel id is not valid")

    # Check to see if the given user (token) is actully in the given channel
    user_id = auth_decode_token(token)
    if user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError("The user corresponding to the given token is not in the channel")

    
    # Check to see if the given start value is larger than the number of
    # messages in the given channel
    num_messages = len(data['channels'][channel_id]['messages'])
    if start > num_messages:
        raise InputError("Inputted starting index is larger than the current number of messages in the channel")

    # Initialise our message dictionary which we will be returning
    messages_dict = {
        'messages': [],
        'start': start,
        'end': 0
    }

    # Get our current channel
    channel = data['channels'][channel_id]
    # ASSUMPTION: messages are APPENDED to our message list within the channel
    # key of our data dictionary
    # Reverse the order of the channel messages so the most recent message
    # appears in index 0 and the least recent in the last index
    messages_list = channel['messages'][::-1]


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
    # If the number of messages in the channel minus the given start divided
    # by 50 returns 1, this mean the most recent message has been returned
    elif (num_messages - start) / 50 == 1:
        messages_dict['end'] = -1
    else:
        messages_dict['end'] = start + 50

    return messages_dict

def channel_leave_v1(token, channel_id):
    '''
    BRIEF DESCRIPTION
    Given a channel ID, the user removed as a member of this channel. Their messages should remain in the channel

    Arguments:
        token (string)       - authenticated user to leave a channel
        channel_id (integer) - channel that the user wants to leave

    Exceptions:
        InputError  - Occurs when the channel ID is not a valid channel 
        AccessError - Occurs when the authorised user is not a member of channel with channel_id    

    Returns:
        n/a
    '''

    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError
    
    # If the auth_user is not a member of the channel, raise access error
    if user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError
    # auth_user is a member, proceed with removal
    else:
        # Remove user ID from all_members
        data['channels'][channel_id]['all_members'].remove(user_id)
        # Remove in owner_members if applicable as well
        if user_id in data['channels'][channel_id]['owner_members']:
            data['channels'][channel_id]['owner_members'].remove(user_id)
    
    return {
    }

# Function that allows a member to add themselves to a channel given that it is public
def channel_join_v1(auth_user_id, channel_id):
    data = retrieve_data()

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError

    # Checks if the auth_user is in channel, if not proceed, otherwise do nothing
    if auth_user_id not in data['channels'][channel_id]['all_members']:
        # Checks if channel is public, if true proceed, if false raise error
        if (data['channels'][channel_id]['is_public']) or data['users'][auth_user_id]['permission_id'] == 1:
            
            # If user is a global owner, user has owner permissions in every channel they join
            if data['users'][auth_user_id]['permission_id'] == 1:
                data['channels'][channel_id]['owner_members'].append(auth_user_id)
            
            # Add user to all_members pool in channel
            data['channels'][channel_id]['all_members'].append(auth_user_id)
        else: raise AccessError

    return {}


def channel_join_v2(token, channel_id):
    '''
    BRIEF DESCRIPTION
    Second version of channel_join that requires authentic token
    
    Arguments:
        token (int)      - The login session of the person joining the channel
        channel_id (int) - References the channel the user is joining
 
    Exceptions:
        InputError  - Occurs when channel ID is not a valid channel
        AccessError - Occurs when channel_id refers to a private channel and user is not dreams owner

    Return value:
        n/a
    '''
    user_id = auth_decode_token(token)
    return channel_join_v1(user_id, channel_id)

def channel_addowner_v1(token, channel_id, u_id):
    '''
    BRIEF DESCRIPTION
    A function that adds users as owners of a channel
    
    Arguments:
        token (int)      - The login session of the person adding owner to channel
        channel_id (int) - References the channel the user adding to
        u_id (int)       - The auth_user_id of the person being added as owner
    
    Exceptions:
        InputError  - Occurs when channel ID is not a valid channel or when u_id owner is already an owner of channel
        AccessError - Occurs when channel_id refers to a private channel and user is not dreams owner
    
    Returns:
        n/a
    '''

    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError
    
    # If the target user is already an owner_member of the channel, raise access error
    if u_id in data['channels'][channel_id]['owner_members']: raise InputError

    # If the commanding user is not an owner or dreams owner
    if (user_id not in data['channels'][channel_id]['owner_members'] and
    data['users'][user_id]['permission_id'] != 1): raise AccessError

    # All error checks passed, continue on to add owner
    data['channels'][channel_id]['owner_members'].append(u_id)
    # If not already in server, add on to all members
    if (u_id not in data['channels'][channel_id]['all_members']):
        data['channels'][channel_id]['all_members'].append(u_id)

    return {
    }


def channel_removeowner_v1(token, channel_id, u_id):
    '''
    BRIEF DESCRIPTION
    A function that removes users as owners of a channel
    
    Arguments:
        token (int)      - The login session of the person removing owner from channel
        channel_id (int) - References the channel the user removing from
        u_id (int)       - The auth_user_id of the person being removed as owner
    
    Exceptions:
        InputError  - Occurs when channel ID is not a valid channel or when u_id owner is not an owner of channel
        AccessError - Occurs when channel_id refers to a private channel and user is not dreams owner
    
    Returns:
        n/a
    '''

    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError
    
    # If the target user is not an owner_member of the channel, raise access error
    if u_id not in data['channels'][channel_id]['owner_members']: raise InputError

    # If the target user is the only owner, raise access error
    if len(data['channels'][channel_id]['owner_members']) == 1: raise InputError

    # If the commanding user is not an owner or dreams owner
    if (user_id not in data['channels'][channel_id]['owner_members'] and
    data['users'][user_id]['permission_id'] != 1): raise AccessError

    # All error checks passed, continue on to remove owner
    data['channels'][channel_id]['owner_members'].remove(u_id)

    return {
    }
