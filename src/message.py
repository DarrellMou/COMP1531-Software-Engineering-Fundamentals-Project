from src.data import data, retrieve_data
from src.error import AccessError, InputError
from src.auth import auth_token_ok, auth_decode_token
from uuid import uuid4
from datetime import datetime


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


    # Creating a unique id for our message_id. The chances of uuid4 returning
    # the same time is infinitesimally small.
    # ASSUMPTION: int(uuid4()) will never reproduce the same id
    unique_message_id = int(uuid4())
    # Creating a timestamp for our time_created key for our messages dictionary
    # which is based on unix time (epoch/POSIX time)
    time_created_timestamp = round(datetime.now().timestamp())

    # Create a dictionary which we will append to our messages list in our channel
    message_dictionary = {
        'message_id': unique_message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_created_timestamp,
    }

    # Append our message dictionary to the messages list
    data['channels'][channel_id]['messages'].append(message_dictionary)

    return {
        'message_id': unique_message_id
    }

def message_remove_v1(token, message_id):
    return {
    }

def message_edit_v2(token, message_id, message):
    return {
    }