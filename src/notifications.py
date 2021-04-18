# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from src.data import data, retrieve_data
from src.auth import auth_token_ok, auth_decode_token

def notifications_get_v1(token):
    '''
    BRIEF DESCRIPTION
    Accesses the 20 most recent notifications of a user
    
    Arguments:
        token (int) - The login session of the person accessing their notifications that were triggered by other functions

    Exceptions:
        InputError  - N/A
        AccessError - N/A
        
    Return value:
        notifications (list of notification data structures) - A list of notifications that the user has recieved
    '''
    # Make sure user is valid
    if not auth_token_ok(token):
        raise AccessError(description="The given token is not valid")
        
    data = retrieve_data()
    user_id = auth_decode_token(token)

    return {'notifications': data['users'][user_id]['notifications']}
