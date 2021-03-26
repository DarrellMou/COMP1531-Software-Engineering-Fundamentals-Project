"""
A user's profile is set when he registers, in auth_register
"""

def user_profile_v1(token, u_id):
    return {
        'user': {
            'auth_user_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname_v1(token, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(token, email):
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    return {
    }