from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_token_decode

def message_send_v2(token, channel_id, message):
    data = retrieve_data()

    # Check to see if token is valid
    if not auth_token_ok(token):
        raise AccessError("The given token is not valid")

    # Check to see if the message is too long
    if len(message) > 1000:
        raise InputError("The message exceeds 1000 characters")
    
    # Check to see if the given user (from token) is actully in the given channel
    user_id = auth_decode_token(token)
    if user_id not in data['channels'][channel_id]['all_members']:
        raise AccessError("The user corresponding to the given token is not in the channel")

    


    return {
        'message_id': 1,
    }

def message_remove_v1(token, message_id):
    return {
    }

def message_edit_v2(token, message_id, message):
    return {
    }