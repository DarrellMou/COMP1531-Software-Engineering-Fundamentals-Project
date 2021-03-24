from src.error import InputError 
from src.data import retrieve_data
from src.auth import auth_token_ok, auth_decode_token
import src.data

def clear_v1():
    src.data.data = {
        "users" : {},
        "channels" : {}
    }
    return {}

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
