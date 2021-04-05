# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

from src.error import InputError, AccessError 
from src.data import retrieve_data
from src.auth import auth_token_ok, auth_decode_token
import src.data
import json

def clear_v1():
    src.data.data = {
        "users" : {},
        "channels" : {},
        "dms" : {},
        "messages" : []
    }
    with open("data.json", "w") as FILE:
        json.dump(src.data.data, FILE)
    return {}

def search_v2(token, query_str):
    
    data = retrieve_data()

    # InputError occurs when query_str is longer than 1000 characters
    if len(query_str) > 1000: raise InputError("Query cannot be longer than 1000 characters")

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid token")
    auth_user_id = auth_decode_token(token)

    # Create a collection of messages
    collection_messages = []
    # Find channels user is part of and return a collection of messages
    for channel in data['channels']:
        for member in data['channels'][channel]['all_members']:
            if member == auth_user_id:
                for message in data['channels'][channel]['messages']:
                    # query_str is a substring of message 
                    if query_str in message['message']:
                        collection_messages.append(message['message'])
    # Find DMs user is part of and return a collection of messages
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if member == auth_user_id:
                for message in data['dms'][dm]['messages']:
                    # query_str is a substring of message 
                    if query_str in message['message']:
                        collection_messages.append(message['message'])
    
    return collection_messages


def admin_user_remove_v1(token, u_id):

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid token")
    user_id = auth_decode_token(token)

    # Check if u_id exists
    if u_id not in data['users'] or data['users'][u_id]['is_removed'] == True: raise InputError("This u_id does not exist")

    # Checks if authorised user is an owner
    if data['users'][user_id]['permission_id'] == 2: raise AccessError("Token is not an admin user")

    # Checks if the user is the currently the only owner
    admin_flag = 0
    only_owner = False
    for user in data['users']:
        if data['users'][user]['permission_id'] == 1:
            admin_flag += 1
            if user == u_id:
                only_owner = True
    if admin_flag == 1 and only_owner == True: raise InputError("Token is currently the only global owner")

    # Iterate through channels to identify which channels the user is in
    for channel in data['channels']:      
        # Remove user from the all_members list
        for member in data['channels'][channel]['all_members']:
            if u_id in data['channels'][channel]['all_members']:
                for message in data['channels'][channel]['messages']:
                    # Replace channel message with 'Removed user'
                    if message['u_id'] == u_id:
                        message['message'] = "Removed user"
                data['channels'][channel]['all_members'].remove(u_id)
        # Remove user from the owner_members list
        for member in data['channels'][channel]['owner_members']:
            if u_id in data['channels'][channel]['owner_members']:
                data['channels'][channel]['owner_members'].remove(u_id)
                break

    # Iterate through dms to identify which dms the user is in
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if u_id in data['dms'][dm]['members']:
                for message in data['dms'][dm]['messages']:
                    # Replace dm message with 'Removed user'
                    if message['u_id'] == u_id:
                        message['message'] = "Removed user" 
            # Remove user from the dm members list
            data['dms'][dm]['members'].remove(member)

    # Replace any messages from u_id with 'Removed user'
    for message in data['messages']:
        if message['u_id'] == u_id:
            message['message'] = "Removed user"
            break

    # Replace user name with 'Removed user'
    # Have user/profile/v2 to have an if statement for is_removed and only show their name 'Removed user'
    for user in data['users']:
        if user == u_id:
            data['users'][user]['is_removed'] = True
    
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid token")
    auth_user_id = auth_decode_token(token)

    # Check if u_id exists
    if u_id not in data['users'] or data['users'][u_id]['is_removed'] == True: raise InputError("This u_id does not exist")

    # Checks if authorised user is an owner
    if not data['users'][auth_user_id]['permission_id'] == 1: raise AccessError("Token is not an admin user")

    # Checks if permission_id refers to a value permission
    if not (permission_id == 1 or permission_id == 2): raise InputError("Not a value permission")

    # Checks if the user is the currently the only owner
    if permission_id == 2:
        admin_flag = 0
        for user in data['users']:
            if data['users'][user]['permission_id'] == 1:
                admin_flag += 1
        if admin_flag <= 1: raise InputError("The user is currently the only global owner")

    # Change u_id permission to permission_id
    data['users'][u_id]['permission_id'] = permission_id
