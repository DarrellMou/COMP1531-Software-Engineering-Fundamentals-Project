from src.error import InputError 
from src.data import retrieve_data
'''
# For testing
from error import InputError 
from data import retrieve_data
'''
import re
import itertools
import uuid

# checks if email address has valid format, if so returns true
def auth_email_format(email):
    pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    
    return bool(re.match(pattern, email))

# Given a registered users' email and password
# Returns their `auth_user_id` value
def auth_login_v1(email, password):  

    data = retrieve_data()

    # Checks for invalid email format
    if auth_email_format(email) == False:
        raise InputError
    
    # Checks for existing email and password
    for key_it in data['users'].keys():
        data_email = data['users'][key_it]['email']
        data_password = data['users'][key_it]['password']
        # Checks for matching email and password
        if email == data_email and password == data_password:
            return {'auth_user_id' : key_it}        
    raise InputError



# Given a user's first and last name, email address, and password
# create a new account for them and return a new `auth_user_id`.
def auth_register_v1(email, password, name_first, name_last):

    data = retrieve_data()
    # Checks for invalid email format
    if auth_email_format(email) == False:
        raise InputError
    # Checks for an already existing email address
    elif any(email == data['users'][key_it]['email']\
    for key_it in data['users']):
        raise InputError
    # Ensuring password is over 5 characters
    elif len(password) < 6:
        raise InputError
    # Checks that name_first is not between 1 and 50 characters inclusively in length
    elif len(name_first) > 50 or len(name_first) < 1\
        or len(name_last) > 50 or len(name_last) < 1:
        raise InputError
    
    # Generate handle and add to data['users'][auth_user_id]
    new_handle = name_first.lower() + name_last.lower()
    # Limit handle to first 20 characters if exceeding 20 characters
    if len(new_handle) > 20:
        new_handle = new_handle[0:20]

    # Randomly generate a unique auth_user_id
    new_auth_user_id = int(uuid.uuid4())


    data['users'][new_auth_user_id] = {
        'name_first' : name_first, 
        'name_last' : name_last, 
        'email' : email,
        'password' : password,
        'handle_str' : '',
    }

    # Check to see if the handle is unique
    if any(new_handle == data['users'][user]['handle_str']\
    for user in data['users']):
        # If the handle already exists, append with a number starting from 0
        for epilogue in itertools.count(0, 1):
            if(not any((new_handle + str(epilogue)) ==\
            data['users'][user]['handle_str'] for user in data['users'])):
                data['users'][new_auth_user_id]['handle_str'] =\
                new_handle + str(epilogue)
                return {'auth_user_id' : new_auth_user_id}
    else:   # unique handle, add straght away 
        data['users'][new_auth_user_id]['handle_str'] = new_handle
        return {'auth_user_id' : new_auth_user_id}
