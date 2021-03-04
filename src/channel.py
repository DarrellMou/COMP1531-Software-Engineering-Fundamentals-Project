from src.data import data
from src.error import AccessError, InputError

###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################


# Helper function to determine if a channel is a valid channel
def is_valid_channel_id(channel_id):
    global data
    
    for channel in data['channels']:
        if int(channel_id) == channel['channel_id']:
            return True
    
    return False


# Helper function to determine if an authorised user is a member of the channel
def is_valid_user_in_channel(user_id, channel_id):
    # Get the channel from the given channel id
    global data
    channel = data['channels'][channel_id - 1] # Assuming channel_id starts off from 1 intead of 0

    for user in channel['all_members']:
        if int(user_id) == user['auth_user_id']:
            return True
    
    return False


# Helper function to determine the number of messages in a given channel
def num_messages(channel_id):
    # Get the channel from the given channel id
    global data
    channel = data['channels'][int(channel_id) - 1]

    count = 0
    for message in channel['messages']:
        count += 1
    
    return count


###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################


###############################################################################
#                               CHANNEL FUNCTIONS                             #
###############################################################################


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    # Check to see if the given channel_id is a valid channel
    if not is_valid_channel_id(channel_id):
        raise InputError("Channel id is not valid")
    # Check to see if the given user is actully in the given channel
    elif not is_valid_user_in_channel(auth_user_id, channel_id):
        raise AccessError("The user is not in the channel")
    
    # Check to see if the given start value is larger than the number of
    # messages in the given channel
    if start > num_messages(channel_id):
        raise InputError("Inputted starting index is larger than the current number of messages in the channel")
    
    # Check to see if the given start is negative
    if start < 0:
        raise InputError("Inputted starting index is negative")

    # Initialise our message dictionary which we will be returning
    messages_dict = {
        'messages': [],
        'start': start,
        'end': 0
    }

    # Get our current channel
    global data
    channel = data['channels'][channel_id - 1]
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
    if count < start + 50:
        messages_dict['end'] = -1
    else:
        messages_dict['end'] = start + 50


    return messages_dict

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }