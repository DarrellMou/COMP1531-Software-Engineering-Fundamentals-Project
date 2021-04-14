# PROJECT-BACKEND: Team Echo
# Written by Winston Lin

from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token, auth_email_format

###############################################################################
'''       A user's profile is set when he registers, in auth_register       '''
###############################################################################

def user_profile_v2(token, u_id):
    '''
    BRIEF DESCRIPTION
    For a valid user, returns information about their user_id, email, first name, last name, and handle

    Arguments:
        token (string)   - authenticated user calling function
        u_id (int)       - the user whose profile will be retrieved

    Exceptions:
        InputError  - Occurs when the user with u_id is not a valid user
        AccessError - Occurs when the token is invalid

    Returns:
        Returns a dictionary about their user_id, email, first name, last name, and handle
    '''

    data = retrieve_data()

    if not auth_token_ok(token):
        raise AccessError('invalid token')

    if not any(x == u_id for x in data['users'].keys()):
        raise InputError('User does not exist')

    userDict = data['users'][u_id]

    if data['users'][u_id]['is_removed']:
        return {'user' : {
                    'name_first': "Removed",
                    'name_last' : "user"
                    }
                }

    return {'user' : {
                'auth_user_id' : u_id,
                'email'        : userDict['email'],
                'name_first'   : userDict['name_first'],
                'name_last'    : userDict['name_last'],
                'handle_str'   : userDict['handle_str']
                }
           }

def user_profile_setname_v2(token, name_first, name_last):
    '''
    BRIEF DESCRIPTION
    Update the authorised user's first and last name

    Arguments:
        token (string)           - authenticated user setting their name
        name_first (string)      - user's first name
        name_last (string)       - user's last name

    Exceptions:
        InputError  - Occurs when the name_first is not between 1 and 50 characters inclusively in length
        InputError  - Occurs when the name_last is not between 1 and 50 characters inclusively in length
        AccessError - Occurs when the token is invalid

    Returns:
        n/a
    '''

    data = retrieve_data()

    if len(name_first) not in range(1, 50) or len(name_last) not in range(1, 50):
        raise InputError('invalid name length')

    if not auth_token_ok(token):
        raise InputError('invalid token')

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['name_last'] = name_last
    data['users'][auth_user_id]['name_first'] = name_first

    return {}


def user_profile_setemail_v2(token, new_email):
    '''
    BRIEF DESCRIPTION
    Update the authorised user's email address

    Arguments:
        token (string)     - authenticated user setting their email
        new_email (string) - user's new email

    Exceptions:
        InputError  - Occurs when the email entered is not a valid email
        InputError  - Occurs when the email address is already being used by another user
        AccessError - Occurs when the token is invalid

    Returns:
        n/a
    '''

    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    # email format check 
    if not auth_email_format(new_email):
        raise InputError('invalid email format')

    # if email already used by another user 
    if any(user['email'] == new_email for user in data['users'].values()):
        raise InputError('email already exists') 

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['email'] = new_email

    return {}


def user_profile_sethandle_v2(token, new_handle):
    '''
    BRIEF DESCRIPTION
    Update the authorised user's handle (i.e. display name)

    Arguments:
        token (string)          - authenticated user setting their handle
        handle_str (string)     - user's new handle

    Exceptions:
        InputError  - Occurs when the handle_str is not between 3 and 20 characters inclusive
        InputError  - Occurs when the handle is already being used by another user
        AccessError - Occurs when the token is invalid

    Returns:
        n/a
    '''

    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    # if email already used by another user 
    if any(user['handle_str'] == new_handle for user in data['users'].values()):
        raise InputError('handle already exists') 
           
    # check handle format
    if len(new_handle) not in range(3, 20):
        raise InputError('invalid handle length')

    auth_user_id = auth_decode_token(token)

    data['users'][auth_user_id]['handle_str'] = new_handle

    return {}


def users_all_v1(token):
    '''
    BRIEF DESCRIPTION
    Returns a list of all users and their associated details

    Arguments:
        token (string)          - authenticated user setting their name

    Exceptions:
        AccessError - Occurs when the token is invalid

    Returns:
        Returns a list of all users and their associated details
    '''

    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')

    return data['users']


# Function to return the statistics of a user
def user_stats_v1_tests(token):
    data = retrieve_data()

    # Make sure user is valid
    if not auth_token_ok(token):
        raise AccessError(description="The given token is not valid")

    user_id = auth_decode_token(token)

    # Token is valid, continue to gather statistics about this user

    # Channels joined statistic
    channel_num = 0
    total_ch = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member == user_id:
                channel_num += 1

        
        total_ch += 1

    # Dms joined statistic
    dm_num = 0
    total_dm = 0
    for dm in data['dms']:
        for member in dm['members']:
            if member == user_id:
                dm_num += 1
        total_dm += 1

    # Messages sent statistic
    msg_num = 0
    total_msg = 0
    for msg in data['messages']:
        if msg['u_id'] == user_id:
            msg_num += 1
        total_msg += 1

    # Calculate involvement
    activity = channel_num + dm_num + msg_num
    server_act = total_ch + total_dm + total_msg
    involvement = 0

    if not activity == 0:
        involvement = (activity / server_act)

    # Create dict for stats
    stat_dict = {
        'num_channels_joined': channel_num,
        'num_dms_joined': dm_num,
        'num_msgs_sent': msg_num,
        'involvement': involvement,
    }

    return stat_dict