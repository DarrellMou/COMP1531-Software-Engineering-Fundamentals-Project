# PROJECT-BACKEND: Team Echo
# Written by Winston Lin

from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token, auth_email_format

import requests
import imgspy
from PIL import Image
import os

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
        return {'user' :
                    {
                    'name_first': "Removed",
                    'name_last' : "user"
                    }
               }

    return  {'user' :
                {
                'u_id'         : u_id,
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

    usersList = []

    for u_id in data['users'].keys():
        userDict = {
            'u_id'         : u_id,
            'email'        : data['users'].get(u_id)['email'],
            'name_first'   : data['users'].get(u_id)['name_first'],
            'name_last'    : data['users'].get(u_id)['name_last'],
            'handle_str'   : data['users'].get(u_id)['handle_str']
        }
        usersList.append(userDict)

    return {'users' : usersList}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    BRIEF DESCRIPTION
    Given a URL of an image on the internet, 
    crops the image within bounds (x_start, y_start) and (x_end, y_end). 
    Position (0,0) is the top left.

    Arguments:
        token   (string)        - authenticated user setting their name
        img_url (string)        - url of the image on internet
        x_start (integer)       - starting x value of wanted area after cropping
        y_start (integer)       - starting y value of wanted area after cropping
        x_end   (integer)       - ending x value of wanted area after cropping
        xy_end  (integer)       - ending y value of wanted area after cropping
        
    Exceptions:
        InputError - img_url returns an HTTP status other than 200.
        InputError - any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
        InputError - Image uploaded is not a JPG.

    Returns:
        Returns a an empty dictionary
    '''
    
    if not auth_token_ok(token):
        return {}
    
    # check availability 
    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError
    
    # check photo type 
    img_info = imgspy.info(img_url)
    if img_info['type'] != "jpg":
        raise InputError
    
    # choose a name for the photo file
    img_name = str(auth_decode_token(token)) + '.jpg'
    
    f = open(img_name, 'wb')
    f.write(response.content)
    f.close()
    
    img = Image.open(img_name)
    # check for boundary overreach 
    if x_start < 0 or y_start < 0 or x_end > img.size[0] or y_end > img.size[1]:
        os.remove(img_name)
        raise InputError
    
    img_cropped = img.crop((x_start, y_start, x_end, y_end))
    
    os.remove(img_name)
    img_cropped.save(img_name)
    
    return {}
    
    