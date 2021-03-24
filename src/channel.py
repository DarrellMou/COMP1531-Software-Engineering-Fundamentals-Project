from src.data import data, retrieve_data
from src.error import AccessError, InputError
#from data import data, retrieve_data
#from error import AccessError, InputError

# Invites a user (with user id u_id) to join a channel with ID channel_id
# Once invited the user is added to the channel immediately
def channel_invite_v1(auth_user_id, channel_id, u_id):
    data = retrieve_data()

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError

    # Checks if user exists
    if u_id not in data['users']: raise InputError

    # Checks if the auth_user is in channel
    if auth_user_id not in data['channels'][channel_id]['all_members']: raise AccessError

    # Appends new user to given channel
    # Assume no duplicate entries allowed
    # Assume no inviting themselves
    # Assume inviting people outside channel only
    # if not any(user == u_id for user in data['channels'][channel_id]['all_members']):
    data['channels'][channel_id]['all_members'].append(u_id)

    return {}

# Given a Channel with ID channel_id that the authorised user is part of
# Provides basic details about the channel
def channel_details_v1(auth_user_id, channel_id):

    data = retrieve_data()

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError

    # Checks if the auth_user is in channel
    if auth_user_id not in data['channels'][channel_id]['all_members']: raise AccessError

    # Creates list with necessary data
    name = data['channels'][channel_id]['name']
    owners = data['channels'][channel_id]['owner_members']
    members = data['channels'][channel_id]['all_members']

    # Create list to return
    details_dict = {
        'name' : name,
        'owner_members' : [],
        'all_members' : []
    }

    # Create temporary list for owner members
    tmp_list = []
    for owner in owners:
        tmp_dict = {
            'u_id' : owner,
            'name_first' : data['users'][owner]['name_first'],
            'name_last' : data['users'][owner]['name_last']
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
            'name_first' : data['users'][member]['name_first'],
            'name_last' : data['users'][member]['name_last']
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
def channel_messages_v1(auth_user_id, channel_id, start):
    data = retrieve_data()
    # Check to see if the given channel_id is a valid channel
    if channel_id not in data['channels']:
        raise InputError("Channel id is not valid")
    # Check to see if the given user is actully in the given channel
    elif auth_user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError("The user is not in the channel")
    
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
        if user_id in data['channels'][channel_id]['all_members']:
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
        if (data['channels'][channel_id]['is_public']):
            #Add user to all_members pool in channel
            data['channels'][channel_id]['all_members'].append(auth_user_id)
        else: raise AccessError

    return {}

# Second version of channel_join that requires authentic token
def channel_join_v2(token, channel_id):
    user_id = auth_decode_token(token)
    return channel_join_v1(user_id, channel_id)

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError
    
    # If the target user is already an owner_member of the channel, raise access error
    if u_id in data['channels'][channel_id]['owner_members']: raise InputError

    # If the commanding user is not an owner or dreams owner
    if user_id not in data['channels'][channel_id]['owner_members'] and
    data['users'][user_id]['permission_id'] != 1: raise AccessError

    # All error checks passed, continue on to add owner
    data['channels'][channel_id]['owner_members'].append(u_id)
    # If added owner is not already a member, add to members list
    if user_id not in data['channels'][channel_id]['members']:
        data['channels'][channel_id]['members'].append(u_id)
    
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Checks if given channel_id is valid
    if channel_id not in data['channels']: raise InputError
    
    # If the target user is not an owner_member of the channel, raise access error
    if u_id not in data['channels'][channel_id]['owner_members']: raise InputError

    # If the target user is the only owner, raise access error
    if len(data['channels'][channel_id]['owner_members']) == 1: raise InputError

    # If the commanding user is not an owner or dreams owner
    if user_id not in data['channels'][channel_id]['owner_members'] and
    data['users'][user_id]['permission_id'] != 1: raise AccessError

    # All error checks passed, continue on to remove owner
    data['channels'][channel_id]['owner_members'].remove(u_id)

    return {
    }
