from src.error import InputError 
from src.data import retrieve_data
from src.auth import auth_token_ok, auth_decode_token

def clear_v1():

    data = retrieve_data()

    data = {
        "users" : {},
        "channels" : {}
    }
    
    return data

def search_v2(auth_user_id, query_str):
    
    data = retrieve_data()

    # InputError occurs when query_str is longer than 1000 characters
    if len(query_str) > 1000: raise InputError("Query cannot be longer than 1000 characters")

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Find channels/DMs user is part of and return a collection of messages
    collection_messages = []

    for channel in data['channels']:
        for member in data['channels'][channel]['all_members']:
            if member == auth_user_id:
                for message in data['channels'][channel]['messages']['message']:
                    # query_str is a substring of message 
                    if query_str in message:
                        collection_messages.append(message)
    
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if member == auth_user_id:
                for message in data['dm'][dm]['messages']['message']:
                    # query_str is a substring of message 
                    if query_str in message:
                        collection_messages.append(message)
    
    return collection_messages

def admin_user_remove_v1(token, u_id):

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid User")
    auth_user_id = auth_decode_token(token)

    # Check if u_id exists
    if u_id not in data['users']: raise InputError("Invalid User")

    # Checks if authorised user is an owner
    if data['users'][auth_user_id]['permission_id'] == 1: raise AccessError("Not an admin user")

    admin = 0
    # Checks if the user is the currently the only owner
    for permission in data['users'][auth_user_id][permission_id]:
        if permission = 2:
            admin += 1
    if admin < 1: raise InputError("The user is currently the only owner")

    # Replace channel message with 'Removed user'
    for channel in data['channels']:
        for member in data['channels'][channel]['all_members']:
            if member == auth_user_id:
                for message in data['channels'][channel]['messages']:
                    message['message'].replace(message['message'], 'Removed user')
                    message['is_removed'] == True

    # Replace dm message with 'Removed user'
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if member == auth_user_id:
                for message in data['dm'][dm]['messages']['message']:
                    message['message'].replace(message['message'], 'Removed user')
                    message['is_removed'] == True

    # Tell user/profile/v2 to have an if statement for is_removed and only show their name 'Removed user'
    for user in data['users']:
        if user == u_id:
            user['name_first'] : 'Removed user',
            user['is_removed'] == True

    return {}