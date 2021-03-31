import json
import src.data

def clear_v1():
    src.data.data = {
        "users" : {},
        "channels" : {}
    }
    return {}

    '''
    data = {
        "users" : {},
        "channels" : {},
        "dms" : {},
        "messages" : []
    }
    with open("data.json", "w") as FILE:
        json.dump(data, FILE)
'''
def search_v2(token, query_str):
    
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
                for message in data['channels'][channel]['messages']:
                    # query_str is a substring of message 
                    if query_str in message['message']:
                        collection_messages.append(message['message'])
                break
    
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if member == auth_user_id:
                for message in data['dms'][dm]['messages']:
                    # query_str is a substring of message 
                    if query_str in message['message']:
                        collection_messages.append(message['message'])
                break
    
    return collection_messages

def admin_user_remove_v1(token, u_id):

    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid User")
    user_id = auth_decode_token(token)

    # Check if u_id exists
    if u_id not in data['users']: raise InputError("Invalid User")

    # Checks if authorised user is an owner
    if data['users'][user_id]['permission_id'] == 2: raise AccessError("Not an admin user")

    # Checks if the user is the currently the only owner
    admin_flag = 0
    for user in data['users']:
        if data['users'][user]['permission_id'] == 1:
            admin_flag += 1
    if admin_flag == 1: raise InputError("The user is currently the only owner")

    # Replace channel message with 'Removed user'
    for channel in data['channels']:      
        # If the user is the only owner of the channel
        owner_flag = 0
        member_flag = False
        for member in data['channels'][channel]['owner_members']:
            owner_flag += 1
            if u_id in data['channels'][channel]['owner_members']: member_flag = True
        if member_flag == True and owner_flag == 1:
            raise InputError("The user is the only owner of a channel")

        for member in data['channels'][channel]['all_members']:
            if u_id in data['channels'][channel]['all_members']:
                for message in data['channels'][channel]['messages']:
                    if message['u_id'] == u_id:
                        message['message'] = "Removed user"
                        message['is_removed'] = True
                data['channels'][channel]['all_members'].remove(member)
                break

    # Replace dm message with 'Removed user'
    for dm in data['dms']:
        for member in data['dms'][dm]['members']:
            if u_id in data['dms'][dm]['members']:
                for message in data['dms'][dm]['messages']:
                    if message['u_id'] == u_id:
                        message['message'] = "Removed user"
                        message['is_removed'] = True   
                data['dms'][dm]['members'].remove(member)
                break

    # Replace any messages from u_id with 'Removed user'
    for message in data['messages']:
        if message['u_id'] == u_id:
            message['message'].replace(message['message'], 'Removed user')
            message['is_removed'] = True   
            break

    # Replace user name with 'Removed user'
    # Tell user/profile/v2 to have an if statement for is_removed and only show their name 'Removed user'
    for user in data['users']:
        if user == u_id:
            data['users'][user]['name_first'].replace(data['users'][user]['name_first'], 'Removed user')
            data['users'][user]['is_removed'] = True
            break
    
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    data = retrieve_data()

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError("Invalid User")
    auth_user_id = auth_decode_token(token)

    # Check if u_id exists
    if u_id not in data['users']: raise InputError("Invalid User")

    # Checks if authorised user is an owner
    if not data['users'][auth_user_id]['permission_id'] == 1: raise AccessError("Not an admin user")

    # Checks if permission_id refers to a value permission
    if not (permission_id == 1 or permission_id == 2): raise InputError("Not a value permission")

    # Checks if the user is the currently the only owner
    if permission_id == 2:
        admin_flag = 0
        for user in data['users']:
            if data['users'][user]['permission_id'] == 1:
                admin_flag += 1
        if admin_flag <= 1: raise InputError("The user is currently the only owner")

    data['users'][u_id]['permission_id'] = permission_id

